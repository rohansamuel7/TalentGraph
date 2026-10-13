# Progress

## 2026-10-12 — QA-FIX-01 semantic taxonomy and evidence extraction

- Classified all 50 existing taxonomy IDs independently of the operational M4 category: 15 technical competencies, 25 functional skills, 9 industry/occupational categories, and 1 ambiguous/other.
- Read the original local descriptions for the 1,500 accepted job IDs without changing production DuckDB or exporting descriptions. Extracted 403 deterministic competency relationships across 270 jobs and 19 competency IDs.
- Preserved provenance in ignored `data/processed/job_competency_evidence.json`; no duplicate job/competency pairs were produced.
- The five-case manually reviewed fixture produced TP=5, FP=0, FN=0 (precision 1.00, recall 1.00); this is a bounded rule-regression check, not a production accuracy estimate.
- Rebuild output was byte-identical with SHA-256 `ffa1b812dc4acc0114cff50de3ffa5fd3f2e923c4b9ca7541507479f37ded9d0`.
- QA extraction tests passed 4/4. A subsequent full-suite attempt was environment-limited by Spark socket creation (`Operation not permitted`) in this sandbox; the prior full M1–M7 suite had passed 22/22 before this diagnostic rerun.

## 2026-10-12 — QA-FIX-02 real-description extraction audit

- Built a reproducible 60-job stratified sample using seed `20261012`: 20 jobs with extracted evidence, 20 with dictionary terms but no extracted evidence, and 20 with no detected dictionary terms.
- Review artifact: ignored `data/processed/qa_fix02_review_sample.json`. It contains 73 candidate-level records because some jobs contain multiple candidate terms; all 60 sampled job IDs are represented.
- Review labels remain unset (`ground_truth_status=not_reviewed`); no automated proposal is represented as human ground truth. Snippets are short, whitespace-normalized, and redact URLs, emails, and phone-like values.
- Across all 1,500 accepted jobs, 270 had extracted evidence, 102 had dictionary terms without extracted evidence, and 1,128 had no detected dictionary terms. The most common candidate terms were Excel (225 jobs), SQL (59), Python (57), AWS (40), and Azure (34).
- No precision, recall, or F1 was claimed because no independent human-reviewed labels were available. The audit identifies likely false-negative candidates for manual review but does not change extraction or matching behavior.

## 2026-10-12 — QA-FIX-03 human review worksheet

- Created ignored `data/processed/qa_fix03_human_review.csv` from the QA-FIX-02 artifact without modifying the source artifact.
- Worksheet contains 25 deterministic candidate-level records, 19 unique jobs, and blank `confirmed_label`/`reviewer_rationale` columns. It includes extracted positives, not-extracted candidates, and Excel, SQL, and Python examples.
- Added `docs/QA_FIX03_REVIEW_GUIDE.md` documenting the allowed labels: required, preferred, incidental, negated, and ambiguous.
- Repeat generation was byte-identical; worksheet SHA-256: `5886e9886681fc0edb281ed86ba5162cf6d356509e06fb410f50a4d970a94ef9`.

## 2026-10-12 — QA-FIX-04 requirement classification

- Updated the extractor to separate competency mention detection from classification. Supported classes are `required`, `preferred`, `mentioned`, `negated`, and `ambiguous`.
- Added explicit patterns for proficiency, computer-literacy, effective-working-skills, preferred, highly-desirable, and experience-a-plus language. Ordinary-English “excel in a team environment” is excluded.
- Diagnostic comparison on the same 1,500 accepted jobs: prior QA-FIX-01 artifact had 403 requirement-only relationships; QA-FIX-04 produced 582 classified mentions across 372 jobs and 20 competency IDs: required 322, preferred 42, mentioned 183, negated 5, ambiguous 30.
- QA-FIX-03 and M4 source relationships were not modified; the comparison output was written to `/tmp/qa_fix04_evidence.json`.
- Phrase regression tests passed 6/6; full M1–M7 suite passed 24/24.

## 2026-10-12

- GitHub repository already connected; local branch `main` tracks `origin/main`.
- Workspace contained only `.gitignore` and an ignored `debug.log` before documentation setup.
- Created initial agent and project documentation files.
- No packages installed, data downloaded, system changes made, or pipeline code started.
- M0 verification: WSL 2.1.5.0 is installed and responds; default WSL version is 2, but Ubuntu is not installed. Only stopped `docker-desktop` and `docker-desktop-data` distributions are listed.
- M0 verification: approximately 7.9 GB total physical memory and 0.9 GB free at inspection time. Python 3.11.9 is accessible. Java 23.0.1 is installed; Java 17 was not found in inspected locations. VS Code 1.108.2 is installed; no Remote-WSL extension was listed.
- M0 limitations: disk-space and firmware virtualization queries returned no usable values in the restricted diagnostic session. Exact manual commands are recorded in `agent/ERROR_LOG.md`.
- M0 installation: Ubuntu was installed and registered as a WSL2 distro, but first launch failed with `Wsl/Service/E_UNEXPECTED`; no Linux account was created, so Java, Python environment, packages, Spark, and Airflow setup could not proceed.
- WSL troubleshooting: `wsl --shutdown` completed, but relaunching `wsl -d Ubuntu` reproduced `Catastrophic failure / Wsl/Service/E_UNEXPECTED`. Safe troubleshooting is exhausted without a Windows restart or destructive distro action.

