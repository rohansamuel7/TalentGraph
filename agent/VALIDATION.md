# Validation Plan

## M8-RELEASE-02 publication checks — 2026-10-13

- Publication target: `main` → `https://github.com/rohansamuel7/TalentGraph.git` (`origin`).
- Owner browser confirmation: light mode and a narrow viewport were checked. Light mode looks somewhat unusual to the owner, who accepted that appearance because dark mode is intended for use. This is an accepted presentation caveat, not an independent visual pass by the agent.
- Staging scope: only public source, docs, requirements, frontend lockfile, screenshots, and background are intended. Final staged path, content, README-link, and whitespace checks are required before commit.
- Final release review: 80 committed files; no excluded paths, obvious secret patterns, or nonstandard Git modes; 11 local README links resolve; all four screenshots and the background are included; `git diff --cached --check` passed before commit. No private guide, data, databases, dependencies, build output, or local Node binaries were committed.
- Publication: `git -c credential.helper='!gh auth git-credential' push origin main` succeeded without force. `git ls-remote origin refs/heads/main` returned `78f9eda0ddf2184bc16eaaa977f21d3b4d381d81`, matching local HEAD at verification.

## M8-RELEASE-01 validation — 2026-10-13

- Git: `main` with `origin` configured; no staged files; 96 tracked or non-ignored candidate files; no excluded data, databases, private guide, dependencies, build output, or local Node binaries among them. `git diff --check`: PASS.
- Python: complete `unittest` suite passed 44 tests, 0 failures, 0 skips, including Spark, outside the restricted socket sandbox. Frontend: TypeScript PASS, ESLint PASS, Next.js production build PASS (7 static pages); no frontend test script is configured.
- API: health, overview, jobs, candidates, matches, graph neighborhood, and skill frequency returned HTTP 200 in a read-only test client. Overview returned 1,500 sampled jobs and 300 synthetic candidates; coverage groups were 80 required, 7 preferred-only, 44 non-required, and 1,369 insufficient. SQL and Python frequencies were 42 and 35 distinct jobs.
- Assets: four accurately named screenshots and the background are present with distinct hashes and reasonable PNG sizes (0.7–2.1 MB). README relative screenshot links resolve. Screenshots show dark mode and no obvious credentials. Current light-mode contrast and responsive crop were not rechecked in a browser.
- Database SHA-256: production `663dbe12cde5231e4d1dc65a880041ecaffe840469a0efcf4a0c8db5202dc397`; repository processed `b2314da8faf5aea8ad8643a1790c96ce7b116bb0ce544473883f45e37f889160`. Both match the expected values after checks.
- Release follow-up: the user explicitly confirmed permission for this repository's use of the artwork; treat the prior licensing gate as resolved on that basis. The audit is **READY** with a documented caveat that fresh light-mode and responsive browser checks were not performed. No commit, push, or deployment performed.

## M8-DOCS-02 validation — 2026-10-13

- Visually mapped each original screenshot to its destination name and inspected for obvious private information; none was observed.
- Original and destination bytes matched for all four PNGs (SHA-256 comparison). Their dimensions were verified; all four README image links resolve to copied files.
- `git diff --check`: PASS. No application code or data was changed.

## M8-DOCS-01 validation — 2026-10-13

- Documentation: four requested files created; 24 local Markdown links checked with no missing targets; historical claims cross-checked against source and milestone records.
- Python dependencies: all eight exact pins across `requirements.txt` and its included backend file matched installed distributions. Pandas and PyArrow are installed but have no direct application imports; pytest, Plotly, Streamlit, and Airflow are not installed in the working virtual environment.
- Syntax and frontend: modified Python files parsed successfully; TypeScript and ESLint passed. No frontend production build or pipeline regeneration was run.
- Regression: restricted-shell unittest discovery ran 44 tests with one Spark startup error caused by Java socket denial; the approved unrestricted rerun passed all 44 in 44.215 seconds. The failure remains recorded as an environment limitation.
- Database: production `/home/developer/talentgraph_data/talentgraph.duckdb` SHA-256 remained `663dbe12cde5231e4d1dc65a880041ecaffe840469a0efcf4a0c8db5202dc397`; repository `data/processed/talentgraph.duckdb` remained `b2314da8faf5aea8ad8643a1790c96ce7b116bb0ce544473883f45e37f889160`. Neither was opened for writing.
- `git diff --check`: PASS. Existing unrelated worktree changes and untracked frontend/docs files were preserved; no commit or push.

