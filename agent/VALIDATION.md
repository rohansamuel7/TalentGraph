# Validation Plan

## QA-FIX-01 validation

- Semantic classification: `PASS` — technical competency 15, functional skill 25, industry/occupational category 9, ambiguous/other 1; all 50 entries classified independently of M4 operational categories.
- Source availability: `PASS` — all 1,500 accepted jobs had locally available non-empty descriptions; production DuckDB was read-only and unchanged.
- Extraction: `PASS` — 403 relationships, 270 jobs with evidence, 19 canonical competency IDs.
- Canonical integrity/provenance: `PASS` — all IDs belong to the curated dictionary; 403/403 job-competency pairs are unique and required provenance fields are populated.
- False-positive controls: `PASS` on bounded fixture — SQL Server did not match SQL, JavaScript did not match Java, incidental Spark was excluded, and negated Docker/Go/SQL was excluded.
- Manual fixture: `PASS` — TP=5, FP=0, FN=0; precision 1.00 and recall 1.00 on five reviewed cases only. This is not a production accuracy estimate.
- Determinism: `PASS` — independent rebuilds were byte-identical with SHA-256 `ffa1b812dc4acc0114cff50de3ffa5fd3f2e923c4b9ca7541507479f37ded9d0`.
- QA tests: `PASS` — 4/4 extraction tests. Full-suite diagnostic rerun was environment-blocked before test code because Spark socket creation was denied; earlier full M1–M7 regression was 22/22.

## QA-FIX-02 validation

- Sampling: `PASS` — 60 unique accepted jobs selected deterministically with seed `20261012`: 20 extracted-evidence, 20 terms-without-extraction, 20 no-dictionary-term strata.
- Review artifact: `PASS` — `data/processed/qa_fix02_review_sample.json` contains 73 candidate-level records, sanitized snippets, extraction decisions/rule IDs, evidence classifications, and blank proposed/confirmed review fields.
- Ground truth: `NOT RUN` — no independent human labels were available; precision, recall, and F1 are intentionally not reported.
- Coverage diagnostic: `PASS` — all 1,500 descriptions scanned; 270 jobs had extracted evidence, 102 had dictionary terms without extracted evidence, and 1,128 had no detected dictionary terms.
- Regression impact: `PASS` — no extractor, candidate, matching, DuckDB, or M1–M7 source behavior was changed. The review generator ran independently against the local archive.

## QA-FIX-03 validation

- Worksheet format: `PASS` — 25 CSV records with stable IDs, decisions, rule IDs, classifications, and short snippets.
- Required coverage: `PASS` — extracted and not-extracted cases plus Excel (7), SQL (3), and Python (3) candidate records included.
- Human-label safety: `PASS` — all `confirmed_label` and `reviewer_rationale` fields are blank; no ground truth was generated.
- Allowed labels: `PASS` — documented in `docs/QA_FIX03_REVIEW_GUIDE.md`: required, preferred, incidental, negated, ambiguous.
- Uniqueness: `PASS` — 25 unique job/competency review records representing 19 unique jobs.
- Reproducibility: `PASS` — repeated generation was byte-identical; SHA-256 `5886e9886681fc0edb281ed86ba5162cf6d356509e06fb410f50a4d970a94ef9`.

## QA-FIX-04 validation

- Detection/classification separation: `PASS` — mention detection retains provenance and assigns one of five explicit evidence classes.
- Phrase coverage: `PASS` — proficiency in SQL, computer literate in Excel, effective working skills of Excel, Python preferred, highly desirable, and experience-a-plus cases are covered by tests.
- False-positive control: `PASS` — ordinary-English “excel in a team environment” is not emitted as a competency.
- Diagnostic counts: `PASS` — before 403 requirement-only relationships; after 582 classified mentions: required 322, preferred 42, mentioned 183, negated 5, ambiguous 30.
- Tests: `PASS` — QA-FIX-04 phrase tests 6/6; full M1–M7 regression 24/24.
- Accuracy claims: `NOT RUN` — no independently confirmed human labels exist, so precision/recall are not reported.