## 2026-10-12 — M0-01 resolved

- Ubuntu 26.04.1 LTS now launches successfully in WSL2; Linux user is `developer`.
- Repository remains at `/mnt/c/Projects/TalentGraph`, and VS Code is connected to WSL Ubuntu.
- Verified from Linux: Python 3.12.15 at `/home/developer/venvs/talentgraph/bin/python`, Java 17.0.20.1, and PySpark 3.5.6.
- User-confirmed local Spark smoke test passed: `spark.range(5).count() == 5`.
- WSL-visible resources at verification time: 3,684,968 kB total memory (~3.5 GiB), 1,984,260 kB available (~1.9 GiB), 1 GiB swap with approximately 1 GiB free. This is the WSL limit/visibility, distinct from the laptop's approximately 8 GiB physical RAM.
- Mounted repository filesystem: 475G total, 65G available, 87% used.
- M0-01 is complete. No packages were installed, datasets downloaded, application code created, or system changes made.

## 2026-10-12 — M1-01 dataset strategy

- Identified the referenced dataset as Kaggle `arshkon/linkedin-job-postings`, “LinkedIn Job Postings (2023 - 2024)”, published by Arsh Koneru and one collaborator.
- Kaggle metadata declares CC BY-SA 4.0 and lists the posting, benefits, companies, and employee-count CSVs. Field names and descriptions were recorded without asserting physical dtypes or version-independent schemas.
- Defined a default deterministic 1,500-posting sample using SHA-256 ranking by `job_id`, plus provenance, missingness, privacy, and related-table filtering rules.
- Defined proposed canonical job, synthetic candidate, skill, job-skill, and candidate-skill contracts.
- M1-01 is complete for strategy design. Approved download-time inspection is still required before M1-02; no dataset was downloaded.

## 2026-10-12 — M1-02 acquisition blocker

- Reviewed `.gitignore` before acquisition and added protections for `.kaggle/`, `kaggle.json`, `artifacts/`, and downloaded archive extensions.
- The official `kaggle` and `kagglehub` clients are not installed, and no local Kaggle credential file was found. No installation or download was attempted.
- Kaggle declares CC BY-SA 4.0, but the underlying LinkedIn collection's privacy/platform-terms boundary for local processing of descriptions, application URLs, and possible incidental personal data remains materially uncertain.
- M1-02 is `BLOCKED` pending an approved official download method/credential setup and explicit privacy/legal approval for local raw-data processing.

## 2026-10-12 — M1-02 archive and sample completed

- Inspected user-provided `data/raw/archive (2).zip`; Git ignores it via `data/`.
- Archive size: 166,472,808 bytes. SHA-256: `4890ecccfdbd6b7ec0e57af6012cae2e960ba74c10702f5957be365469acc7a4`.
- ZIP integrity passed, with 11 members and no unsafe paths. The actual manifest uses `postings.csv` and related `companies/`, `jobs/`, and `mappings/` paths; the ZIP filename does not prove Kaggle version 13.
- Physical postings schema has 31 columns and 123,849 rows. Job IDs are 100% non-null and unique; listed timestamps are all valid millisecond epoch values; zero malformed rows were observed.
- Streaming standard-library sampling produced exactly 1,500 deterministic postings, zero rejects, and Git-ignored metadata/output under `data/processed/`.
- Added `src/talentgraph/m1_sampling.py` and focused standard-library tests. No packages were installed and the raw archive was not modified.

## 2026-10-12 — M2-01 PySpark ingestion

- Added `src/talentgraph/m2_ingestion.py` with explicit 31-column string schema, local[2]/1g Spark configuration, multiline CSV handling, normalization, provenance, rejects, Parquet outputs, and a non-sensitive JSON quality report.
- Production sample run: Spark parsed 1,516 physical records; 1,484 accepted and 32 rejected as `malformed_record`. No duplicate IDs were removed. Descriptions and URLs are excluded from curated outputs.
- Added M2 contract tests. Standard-library regression suite passed: 5 tests. Pytest was not available and no package was installed.

## 2026-10-12 — M2-02 CSV discrepancy resolved