## M8-VISUAL-02 validation — 2026-10-13

- Frontend TypeScript: PASS. ESLint: PASS.
- Browser visual review: NOT RUN; inspect sidebar image crop and navigation contrast in light and dark themes.

## M8-VISUAL-01 validation — 2026-10-13

- Inspected the final 1854 × 848 PNG: rocket, rider, stars, clouds, and planet remain; page text and controls are absent.
- Frontend TypeScript and ESLint: PASS using the repository's user-scoped Node toolchain. `git diff --check`: PASS.
- Browser visual review and production build: NOT RUN for this CSS and static-asset change. Light/dark opacity and responsive crop should be checked in the browser.

## M8-POLISH-04 validation

- Development server check: no active Next.js dev server was present before production build.
- TypeScript: PASS.
- ESLint: PASS.
- Production build: PASS — Next.js compiled and generated all seven static pages.
- Dedicated frontend test suite: NOT CONFIGURED in `frontend/package.json`; no new dependency or test framework was added.
- `git diff --check`: PASS.
- Split selection/filter behavior: code-validated; result selection uses semantic buttons with `aria-pressed` and a visible focus indicator.
- Graph button: explicit scoped `.show-more` CSS fixes the missing-style/flex-stretch root cause; browser rendering remains manual.
- Browser interaction/viewport checks: unavailable here; verify at 1366×768 and 1920×1080, including keyboard selection and list/detail scrolling.

## M8-POLISH-03 validation

- TypeScript: PASS.
- ESLint: PASS.
- Production build: PASS — all seven static pages generated.
- Graph labels: source confirms React Flow preferred text labels removed; accessible edge descriptions and Required/Preferred legend remain. Visual check requires browser.
- Split-view selection and responsive layout: code/build validated; browser interaction unavailable in this environment.
- `git diff --check`: PASS.

## M8-POLISH-02 validation

- Font inspection: no Avenir or local Lato files available; Lato-first CSS stack uses Windows/system fallbacks and no runtime font network dependency.
- TypeScript: PASS.
- ESLint: PASS.
- Production build: PASS — all seven static pages generated successfully.
- Focused FastAPI regression: PASS — 8/8 tests.
- `git diff --check`: PASS.
- Matching and graph backend semantics: unchanged; existing API contracts remain in use.
- Browser visual verification: NOT RUN — browser automation is unavailable; manually inspect both themes at 1366x768 and 1920x1080.

## M8-MIGRATE-06 validation

- Browser tooling: NOT AVAILABLE — no Playwright, Chromium, Chrome, Firefox, or Puppeteer executable was found; no installation attempted.
- Frontend routes: PASS by production build — `/network`, `/matches`, `/insights`, and the redirect route were statically generated.
- Backend endpoint audit: PASS — health, overview, jobs, job detail, candidates, candidate detail, matches, and graph neighborhood direct calls returned valid typed data.
- Coverage: PASS — 80 required, 7 preferred-only, 44 non-required-only, 1,369 no eligible technical evidence; 1,420 lack required evidence.
- Representative matches: PASS — candidates `synthetic:candidate:000001`, `000076`, and `000226` returned real comparison rows.
- TypeScript: PASS; ESLint: PASS; production build: PASS; `git diff --check`: PASS.
- Full Python regression: 42/43 passed; one existing Spark test is environment-blocked by Java socket creation permissions, not application behavior.
- DuckDB SHA-256 observed unchanged during this task: `663dbe12cde5231e4d1dc65a880041ecaffe840469a0efcf4a0c8db5202dc397`.
- Manual browser checks remain: 1366x768 and 1920x1080 at 100% zoom; route navigation, graph interactions, match filtering/expansion, light/dark persistence, and console inspection.