Results must be marked `PASS`, `FAIL`, or `NOT RUN` only after execution.

| Area | Verification | Success | Failure |
|---|---|---|---|
| Python environment | Version and import smoke checks | Approved interpreter and imports work | Missing/incompatible runtime |
| PySpark | Small local DataFrame job | Job completes with expected schema/count | Startup, schema, or count error |
| DuckDB | Create/query temporary model | Connection and SQL assertions pass | Connection or query failure |
| Airflow | Parse DAG in WSL2 | DAG loads with no import errors | Parse/import/scheduling error |
| Ingestion | Fixture/raw-file run | Records and rejects are accounted for | Silent loss or unclassified rejects |
| Schema integrity | Contract and constraint tests | Types, keys, grain, null rules hold | Contract violation |
| Entity resolution | Known matches and unknowns | Thresholds and reasons are deterministic | Ambiguous or unexplained result |
| Graph | Node/edge fixture checks | Expected relationships exist | Missing/duplicate relationship |
| Incremental/idempotency | Repeat and changed-input runs | No duplicate outputs; updates isolated | Duplicate or non-repeatable output |
| Data quality | Null, uniqueness, referential, range checks | Checks report actionable results | Undetected invalid data |
| Matching | Hand-calculated fixtures | Scores and explanations match expected values | Score drift or missing reason |
| Streamlit | App smoke launch | Verified outputs render without crash | Startup/render/data error |
| Regression | Full approved test suite | All required tests pass | Any unreviewed failure |

Current status: M0-01 environment verification is `PASS`; application validation is `NOT RUN` because implementation has not started.

## M2-01 validation

- Explicit schema and sensitive-field exclusion tests: `PASS` — 2 M2 tests; full unittest discovery 5/5 passed.
- Spark production smoke run: `PASS` — 1,516 parsed records, 1,484 accepted, 32 malformed rejects, zero duplicate removals.
- Reject output and quality report: `PASS` — Parquet rejects plus non-sensitive JSON metrics generated under ignored `data/processed/m2_ingestion/`.
- Pytest suite: `NOT RUN` — pytest is unavailable in the approved virtualenv; no installation was attempted.
- Repeat-run consistency: `PASS` after deterministic run metadata is applied; rerun comparison should use identical report and Parquet content.

## M2-02 validation

- Python logical CSV count: `PASS` — 1,500 records, all 31 fields, 1,500 unique job IDs.
- Spark-vs-Python diagnosis: `PASS` — Spark-only 1,516-row result was caused by unescaped quote handling in multiline descriptions; 32 rejects were parser artifacts.
- Corrected ingestion: `PASS` — 1,500 accepted, zero rejected, zero duplicate removals.
- Quoted-field tests: `PASS` — multiline, comma, escaped-quote, and malformed-width fixture coverage included.
- Repeat-run/idempotency: `PASS` — two final runs produced identical quality-report SHA-256 `fe52ec094269df094cbc8f5593a8b21b688acff86b7e69f68d1eb811b21cd206`.

M0-01 verification: Ubuntu 26.04.1 LTS launches successfully in WSL2 as user `developer`; Python 3.12.15, Java 17.0.20.1, PySpark 3.5.6, memory, disk, and Git checks were completed. The requested local Spark test was confirmed by the user as `PASS` (`spark.range(5).count() == 5`). A repeat attempt in this restricted audit shell was not executable because Java socket creation was denied by the sandbox; this is an audit-environment limitation, not an application failure.

WSL-visible memory was 3,684,968 kB total (~3.5 GiB) and 1,984,260 kB available (~1.9 GiB), with 1 GiB swap. These values are distinct from the laptop's approximately 8 GiB physical RAM.

Prior WSL launch failures are historical and resolved; no further WSL troubleshooting is pending for M0-01.

