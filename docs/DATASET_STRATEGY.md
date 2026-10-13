# M1-01 Dataset Strategy

## Status

M1-01 is complete for provenance planning and bounded-sample design. Download-time inspection remains required before M1-02 because Kaggle's accessible page metadata does not establish physical CSV dtypes, checksums, exact row counts for every file, or whether a later dataset version changes the manifest.

## M1-02 acquisition result

The user-provided archive was inspected locally without extraction. It is a valid ZIP with 11 safe members and a 166,472,808-byte size. Its SHA-256 is `4890ecccfdbd6b7ec0e57af6012cae2e960ba74c10702f5957be365469acc7a4`. The archive contains `postings.csv` (516,843,769 uncompressed bytes), three company mapping tables plus employee counts, four job mapping/detail tables, and two mapping tables. It does not use the metadata page's earlier `job_postings.csv` path, so the source version is recorded as unknown from the archive itself; the approved target was version 13.

The physical `postings.csv` has 31 columns and 123,849 data rows. All 123,849 `job_id` values are non-empty and unique; all `listed_time` values are non-empty and valid millisecond epoch values; no malformed rows were observed. The header includes `company_name`, `normalized_salary`, `zip_code`, and `fips`, while the earlier metadata description did not list those fields. Sensitive or potentially sensitive fields include `description`, `skills_desc`, `job_posting_url`, `application_url`, company descriptions/addresses/URLs, and location fields. These remain local-only and are not printed into logs or redistributed.

The streaming standard-library sampler produced 1,500 rows in `data/processed/job_postings_sample.csv`, zero rejects, and metadata in `data/processed/sample_metadata.json`. These outputs are Git-ignored. The archive and raw records remain unchanged.

## Public job source

The dataset reference in `docs/PROJECT_SPEC.md` (`https://www.kaggle.com/dsv/9200871`) resolves to the Kaggle dataset slug `arshkon/linkedin-job-postings`, titled **LinkedIn Job Postings (2023 - 2024)**. The Kaggle page identifies **Arsh Koneru and one collaborator** as the publisher/contributors and links scraper code at `https://github.com/ArshKA/LinkedIn-Job-Scraper`.

Authoritative metadata page: `https://www.kaggle.com/datasets/arshkon/linkedin-job-postings/versions/13`.

The Kaggle metadata states that the dataset contains 124,000+ postings from 2023 and 2024 and declares **CC BY-SA 4.0**. Reuse must include attribution, a license link, an indication of changes, and ShareAlike treatment for distributed adaptations. The dataset's underlying LinkedIn collection and any platform terms/privacy obligations require a separate legal/privacy review; the Kaggle license alone is not treated as permission to redistribute personal or copyrighted text.

### Metadata-listed files

The page describes these CSV files:

- `job_postings.csv`
- `job_details/benefits.csv`
- `company_details/companies.csv`
- `company_details/employee_counts.csv`

The page's metadata describes the first as the posting fact and the other three as related tables. The exact versioned manifest, file sizes, hashes, row counts, encoding, delimiter, and physical dtypes are **not verified until an approved download and inspection**.

## Verified source fields

These names and descriptions are transcribed from the Kaggle metadata; they are not yet a local schema contract:

### `job_postings.csv`

`job_id`, `company_id`, `title`, `description`, `max_salary`, `med_salary`, `min_salary`, `pay_period`, `formatted_work_type`, `location`, `applies`, `original_listed_time`, `remote_allowed`, `views`, `job_posting_url`, `application_url`, `application_type`, `expiry`, `closed_time`, `formatted_experience_level`, `skills_desc`, `listed_time`, `posting_domain`, `sponsored`, `work_type`, `currency`, `compensation_type`.

### `job_details/benefits.csv`

`job_id`, `type`, `inferred`.

### `company_details/companies.csv`

`company_id`, `name`, `description`, `company_size`, `country`, `state`, `city`, `zip_code`, `address`, `url`.

### `company_details/employee_counts.csv`

`company_id`, `employee_count`, `follower_count`, `time_recorded`.

## Proposed canonical schemas

These are TalentGraph contracts, not claims about source columns. Raw source columns must be preserved separately with `source_file`, `source_version`, `source_row_number`, `ingestion_run_id`, `retrieved_at_utc`, and `raw_record_hash`.

### `job_posting`

One row per source `job_id` and source version.