## M8-MIGRATE-05A validation

- Root cause: the pre-hydration theme script intentionally added `data-theme` before React hydration, creating the reported root attribute mismatch.
- Fix: narrow `suppressHydrationWarning` on `<html>` only; the script remains responsible for no-flash localStorage/system initialization, while React component initial state remains deterministic.
- Browser automation: unavailable; saved light/dark, system dark, toggle, refresh, and extension-isolation checks require manual browser verification.

## M8-MIGRATE-05 validation

- Browser automation: unavailable; light/dark visual and interaction checks remain manual at supported desktop sizes.
- Frontend TypeScript: PASS.
- Frontend ESLint: PASS.
- Next.js production build: PASS.
- Full Python regression: 42/43 passed; 1 Spark framing test was blocked by restricted-shell Java socket creation (`Operation not permitted`).
- DuckDB checksum observed: `663dbe12cde5231e4d1dc65a880041ecaffe840469a0efcf4a0c8db5202dc397`; no database write was performed in this task.
- `git diff --check`: PASS.

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

## QA-FIX-05 validation

- Worksheet reconciliation: `PASS` — all 25 source records are present and uniquely identified by job key plus competency display value.
- Updated extraction: `PASS` — each row was re-evaluated against the QA-FIX-04 extractor and includes the updated decision, class, and bounded evidence snippet.
- Human-label preservation: `PASS` — `confirmed_label` and `reviewer_rationale` match the original worksheet exactly; no proposed labels were treated as confirmed.
- Reconciliation summary: `PASS` — 3 previously missed explicit requirements are identified; required/preferred corrections, incidental/ambiguous cases, and remaining review cases are documented.
- Targeted QA tests: `PASS` — 6/6 `test_qa_fix_extraction` tests.
- Full regression: `PASS` — 24/24 tests under the approved local Spark environment. The restricted shell attempt was environment-limited before Spark test code ran.
- Production DuckDB: `PASS` — no database access or writes were performed; production database timestamp was unchanged.
- Maintainability: `PASS` — reconciliation orchestration is 96 lines and archive/evidence I/O is isolated in a 37-line helper module; `git diff --check` passed.

## QA-FIX-06 validation

- Human-label import: `PASS` — exactly 25 unique job/competency records validated; raw human labels preserved separately from AI proposal fields.
- Description completeness: `PASS` — all 19 unique source descriptions found in `postings.csv`; every output row contains the complete original description and a deterministic UTF-8 SHA-256.
- Evidence quality: `PASS` — original excerpts, cleaned full excerpts, bounded previews, extraction method, source file, and source row are present; 7 display cleanups were applied without changing source text.
- No-dictionary cases: `PASS` — five complete descriptions retained and human labels remain `ambiguous` with unresolved review flags.
- Java judgment: `PASS` — raw `required/preferred` label preserved and flagged unresolved; no coercion performed.
- Focused tests: `PASS` — QA-FIX-06 plus QA-FIX-04 tests passed 8/8.
- Full regression: `PASS` — 26/26 tests under the approved local Spark environment.
- Scope safety: `PASS` — production DuckDB, source data, extractor, M6, and M7 were not modified.

## QA-FIX-07 validation

- Java resolution: `PASS` — raw `required/preferred` preserved; resolved to `preferred` only because the full description presents Java as an alternative to Python.
- Final label preservation: `PASS` — all 25 rows retained; final counts are required 15, preferred 4, incidental 1, ambiguous 5.
- No-term review: `PASS` — all five complete descriptions inspected and documented with exact quotations; suggestions are coverage prompts only.
- Evaluation: `PASS` — confusion matrix and supported per-class metrics generated for 17 comparable records; five no-term and three `mentioned` predictions excluded with reasons.
- Focused tests: `PASS` — QA-FIX-07, QA-FIX-06, and QA-FIX-04 tests passed 10/10.
- Full regression: `PASS` — 32/32 tests under the approved local Spark environment.
- Scope safety: `PASS` — production DuckDB, extractor, taxonomy, M6, and M7 were not modified.