- Python `csv.reader` established the sample as exactly 1,500 logical rows, all width 31 and uniquely identified; 1,443 descriptions contain newlines, 132 contain quotes, and 1,497 contain commas.
- Spark CSV parsing with `multiLine=true` and `STOP_AT_CLOSING_QUOTE` produced 1,516 rows and 32 parser artifacts. The sample was not genuinely malformed.
- M2 now frames bounded CSV records with Python's CSV reader, then applies the explicit Spark schema and transformations. Final run: 1,500 accepted, zero rejects, zero duplicates.
- Added coverage for multiline descriptions, commas, quotes, and true malformed-width rows. Six unittest tests passed. Two final Spark runs produced identical quality-report hashes.

## 2026-10-12 — M3-01 DuckDB modeling

- DuckDB 1.5.6 is installed in the approved virtual environment and configured with a 1 GB memory limit and two threads.
- Added SQL-first models and a reusable builder for company/location dimensions, job facts, aggregate and salary views, and validation queries.
- Built from 1,500 Parquet rows: 1,134 companies, 761 locations, 1,500 facts, 1,456 aggregate rows, and 457 salary rows.
- All six validations passed; full unittest suite passed 7/7. A second rebuild matched model counts and validation output.

## 2026-10-12 — M4-DEBUG / M4-01 disposable validation

- Audited all DuckDB connection sites: M3 builder, M4 builder, and one test context manager. No import-time or nested connections were found; M3/M4 use `finally: con.close()`.
- Disposable reproduction isolated the problematic operation to the 2,498-row `executemany()` bridge insert. Replaced it with a bounded temporary CSV and set-based DuckDB `read_csv` insert; temporary diagnostic PID/open/close logging confirmed clean closure.
- Fresh `/tmp/` rebuilds passed: taxonomy 50, source definitions 35, bridge 2,498, jobs with skills 1,478, source abbreviations 35, unmatched 0, null skill FKs 0, duplicate relationship keys 0.
- Full regression suite passed 10/10. Two disposable rebuilds produced identical counts and match-method distributions.

## 2026-10-12 — M4-01 production validation

- Confirmed no active database holder was reported; production fact count was 1,500.
- Created and validated a separate DuckDB backup using `ATTACH` plus `COPY FROM DATABASE`; backup also contains 1,500 facts.
- Production M4 build completed at `/home/developer/talentgraph_data/talentgraph.duckdb`.
- Final production counts: taxonomy 50, source definitions 35, bridge rows 2,498, jobs with explicit skills 1,478, source abbreviations 35.
- Two production builds retained M1–M3 counts unchanged: companies 1,134, locations 761, facts 1,500. Full regression passed 10/10.

## 2026-10-12 — M5-01 knowledge graph

- Added read-only DuckDB graph builder and deterministic NetworkX queries. Production database was not modified.
- Graph contains 3,445 nodes: 1,500 jobs, 1,134 companies, 761 locations, and 50 skills; 5,498 edges: 1,500 `POSTED_BY`, 1,500 `LOCATED_IN`, and 2,498 `REQUIRES_SKILL`.
- All 22 jobs without explicit skills remain represented. Graph summary SHA-256: `3e0a2fe489d5b51d104b199083f6db1bc3e96174a07980bc883eebcc48f851b8`.
- M5 tests passed 3/3. Full suite was environment-limited by the existing Spark worker Python 3.14 vs driver 3.12 mismatch in an M2 test; no M5 failure occurred.

## 2026-10-12 — ENV-02 Spark Python worker correction

- Root cause: the driver used `/home/developer/venvs/talentgraph/bin/python` 3.12.15 while Spark workers inherited `/usr/bin/python3` 3.14.4 because the PySpark environment variables were unset.
- Updated `create_spark()` to set `PYSPARK_PYTHON`, `PYSPARK_DRIVER_PYTHON`, `spark.pyspark.python`, `spark.pyspark.driver.python`, and `spark.executorEnv.PYSPARK_PYTHON` to the approved interpreter.
- M2 tests passed 3/3; full M1–M5 suite passed 13/13 without external environment variables.

## 2026-10-12 — M6-01 synthetic candidates

- Added deterministic candidate generation from the read-only M4 taxonomy using seed `20261012`.
- Generated exactly 300 fictional candidates and 1,344 candidate-skill relationships across all 50 canonical skill IDs.
- Experience distribution: junior 100, mid 120, senior 80. Artifact written under ignored `data/processed/synthetic_candidates.json`.
- Candidate validation and full M1–M6 regression passed: 14/14 tests.

## 2026-10-12 — M7-01 explainable matching

- Added skill-overlap-only matching over 300 synthetic candidates and 1,500 jobs, using canonical IDs from M4 and explicit job-skill bridge evidence.
- Formula: `matched explicit skills / total explicit job skills`; jobs without evidence receive `insufficient_skill_evidence` and zero coverage.
- Added deterministic top-K job ranking and reverse candidate ranking with job/candidate ID tie-breaking, plus matched/missing explanations.
- Full M1–M7 regression passed 18/18 tests. Production DuckDB remained read-only.