## M1-01 validation

- Dataset identity and Kaggle metadata review: `PASS` — completed against the referenced Kaggle page without downloading.
- License metadata review: `PASS` — Kaggle declares CC BY-SA 4.0; legal/privacy conditions and ShareAlike obligations are documented.
- Source field-name review: `PASS` — field names/descriptions recorded from accessible Kaggle metadata.
- Physical schema, hashes, exact file sizes, encodings, dtypes, and versioned row counts: `NOT RUN` — requires approved download and inspection.
- Deterministic sample/provenance design: `PASS` — documented in `docs/DATASET_STRATEGY.md`.
- Synthetic candidate contract: `PASS` — fixed seed, labels, safeguards, and versioning documented.
- Dataset download/package installation/application tests: `NOT RUN` by instruction.

## M1-02 acquisition preflight

- `.gitignore` protection review: `PASS` — raw data directories, CSV/TSV/Parquet files, archives, artifacts, and Kaggle credential locations are ignored.
- Official Kaggle client availability: `FAIL` — `kaggle` and `kagglehub` are not installed.
- Kaggle credential availability: `NOT RUN` — no credential file was found; no secrets were inspected or exposed.
- Licensing/privacy preflight: `FAIL` — the Kaggle page declares CC BY-SA 4.0, but local processing of LinkedIn-derived descriptions, application URLs, and possible incidental personal data requires an explicit privacy/terms decision.
- Dataset download: `NOT RUN` — stopped before acquisition as required.
- Physical schema, hashes, sampling, and schema tests: `NOT RUN` — acquisition did not occur.

## M1-02 archive and sampling validation

- Archive Git-ignore check: `PASS` — `data/raw/archive (2).zip` is ignored by `data/`.
- ZIP readability/integrity: `PASS` — `testzip()` returned no errors.
- Unsafe ZIP path scan: `PASS` — no absolute, parent-traversal, or backslash paths.
- Archive provenance: `PASS` — size and SHA-256 recorded in `docs/DATASET_STRATEGY.md` and sample metadata.
- Actual manifest/header inspection: `PASS` — 11 members; `postings.csv` has 31 columns.
- Physical postings validation: `PASS` — 123,849 rows, 123,849 unique/non-empty job IDs, valid listed timestamps, zero malformed rows.
- Deterministic sample: `PASS` — exactly 1,500 rows selected using SHA-256 job-ID ranking; rerun fixture test produced identical output.
- Reject handling: `PASS` — malformed fixture row was classified as `column_count_mismatch`; production reject output contains only its header because no production malformed rows were found.
- Focused tests: `PASS` — 3 standard-library unit tests passed.
- Full project regression suite: `NOT RUN` — no broader application suite exists yet.

## M3-01 validation

- M2 input Parquet count: `PASS` — 1,500 rows.
- DuckDB build: `PASS` — memory limit 1 GB, threads 2.
- Model counts: `PASS` — company 1,134; location 761; fact 1,500; aggregate 1,456; salary 457.
- SQL constraints: `PASS` — row count, unique keys, foreign keys, timestamp range, and salary constraints.
- Automated tests: `PASS` — full unittest discovery 7/7.
- Repeat rebuild: `PASS` — matching counts and validation results; report hash `4d99966ed4bf8354c4cd5d708a093ac15991c3875f7ec430426bb29c5c12c0ff`.

## M4-DEBUG / M4-01 validation

- Connection audit: `PASS` — no nested/import-time connections; explicit `finally` close confirmed.
- Disposable reproduction: `PASS` — failure isolated to bridge `executemany`; fresh `/tmp/` database no longer locks after set-based CSV insert.
- Taxonomy/source preservation: `PASS` — 50 taxonomy rows, all 35 source definitions represented.
- Bridge integrity: `PASS` — 2,498 rows, 1,478 jobs covered, 35 source abbreviations, zero unmatched, zero null skill foreign keys, zero duplicate relationship keys.
- Matching methods: `PASS` — all 2,498 explicit mappings matched by exact/alias; no fuzzy matching was forced.
- Full regression: `PASS` — 10/10 unittest tests.
- Disposable idempotency: `PASS` — two rebuilds matched counts and method distributions.