## M6-REFINE-01 validation

- Candidate count and IDs: `PASS` — exactly 300 unique stable synthetic candidate IDs.
- Role-family distribution: `PASS` — data engineering, analytics, software engineering, and cloud/platform engineering each have 75 candidates.
- Seniority distribution: `PASS` — junior 100, mid 120, senior 80; years remain within each band.
- Technical bridge: `PASS` — 1,527 relationships across 14 allowed technical competencies; no broad category labels appear.
- Referential integrity: `PASS` — all candidate-skill relationships reference an existing candidate and taxonomy skill.
- Determinism: `PASS` — repeated generation is byte-identical with seed `20261012`.
- M7 compatibility: `PASS` — existing M7 integration and scoring tests pass without M7 changes.
- Regression: `PASS` — full unittest suite completed 28/28; `git diff --check` passed.

## M7-REFINE-01 validation

- Eligibility filtering: `PASS` — only canonical technical/cloud/data-engineering competency keys from the evidence artifact are matched; broad M4 categories are excluded.
- Evidence status: `PASS` — no evidence has null overlap and `insufficient_evidence`; one observed requirement is `limited_evidence`; larger observed sets are `sufficient_for_limited_comparison`.
- Explainability: `PASS` — outputs include required/preferred counts, matched/missing skills, source, extraction version, and an explicit overlap limitation.
- Ranking: `PASS` — both directions prioritize evidence status, then overlap, observed evidence, preferred matches, and stable identifiers.
- Evidence inventory: `PASS` — 101 required-evidence jobs, 0 preferred-only jobs, and 1,399 insufficient jobs recorded from the stable artifact.
- Focused tests: `PASS` — M7 and M6 tests passed 6/6.
- Full regression: `PASS` — 28/28 tests under the approved local Spark environment.
- Scope safety: `PASS` — M6, taxonomy, extractor, production DuckDB, and Streamlit were not modified.

## M7-REFINE-02 validation

- Lineage: `PASS` — canonical artifact rebuilt from the unchanged QA-FIX-04 extractor, accepted sample, and original archive descriptions.
- Canonical schema: `PASS` — `m7-evidence-v2`, extraction `qa-fix-04-v1`, 582 stable relationships, all five classifications, source text, row locations, hashes, rules, and versions.
- Coverage: `PASS` — 80 required, 7 preferred-only, 44 non-required mention/negated/ambiguous, and 1,369 with no eligible technical evidence across 1,500 jobs.
- Loader safety: `PASS` — stale schema/version and missing provenance tests fail closed; no fallback to QA-FIX-01.
- Human review: `PASS` — QA-FIX-07 labels remain separate; 13 comparable disagreements are documented without accuracy overclaiming.
- Determinism: `PASS` — canonical artifact ordering and repeated hash validation are stable.
- Focused tests: `PASS` — evidence pipeline and M7 tests passed 8/8.
- Full regression: `PASS` — 29/29 tests under the approved local Spark environment.
- Scope safety: `PASS` — production DuckDB, extractor, taxonomy, M6, and M7 scoring semantics were not changed.

## M8-01 validation

- Streamlit dependency: `PASS` — version 1.65.0 imports from the existing TalentGraph virtual environment; no package installation was performed during implementation.
- Dashboard data loading: `PASS` — 1,500 jobs, 300 synthetic candidates, and `m7-evidence-v2` are validated through M7 APIs.
- UI behavior tests: `PASS` — coverage counts, empty results, null-company fallback, one-skill limited evidence, and insufficient-score handling covered in focused tests.
- Startup smoke: `PASS` — elevated headless Streamlit server started on localhost:8501 and stopped cleanly. Restricted-shell retry was socket-permission limited.
- Browser/screenshot check: `NOT RUN` — no browser automation or screenshot tool was available in the execution environment.
- Full regression: `PASS` — 37/37 tests under the approved local Spark environment.
- Scope safety: `PASS` — no M4, M6, M7 scoring, extractor, taxonomy, or production DuckDB changes.

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