| Field | Type/requirement | Rule |
|---|---|---|
| `job_key` | string, required | Stable key: `linkedin:{job_id}`; never regenerated from title/text |
| `source_job_id` | string, required | Raw `job_id` preserved as text |
| `source_company_id` | string, nullable | Raw company key |
| `title` | string, nullable | Preserve raw and normalized forms |
| `description` | string, nullable | Preserve only under approved handling policy |
| `location` | string, nullable | Raw location; no geocoding in M1 |
| `work_type` | string, nullable | Preserve both `work_type` and `formatted_work_type` if present |
| `experience_level` | string, nullable | Canonical field from formatted source field |
| `listed_at`, `original_listed_at`, `expires_at`, `closed_at` | timestamp, nullable | Parse only after format inspection; retain parse errors |
| `remote_allowed` | boolean, nullable | Do not coerce unknown values to false |
| `min_salary`, `med_salary`, `max_salary` | decimal, nullable | Preserve currency and pay period |
| `currency`, `pay_period`, `compensation_type` | string, nullable | Controlled values validated after inspection |
| `source_url`, `application_url` | string, nullable | Treat as potentially sensitive/external links |
| `source_version`, `retrieved_at_utc`, `raw_record_hash` | required metadata | Provenance and idempotency |

### `candidate_profile`

One row per synthetic candidate version. Fields: `candidate_key`, `candidate_version`, `synthetic_label` (always `true`), `generation_seed`, `generated_at_utc`, `target_role_family`, `experience_level`, `location`, `work_authorization` (coarse category only), `years_experience`, `summary`, and `raw_record_hash`. No real names, emails, phone numbers, addresses, employers, schools, or copied resumes.

### `skill`

One row per controlled concept: `skill_key`, `canonical_name`, `skill_type`, `taxonomy_version`, `aliases_json`, `provenance`, `active_flag`. Raw terms are never overwritten.

### `job_skill` and `candidate_skill`

Relationship grain is one source entity, raw skill term, and ontology decision. Fields: `relationship_key`, entity key, `raw_skill_term`, `normalized_skill_term`, nullable `skill_key`, `match_status` (`matched`, `review`, `unknown`), `confidence`, `match_reason`, `source_file`, `source_row_number`, `ontology_version`, and `created_at_utc`. Duplicate relationship keys must be rejected; unknown and review outcomes are retained.

## Bounded deterministic sample

Use **1,500 job postings** as the default sample, with an allowed configured range of 1,000–2,000. Do not load the full corpus into memory.

1. Read only `job_postings.csv` in streaming/chunked mode or bounded Spark partitions.
2. Validate `job_id` is present; reject and count null/invalid IDs.
3. Deduplicate by `job_id`, retaining the row with the greatest valid `listed_time`, then lowest source row number as deterministic tie-breaker.
4. Compute a stable hash from `job_id` using SHA-256 and select rows where the unsigned hash rank is lowest, after sorting by `(hash, job_id)`.
5. Select exactly 1,500 valid postings when at least that many exist; otherwise fail the contract rather than silently lowering the target.
6. Filter all related benefits to selected `job_id`s and all company/employee rows to selected `company_id`s.
7. Record `sample_method`, `sample_seed` (not needed for hash ranking), source version, selection timestamp, input row count, selected row count, rejected count, and hash algorithm.

The hash-ranked approach is reproducible across runs and does not depend on file order. A stratified sample may be evaluated later, but it must be approved separately because it changes the reproducibility contract.

## Provenance, missingness, and validation

- Preserve source title, publisher, source URL, dataset version, file name, retrieval timestamp, license, and transformation version.
- Store source timestamps as raw values plus parsed UTC values; never fabricate dates.
- Represent absent values as typed nulls. Empty strings, sentinel values, and malformed timestamps are classified before conversion.
- Preserve malformed records in a rejects artifact with reason and source row number; do not silently drop them.
- Validate file manifest, encoding, headers, required IDs, uniqueness, referential integrity, timestamp parse rates, salary consistency, allowed booleans, and duplicate relationships after download.
- Hash downloaded files and record hashes only after an approved download; do not claim them now.
- Do not publish raw descriptions or application URLs in demo artifacts until privacy/copyright review approves their use.

## Synthetic candidates

Generate approximately **300** candidates with a fixed documented seed, proposed default `20261012`, using controlled role families, experience bands, coarse locations, and skills sampled from the approved ontology. Every row receives `synthetic_label=true`, `source_type=synthetic`, `generation_seed=20261012`, and a deterministic `candidate_key` such as `synthetic:candidate:000001`.

Candidate profiles must be fictional and generated from templates and controlled vocabularies. Do not use real resumes, names, contact details, exact addresses, real employers, or identifiable combinations. Include a small deliberate proportion of missing optional fields and unknown skills to exercise quality paths. Candidate updates must increment `candidate_version` and preserve prior versions.

## Acceptance criteria

- Dataset identity, publisher, URL, license, and metadata-listed files are recorded.
- Verified source fields are separated from proposed canonical fields.
- Unverified dtypes, hashes, file sizes, row counts, and version drift are explicitly listed.
- A deterministic 1,500-row selection method and related-table filtering strategy are documented.
- Job, candidate, skill, and relationship grains/keys are defined.
- Provenance, missingness, malformed-record, privacy, and licensing rules are documented.
- Synthetic candidate generation has a fixed seed, labels, safeguards, and versioning.
- No dataset is downloaded and no package is installed during M1-01.