## M4-01 production validation

- Production preflight: `PASS` — no active holder reported; `fact_job_posting` count 1,500.
- DuckDB backup: `PASS` — created with `ATTACH`/`COPY FROM DATABASE`; reopened successfully with 1,500 facts.
- Production taxonomy: `PASS` — 50 rows, including all 35 source definitions.
- Production bridge: `PASS` — 2,498 rows and 1,478 covered jobs.
- Integrity: `PASS` — unique relationship keys, job and skill foreign keys, provenance fields, and exact/alias matching method checks.
- Idempotency: `PASS` — second build preserved M1–M3 counts (1,134 companies, 761 locations, 1,500 facts) and reproduced M4 counts.
- Full regression: `PASS` — 10/10 unittest tests.
- Connection lifecycle: `PASS` — preflight, backup, validation, and rebuild connections closed cleanly; no production lock recurred.

## M5-01 validation

- Production DuckDB read-only access: `PASS` — M4 counts confirmed; no writes performed.
- Graph node counts: `PASS` — Job 1,500; Company 1,134; Location 761; Skill 50.
- Graph edge counts: `PASS` — `POSTED_BY` 1,500; `LOCATED_IN` 1,500; `REQUIRES_SKILL` 2,498.
- Integrity: `PASS` — no dangling references or duplicate directed edges; 22 no-skill jobs retained.
- Query tests: `PASS` — skill frequency, company-skill, co-occurrence, skill-combination, and no-skill queries.
- Repeatability: `PASS` — two independent builds produced the same summary hash `3e0a2fe489d5b51d104b199083f6db1bc3e96174a07980bc883eebcc48f851b8`.
- M5 tests: `PASS` — 3/3.
- Full regression: `FAIL (environment)` — existing Spark framing test encountered Python worker 3.14 versus driver 3.12; M1, M3, M4, and M5 tests passed in the same run.

## ENV-02 validation

- Driver interpreter: `PASS` — `/home/developer/venvs/talentgraph/bin/python`, Python 3.12.15.
- Worker interpreter: `PASS` — Spark worker configuration now uses the same approved Python executable; the M2 worker DataFrame test completed successfully.
- M2 regression: `PASS` — 3/3 tests.
- Full M1–M5 regression: `PASS` — 13/13 tests.
- System Python: `PASS` — `/usr/bin/python3` was not modified.

## M6-01 validation

- Taxonomy read-only access: `PASS` — 50 canonical skill IDs loaded from production DuckDB.
- Candidate count: `PASS` — exactly 300.
- Relationship count: `PASS` — 1,344 candidate-skill relationships.
- Experience distribution: `PASS` — junior 100, mid 120, senior 80.
- Skill references and uniqueness: `PASS` — all references exist in `dim_skill`; candidate IDs are unique; experience values are consistent.
- Deterministic rebuild: `PASS` — repeated generation with seed `20261012` produced byte-identical JSON.
- Full M1–M6 regression: `PASS` — 14/14 unittest tests.

## M7-01 validation

- Reference loading: `PASS` — 1,500 jobs, 300 candidates, 2,498 explicit job-skill relationships.
- Scoring edge cases: `PASS` — full, partial, zero, and no-evidence coverage behavior.
- Ranking: `PASS` — configurable top-K and deterministic stable-ID tie-breaking.
- Reverse lookup: `PASS` — candidates ranked for a specified job.
- False-positive safeguards: `PASS` — only canonical skill-key intersections; broad categories are not converted into technical skills.
- Repeatability: `PASS` — repeated integration ranking results identical.
- Full M1–M7 regression: `PASS` — 18/18 unittest tests.