## M8-02 validation

- Streamlit import: `PASS` — version 1.65.0 in the approved TalentGraph virtual environment.
- Streamlit AppTest: `PASS` — five-page navigation configured with unique paths; startup completed with zero exceptions.
- Dashboard behavior tests: `PASS` — 6/6, including coverage, search/evidence filtering, empty results, missing company fallback, one-skill overlap display, and insufficient-evidence separation.
- Full regression: `PASS` — unittest discovery completed successfully with Spark tests run under the approved environment and required socket permissions.
- Headless localhost startup: `PASS` — Streamlit server started on port 8501 and was stopped after smoke validation.
- Browser screenshots: `NOT RUN` — no browser-level visual inspection was available in this environment.
- Scope safety: `PASS` — no M4, M6, M7 scoring, extractor, taxonomy, or production DuckDB changes made by M8-02.

## M8-04 validation

- Graph projection: `PASS` — all rendered nodes and edge endpoints are source-backed; only `HAS_SKILL`, required, and preferred evidence edges are emitted.
- Projection determinism/bounds: `PASS` — repeated projection is identical and the default view is capped at 24 jobs plus candidate/skills.
- Focused tests: `PASS` — dashboard and graph projection tests passed 9/9.
- Streamlit AppTest: `PASS` — default network destination loaded with zero exceptions.
- Dependency audit: `PASS` — NetworkX 3.7 and Streamlit 1.65.0 available; no graph package installed or required.
- Browser interaction: `NOT RUN` — no browser-level inspection tool was available; SVG interaction was validated by code review and AppTest startup.
- Full regression: `PASS` — 41/41 unittest tests completed successfully with the approved environment and required Spark socket permissions.
- Localhost startup: `PASS` — Streamlit server started on port 8503 and stopped after smoke validation.

## M8-MIGRATE-01 validation

- Environment inspection: `PASS` — Node/npm absence, Python environment, installed packages, memory, project configuration, and frontend-directory status recorded.
- Reusable interface audit: `PASS` — M5 graph, M6 artifact, M7 evidence loader/matching APIs, and current dashboard projection inspected.
- Scope safety: `PASS` — no packages installed, no code or data artifacts modified, and production DuckDB remained read-only.
- Deliverable: `PASS` — `docs/M8_MIGRATION_PLAN.md` contains API contracts, graph strategy, frontend structure, staged plan, risks, and next step.

## M8-MIGRATE-02 validation

- FastAPI installation: `PASS` — FastAPI 0.115.6, Pydantic 2.10.6, HTTPX 0.28.1; Uvicorn 0.54.0 retained.
- Focused API/graph tests: `PASS` — 11/11, covering schemas, pagination, filters, errors, provenance, null insufficient scores, graph edge classes, and database hash behavior.
- Live API smoke: `PASS` — all eight required endpoints returned successful responses through Uvicorn, including candidate/job matching and graph neighborhood requests.
- Full regression: `PASS` — 43/43 unittest tests with approved Spark permissions.
- Database integrity: `PASS` — production DuckDB SHA-256 identical before and after validation; all backend connections are read-only.
- Streamlit retirement: `PASS` — confirmed dashboard-only files removed and Streamlit uninstalled; M1–M7 and shared graph modules preserved.
- `git diff --check`: `PASS`.

## M8-MIGRATE-03 validation

- Node/npm: `PASS` — Node.js 22.14.0 and npm 10.9.2 installed user-scoped; no system-wide installation.
- Dependency lock: `PASS` — `frontend/package-lock.json` generated and `node_modules`/`.next` ignored.
- TypeScript: `PASS` — `tsc --noEmit` completed successfully.
- ESLint: `PASS` — frontend source lint completed successfully.
- Routes: `PARTIAL` — `/network`, `/matches`, and `/insights` served successfully from an earlier completed build; final rebuild after the rewrite change did not complete.
- Production build: `BLOCKED` — optimized compilation terminated/timed out under WSL memory pressure; approximately 33 MiB free and 854 MiB swap used at the final attempt.
- Backend regression: `PASS` — M8-MIGRATE-02 backend regression remains 43/43; frontend changes do not alter Python backend code.
- Browser automation: `NOT RUN` — no browser automation tool was available.

## M8-MIGRATE-03A validation — 2026-10-13

- Resources: 3.5 GiB RAM, 1.0 GiB swap with 914 MiB used; 57 GiB free on `/mnt/c` and 948 GiB free on `/tmp`. No stale TalentGraph Node/Next process was present.
- Toolchain/command: Node `v22.14.0`, npm `10.9.2`, Next `15.2.4`; `npm run build` from `frontend/` using the pinned lockfile.
- Fresh `/mnt/c` build: initial telemetry write failed with `EROFS` before compilation (exit 1, 22.43 s, peak RSS 126,512 KiB). With per-process `NEXT_TELEMETRY_DISABLED=1`, compilation passed but the 180-second bound expired during lint/type checking.
- Frontend-only `/tmp` build: no production data or DuckDB copied; the 240-second bound expired during optimized compilation without OOM evidence or a lingering process.
- TypeScript and ESLint: `PASS`; Python regression: `ENVIRONMENT-BLOCKED` by the known Spark socket-permission error. Production DuckDB hash observed unchanged as `b2314da8faf5aea8ad8643a1790c96ce7b116bb0ce544473883f45e37f889160`.
- Cleanup: only disposable `frontend/.next` was removed; no stale process was terminated. M8-MIGRATE-03 remains `IN_PROGRESS`.

## M8-MIGRATE-03B validation — 2026-10-13

- Environment: `free -h` reported 3.8 GiB RAM, `swapon --show` reported a 3.0 GiB `/dev/sdc` swap device with 0 B used, and `nproc` reported 2. Node `v22.14.0`; npm `10.9.2`.
- Production build: `PASS` — `NEXT_TELEMETRY_DISABLED=1 npm run build` completed on the first controlled attempt; exit 0, elapsed 2:55.42, peak RSS 385,316 KiB (~376 MiB), zero swap operations. Next.js reported successful compilation, lint/type checks, static generation 7/7, and trace collection.
- TypeScript: `PASS` — `npm run typecheck`.
- ESLint: `PASS` — `npm run lint`.
- Frontend routes: `PASS` — production server returned HTTP 200 for `/network`, `/matches`, and `/insights`; `/` returned HTTP 307 with `Location: /network`.
- FastAPI integration: `PASS` — frontend rewrite returned HTTP 200 and live health, overview, jobs, and candidates payloads. Responses showed 1,500 jobs, 300 synthetic candidates, and read-only database status; no fabricated match result was used.
- Python regression: `PASS` — elevated approved WSL execution completed 43/43 tests in 42.494 seconds. Spark emitted only non-fatal hostname/native-library/plan-size warnings.
- DuckDB integrity: `PASS` — SHA-256 remained `b2314da8faf5aea8ad8643a1790c96ce7b116bb0ce544473883f45e37f889160`; no production write was performed.
- Scope: `PASS` — no dependency install, global WSL change, application architecture change, M1–M7 logic change, or M8-MIGRATE-04/React Flow work.

## M8-MIGRATE-04 validation — 2026-10-13

- Dependency: `PASS` — `@xyflow/react` 12.12.0 installed and locked; no other visualization or UI dependency added.
- Graph API mapping: `PASS` — typed `GraphNeighborhood`, `GraphNode`, and `GraphEdge` interfaces match the FastAPI schema. Smoke response contained candidate/competency nodes and `HAS_SKILL` edges with all endpoints present in the node set.
- Graph behavior: `PASS` by code/build validation — deterministic stable-ID columns, bounded limit 35, hops 1–2, lazy expansion, selection highlighting, reset/clear, graph search, fit-to-view, minimap, pan/zoom controls, and candidate/job matches links.
- Evidence integrity: `PASS` — frontend renders only API-provided nodes and relationships; required and preferred relationships remain distinct, and no unsupported evidence is promoted.
- Focused backend tests: `PASS` — API and projection tests 11/11.
- TypeScript/ESLint: `PASS`.
- Production build: `PASS` — exit 0, elapsed 4:28.06, peak RSS 375,040 KiB, zero swap operations.
- Full Python regression: `PASS` — 43/43 tests.
- DuckDB integrity: `PASS` — SHA-256 `b2314da8faf5aea8ad8643a1790c96ce7b116bb0ce544473883f45e37f889160` unchanged.
- Browser interaction: `NOT RUN` — no browser automation tool was available; actual visual node selection, zoom, expansion, and navigation remain manual follow-up checks.

## M8-MIGRATE-04B validation — 2026-10-13

- Readability/UI: `PASS` by code review and build validation — primary graph labels use dark text on light cards; selected nodes have a clear outline; controls, details, and disabled states retain readable contrast; raw IDs and provenance are hidden under Evidence details.
- Simplification: `PASS` — compact Explore Network heading, reduced introduction, candidate/search/expand/reset toolbar, no redundant node subtitles, no generic competency description, and no primary-view technical enums.
- Details: `PASS` — candidates show role family and technical skills; jobs show company and supported required/preferred skills; candidate/job match actions remain available.
- TypeScript: `PASS`; ESLint: `PASS`; production build: `PASS`.
- Full regression: `PASS` — 43/43 tests. DuckDB checksum unchanged: `b2314da8faf5aea8ad8643a1790c96ce7b116bb0ce544473883f45e37f889160`.
- No source data, matching algorithms, dependencies, or system configuration were changed.
# M8-MIGRATE-04D validation

- Browser automation/Chromium: unavailable in the repository environment; exact manual viewport checks remain required at 1366x768 and 1920x1080 in light and dark modes.
- Live API response: PASS — candidate `synthetic:candidate:000001` returned valid scored comparisons with matched required skills and no invented score for insufficient evidence.
- TypeScript: PASS (running with the repository Node toolchain).
- ESLint: PASS (running with the repository Node toolchain).
- Production build: PASS — Next.js compiled, linted, type-checked, generated all seven static pages, and exited 0.
- `git diff --check`: PASS.

## M8-FRONTEND-FINAL-01 validation — 2026-10-13

- TypeScript: PASS — `npm run typecheck` (explicit check after functional code changes).
- ESLint: PASS — `npm run lint`; no frontend test script exists in `frontend/package.json`.
- Production build: PASS — final `NEXT_TELEMETRY_DISABLED=1 npm run build` exited 0 after the graph candidate/reset fix and generated all seven static pages.
- FastAPI: PASS — `PYTHONPATH=src ... python -m unittest tests.test_api`, 9/9 tests. New fixture confirms distinct job/skill counting, required+preferred deduplication, and exclusion of non-scoring evidence.
- The new endpoint's route registration and handler were checked directly. An additional in-process HTTP smoke attempt stalled in the restricted runner's AnyIO portal and was stopped; this is not an HTTP-level pass.
- Live read-only API functions: PASS — 1,500 jobs, 300 synthetic candidates, coverage 80/7/44/1,369 (sum 1,500), 1,420 lacking required evidence; top job frequencies SQL 42, Python 35. No invented chart counts.
- `git diff --check`: PASS. Whitespace scan of new frontend/API source: no trailing whitespace. Production DuckDB SHA-256: `663dbe12cde5231e4d1dc65a880041ecaffe840469a0efcf4a0c8db5202dc397`, unchanged from the pre-task value.
- Code-level checks: candidate ID is passed from selected graph candidate to `/matches`; graph selection stays bound to the candidate after expanding skill/job roots and Reset returns to that candidate; graph search leaves the candidate selector populated. Graph edges have accessible relationship labels but no floating text; Show N is an auto-width themed button below the graph; match selection/filter fallback and theme-aware scroll containers remain. These are not browser interaction tests.
- Browser verification: NOT RUN — no Chromium/Playwright executable or browser automation tool was available. Manual checks remain for light/dark visuals at 1366×768 and 1920×1080, persistence/system theme, graph and match interactions, chart tooltips, overflow, focus/contrast, and console/hydration warnings.
