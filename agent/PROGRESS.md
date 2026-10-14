# Progress

## 2026-10-13 — M8-RELEASE-02 publication preparation

- Confirmed `main` and the intended GitHub `origin`; staged the reviewed public source, docs, requirements, frontend lockfile, screenshots, and background while leaving ignored private/data/build material out.
- The owner confirmed checking light mode and a narrow viewport. They observed that light mode looks somewhat unusual but accept it because dark mode is their intended usage. This caveat remains visible rather than being described as a visual pass.
- Fixed one extra blank line at the end of `api_models.py` found by `git diff --cached --check`; final staged security and content review follows before publication.
- Published release commit `78f9eda0ddf2184bc16eaaa977f21d3b4d381d81` to `origin/main` with the owner's GitHub username and no-reply email. The first push lacked HTTPS credentials; an authenticated GitHub CLI session enabled a command-scoped credential helper, and the non-force retry succeeded. Remote `main` was verified at the release hash.

## 2026-10-13 — M8-RELEASE-01 GitHub readiness audit

- Reviewed the 96 tracked or non-ignored public candidate files, README, documentation, assets, dependency locks, frontend, API, and database integrity. Added narrow ignore rules for DuckDB files, TypeScript build metadata, and the private interview guide; no files were staged or published.
- Follow-up: the user explicitly confirmed permission to use the artwork in this repository. The earlier licensing concern is resolved on that user-provided basis; no separate license document was inspected. All four screenshots contain the backdrop.
- Python regression, TypeScript, ESLint, production build, and seven representative read-only API routes passed. Dark-mode screenshot captures exist; a fresh light-mode browser review was not performed in this audit.

## 2026-10-13 — M8-DOCS-02 application screenshots

- Copied the four user-provided local PNG screenshots without editing them into `docs/screenshots/`, with names for candidate network, Python skill network, candidate–job comparison, and evidence Insights.
- Added a clickable four-image README gallery with accurate captions and a note that the visible **N** badge is the Next.js development indicator.

## 2026-10-13 — M8-DOCS-01 engineering documentation

- Added concise engineering overview, detailed pipeline and quality history, limitations/future work, and verified technology versions. README now links to the documents and root Python requirements.
- Pinned direct Python dependencies while reusing `requirements-backend.txt`; added explanatory comments to pipeline, evidence, matching, API, and frontend source without changing executable statements.
- Marked original Streamlit/Airflow architecture notes as historical. Documented the unresolved source-row mapping and corrected the DuckDB checksum path distinction without altering earlier validation records.
- Verified 24 local Markdown links, eight installed requirement pins, Python syntax, frontend TypeScript/ESLint, and a 44-test Python regression outside the restricted shell. Both known DuckDB hashes remained unchanged.

## 2026-10-13 — M8-VISUAL-02 sidebar polish

- Applied the same local rocket artwork behind a theme-specific sidebar wash to connect the navigation visually with the main area.
- Added a restrained active-route highlight and `aria-current="page"` to sidebar navigation. No backend, data, or matching files changed.

## 2026-10-13 — M8-VISUAL-01 rocket backdrop

- Removed page copy, navigation, buttons, and incidental lettering from the user-provided scene with image editing. Saved the clean illustration as `frontend/public/rocket-background.png`.
- Added subdued light/dark image washes to the main content area and network canvas. No data, API, matching, or database files changed.

## 2026-10-13 — M8-POLISH-04 interaction refinement

- Styled the graph's progressive job-discovery button directly; its prior white stretched appearance came from missing `.show-more` styling combined with default flex-item stretching and browser button defaults.
- The compact control now has theme-aware colors, hover/focus treatment, centered placement below the graph, and a remaining-count label while retaining the same bounded increment behavior.
- Discover Matches keeps a selected visible job when filters change, selects the first remaining result if the current job is filtered out, and presents results as native keyboard-operable buttons with visible focus/selected states.
- Kept independent list and detail scrolling, existing sort/search/filter behavior, and evidence semantics.

## 2026-10-13 — M8-POLISH-03 split comparison workspace

- Replaced expandable rows with a responsive split view: selectable result list on the left and selected comparison details on the right.
- Organized detail panel into overview, required skills with matched/missing columns, preferred skills, and evidence/limitations.
- Removed the rendered `preferred` edge text label from React Flow edges; retained accessible `ariaLabel` relationship descriptions, dashed preferred edges, solid required edges, and the existing legend.
- Preserved candidate selection, search, sorting, comparable-only filter, scoring semantics, and API contract.

## 2026-10-13 — M8-POLISH-02 premium SaaS UI

- Selected Lato as the preferred typography family with `Segoe UI`/Arial fallbacks because no licensed Avenir or local Lato font files were available; no font dependency or network loading was added.
- Added shared role-family presentation labels such as `Data Engineering`, `Software Engineering`, and `Cloud & Platform` across Network and Matches.
- Redesigned Discover Matches with a compact filter toolbar, candidate context, dark comparison rows, primary observed-skill counts, skill chips, evidence status, and expandable limitations.
- Applied shared typography, control sizing, card hierarchy, and responsive styling to Network, Matches, and Insights without changing graph or matching semantics.

## 2026-10-13 — M8-MIGRATE-06 final verification

- Audited all three Next.js destinations and found/fixed one React hook-order defect in Discover Matches: filtering/sorting memoization now runs before loading/error returns.
- Corrected Insights to distinguish required, preferred-only, non-required-only, and no-eligible-evidence groups.
- Added current public-safe README startup and usage documentation.
- Verified FastAPI health, overview, jobs, job detail, candidates, candidate detail, matches, and graph neighborhood behavior; representative candidates `000001`, `000076`, and `000226` returned real comparisons.
- Frontend typecheck, ESLint, and production build passed. Full Python regression reached 42/43 because the existing Spark framing test is blocked by restricted-shell socket permissions.

## 2026-10-13 — M8-MIGRATE-05 matches UX refinement

- Replaced oversized match cards with compact expandable rows emphasizing observed required-skill counts; percentages are secondary and insufficient evidence has no numeric score.
- Added title/company search, observed-overlap and observed-required-skill sorting, and an explicit comparable-only filter.
- Added theme-aware native scrollbar styling for page, matches results, and details panels without a custom dependency; Explore Network behavior was preserved.

## 2026-10-13 — M8-MIGRATE-04D viewport and matches repair

- Diagnosed graph overflow as fixed viewport-height/minimum sizing competing with the page heading and toolbar; constrained the workspace with flex sizing and `min-height: 0`.
- Replaced the `/matches` placeholder with candidate selection, URL candidate context, real `/api/matches` requests, evidence-aware result cards, and truthful insufficient-evidence display.
- Live backend inspection returned valid candidate comparisons with observed matched/missing required competencies; no matching algorithm changes were made.

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

## 2026-10-13 — QA-FIX-05 reconciliation

- Reconciled all 25 records from `data/processed/qa_fix03_human_review.csv` against the QA-FIX-04 extractor and wrote ignored `data/processed/qa_fix05_reconciliation.csv`.
- Preserved `confirmed_label` and `reviewer_rationale` exactly; all remain blank, so no AI-generated classification was promoted to human ground truth.
- Validation found 25 unique worksheet keys, 20 classifier changes, and 25 records still requiring human review. A separate summary is in `docs/QA_FIX05_RECONCILIATION_SUMMARY.md`.
- Targeted QA extraction tests passed 6/6; full regression passed 24/24 with the approved local Spark environment. Production DuckDB was not opened or modified.
- Refactored the reconciliation implementation into a 96-line orchestration module plus a 37-line helper module; regenerated artifacts remained stable and no extractor behavior changed.

## 2026-10-13 — QA-FIX-06 evidence preservation and human-label import

- Imported exactly 25 user-reviewed records from `data/processed/qa_fix06_human_labels.csv` without coercing labels or importing AI proposals as confirmed truth.
- Produced `data/processed/qa_fix06_clean_evidence_review.csv` with complete original descriptions, deterministic UTF-8 SHA-256 hashes, source row locations, original/cleaned evidence, bounded previews, model classifications, raw human labels, and unresolved flags.
- Preserved complete descriptions for 19 unique jobs, including all five no-dictionary-term cases. Seven evidence excerpts received display-only cleaning; source text remains unchanged.
- Human labels: required 15, preferred 3, incidental 1, ambiguous 5, unresolved `required/preferred` 1. There are 13 model/human classification disagreements and 6 unresolved review cases.
- Added focused QA-FIX-06 tests; focused tests passed 8/8 and the full regression suite passed 26/26. Production DuckDB and M6/M7 were not modified.

## 2026-10-13 — QA-FIX-07 final labels and extraction evaluation

- Created `data/processed/qa_fix07_final_review.csv` and `docs/QA_FIX07_EVALUATION.md` from the complete QA-FIX-06 evidence artifact.
- Preserved the raw Java label `required/preferred` and resolved it to `preferred` because the full description presents Java as an alternative among “two or more development languages such as Java or Python.”
- Final labels: required 15, preferred 4, incidental 1, ambiguous 5; 5 no-dictionary cases remain unresolved review inputs.
- The comparable five-class subset contains 17 records. Supported metrics are documented with exclusions for five `no_candidate_term` and three `mentioned` predictions; the selected 25-record sample is not a production accuracy estimate.
- Full-description review identified evidence-backed taxonomy coverage suggestions including SaaS, Foundation software, SharePoint, WMIS, and sales-funnel/go-to-market concepts. No new competencies or human labels were added.
- Focused QA-FIX-07 tests passed 10/10; full regression passed 28/28. Production DuckDB, extractor, taxonomy, M6, and M7 were not modified.

## 2026-10-13 — M6-REFINE-01 competency-based synthetic candidates

- Replaced random full-taxonomy sampling with four explicit role families: data engineering, analytics, software engineering, and cloud/platform engineering.
- Generated 300 deterministic synthetic candidates using seed `20261012`: 75 per role family; junior 100, mid 120, senior 80.
- Candidate bridges contain 1,527 relationships across 14 supported technical competencies. Business, occupational, industry, operations, and other category labels are excluded.
- Preserved M7 interfaces (`candidate_key`, `skills`, and candidate-skill keys); artifact schema is now `m6-v2` and adds `role_family`. M7 scoring was not changed.
- Focused M6/M7 tests passed 5/5 with the expanded assertions; full regression passed 28/28. Production DuckDB was read-only and M7 scoring was unchanged.

## 2026-10-13 — M7-REFINE-01 evidence-aware matching

- Replaced category-based bridge matching with a read-only evidence loader over `data/processed/job_competency_evidence.json`; only canonical technical, cloud, and data-engineering competencies are eligible.
- Required evidence is primary; preferred evidence is separate; mentioned, negated, ambiguous, broad, and industry evidence are excluded. Results now expose provenance, counts, missing skills, nullable overlap, and evidence status.
- Current inventory: 101 jobs with eligible required evidence, 0 preferred-only jobs, and 1,399 insufficient-evidence jobs out of 1,500. This reflects the available artifact, not absence of skills.
- Preserved M7 public function names and candidate/job identifiers. M6 and production DuckDB were unchanged.
- Focused M6/M7 tests passed 6/6; full regression passed 29/29.

## 2026-10-13 — M7-REFINE-02 canonical evidence pipeline

- Root cause confirmed: M7 consumed stale QA-FIX-01 evidence (`403` relationships, `167` eligible across `101` jobs) and treated legacy requirement-context rows as required; the complete QA-FIX-04 output existed only as a diagnostic artifact.
- Rebuilt `data/processed/job_competency_evidence_qa_fix04.json` directly from the unchanged extractor over all 1,500 sampled descriptions: 582 relationships across 372 jobs, with all five classifications, evidence text, source hashes, locations, rules, and versions.
- Canonical eligible coverage: 80 required jobs, 7 preferred-only jobs, 44 non-required mention/negated/ambiguous jobs without requirements, and 1,369 with no eligible technical evidence.
- M7 loader now validates `m7-evidence-v2`, `qa-fix-04-v1`, and provenance fields and fails closed on stale artifacts. Human review remains separate; 13 QA-FIX-07 comparable disagreements are preserved transparently.
- Focused evidence/M7 tests passed 8/8; full regression passed 32/32. Production DuckDB, extractor, taxonomy, and M6 were unchanged.

## 2026-10-13 — M8-01 Streamlit dashboard

- Resolved the prior dependency blocker: Streamlit 1.65.0 imports successfully in the approved TalentGraph virtual environment.
- Built `app.py` plus focused `dashboard_data.py` and `dashboard_views.py` modules. The dashboard provides Overview, Candidate Explorer, Job Explorer, and Match Explanation sections using the current M6 artifact and M7 APIs.
- Added read-only artifact validation, immutable caching, neutral missing-company handling, empty-result handling, non-scoring evidence display, and explicit limited/insufficient evidence messaging.
- Focused dashboard/M7 tests passed 11/11; full regression passed 37/37. Elevated headless Streamlit startup smoke reached localhost:8501 successfully. No browser screenshot was captured.
- Production DuckDB, M4, M6, M7 scoring, extractor, and taxonomy were not modified.

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

## 2026-10-13 — M8-02 product experience redesign

- Reorganized Streamlit into Overview, Explore Jobs, Explore Candidates, Compare Skills, and Data Quality destinations.
- Added readable search/filter flows, neutral missing-company handling, evidence-status definitions, provenance details, and explicit overlap numerator/denominator context.
- Preserved read-only M6 and `m7-evidence-v2` loading and delegated scoring to the existing M7 API.
- Focused dashboard tests passed 6/6. AppTest completed with zero exceptions; full unittest regression completed successfully with elevated Spark permissions. Localhost headless startup was verified; no browser screenshot was captured.

## 2026-10-13 — M8-04 network-first product redesign

- Replaced the five-page dashboard navigation with Explore Network, Discover Matches, and Insights.
- Added a deterministic bounded projection from synthetic candidate skills and canonical required/preferred evidence. Legacy M4 category edges and non-scoring evidence are excluded.
- Added a dependency-free SVG network surface with client-side pan, zoom, and node highlighting, plus Streamlit node inspection and comparison context.
- No new dependency, data pipeline, scoring, taxonomy, extractor, or DuckDB change was made.

## 2026-10-13 — M8-MIGRATE-01 migration audit

- Audited the local environment: Node.js/npm and FastAPI are absent; Uvicorn 0.54.0, DuckDB 1.5.6, NetworkX 3.7, and Streamlit 1.65.0 are available. No frontend directory or package configuration exists.
- Mapped reusable M7 matching/evidence interfaces, M6 candidate artifacts, M5 graph lineage, and the bounded network projection.
- Documented version proposals, API contracts, React Flow architecture, graph semantics, staged migration risks, and the exact next step in `docs/M8_MIGRATION_PLAN.md`.
- No packages, application code, data artifacts, AGENTS.md, taxonomy, extractor, matching logic, or production DuckDB were modified.

## 2026-10-13 — M8-MIGRATE-02 FastAPI backend and Streamlit retirement

- Installed FastAPI 0.115.6, Pydantic 2.10.6, and HTTPX 0.28.1 in the approved environment; Uvicorn 0.54.0 was retained.
- Added typed read-only API modules: `api.py`, `api_models.py`, `api_service.py`, `api_store.py`, and `api_data.py`, plus `docs/M8_BACKEND.md` and `requirements-backend.txt`.
- Implemented health, overview, job, candidate, matching, and graph-neighborhood endpoints using existing M6 artifacts, M7 evidence, and M7 ranking functions.
- Removed confirmed Streamlit-only files and uninstalled Streamlit. Preserved M1–M7 modules, artifacts, production DuckDB, and shared network projection.
- Focused API/graph tests passed 11/11; full unittest regression passed 43/43; live HTTP smoke covered all eight endpoints; DuckDB SHA-256 was unchanged; `git diff --check` passed.

## 2026-10-13 — M8-MIGRATE-03 frontend foundation

- Installed user-scoped Node.js 22.14.0 and npm 10.9.2 under ignored `.tools/`; created pinned `frontend/package.json` and `package-lock.json`.
- Added Next.js App Router shell, `/network`, `/matches`, and `/insights` routes, typed API client, loading/error states, responsive design tokens, and local FastAPI rewrite proxy.
- TypeScript and ESLint passed. Production build attempts were terminated during optimized compilation after available memory fell to approximately 33 MiB and swap was nearly exhausted; task remains in progress pending a successful build in a less constrained environment.

## 2026-10-13 — M8-MIGRATE-03A build diagnosis

- Fresh diagnostics found 3.5 GiB RAM, 1.0 GiB swap (914 MiB used), 57 GiB free on `/mnt/c`, and 948 GiB free on `/tmp`; no stale TalentGraph development process was running.
- Removed only `frontend/.next`. The first controlled build exposed a restricted-runner Next telemetry `EROFS`; disabling telemetry per process allowed `/mnt/c` compilation but the 180-second bound expired during lint/type checking.
- A frontend-only `/tmp` copy also exceeded its 240-second bound during optimized compilation. Neither run emitted OOM evidence or left a Node process. TypeScript and ESLint pass; Python regression remains blocked by the known restricted Spark socket error. No global WSL setting changed and M8-MIGRATE-04 was not started.

## 2026-10-13 — M8-MIGRATE-03B production build verification COMPLETE

- Effective WSL resources: 3.8 GiB visible RAM, 3.0 GiB swap, and 2 CPUs. Node.js 22.14.0 and npm 10.9.2 matched the approved toolchain.
- First controlled `NEXT_TELEMETRY_DISABLED=1 npm run build` passed with exit 0 in 2:55.42. Next.js 15.2.4 compiled, linted, type-checked, generated seven static pages, and finalized traces. Peak RSS was 385,316 KiB (~376 MiB); `/usr/bin/time -v` reported zero swaps.
- Explicit typecheck and ESLint passed. Elevated production smoke returned 200 for `/network`, `/matches`, and `/insights`; `/` returned 307 to `/network`.
- The frontend rewrite returned live FastAPI health, overview, jobs, and candidates data. FastAPI regression passed 43/43. The production DuckDB checksum remained `b2314da8faf5aea8ad8643a1790c96ce7b116bb0ce544473883f45e37f889160`.
- Only disposable `frontend/.next` was removed before the build. No dependencies, global WSL settings, production DuckDB contents, M1–M7 logic, or React Flow code were changed. M8-MIGRATE-04 was not started.

## 2026-10-13 — M8-MIGRATE-04 interactive graph COMPLETE

- Added approved `@xyflow/react` `12.12.0` to the frontend manifest and lockfile. Replaced the network placeholder with a client-side React Flow explorer using the existing `/api/graph/neighborhood` contract.
- Added typed graph node/edge interfaces, deterministic candidate-first layout, bounded `hops=1|2` expansion, candidate/skill/job node styles, solid required versus dashed preferred edges, selection highlighting, graph search, reset/clear controls, contextual details, and candidate/job links to `/matches`.
- Graph API smoke returned 5 nodes and 4 `HAS_SKILL` edges for candidate `synthetic:candidate:000001`; every edge endpoint was source-backed. Focused API/projection tests passed 11/11.
- Frontend typecheck and ESLint passed. Production build passed with exit 0 in 4:28.06; peak RSS was 375,040 KiB and swap operations were zero. Full Python regression passed 43/43. DuckDB checksum remained unchanged.
- Browser automation was unavailable, so actual click/zoom/expansion behavior was not browser-verified. No backend, M1–M7 logic, artifact, or production database changes were made.

## 2026-10-13 — M8-MIGRATE-04B readability pass COMPLETE

- Simplified `/network` to a compact “Explore Network” heading and candidate/search/expand/reset controls. Removed redundant workspace copy, node subtitles, clear control, raw IDs from the primary details view, and generic competency text.
- Improved contrast with dark text on light graph cards, stronger muted-text colors, obvious selected outlines, readable disabled controls, and a compact contextual panel. Candidate skills and job supported required/preferred skills are shown by readable names; provenance remains in an optional disclosure.
- TypeScript, ESLint, and production build passed. Full Python regression passed 43/43. Production DuckDB checksum remained `b2314da8faf5aea8ad8643a1790c96ce7b116bb0ce544473883f45e37f889160`.

## 2026-10-13 — M8-FRONTEND-FINAL-01 frontend audit and Insights

- Audited all three Next.js routes, shared UI, theme initialization, API contracts, and existing documentation. Root light-mode defect: default `--match-*` tokens were dark navy, reinforced by hardcoded pale comparison text and layered CSS overrides. Consolidated light/dark tokens and styles without changing hydration strategy.
- Preserved Discover Matches split view, filters, sorting, candidate context, independent scrolling, and evidence-aware semantics. Removed duplicate overview/repeated preferred-empty content and kept technical details in the evidence disclosure. Removed a job-node link whose query parameter was ignored by Discover Matches; candidate links still carry the selected ID.
- Added four Insights KPIs, a four-group evidence donut, and an eight-skill job-frequency chart using a new read-only API aggregate over validated required/preferred M7 evidence. No matching, extraction, graph relationship, candidate, artifact, or DuckDB data was changed.
- Consolidated theme-aware graph/grid/minimap, buttons, scrollbars, focus states, and chart styles; removed unused frontend helpers and generic copy. Fixed graph candidate selection/reset after expanding a noncandidate root and kept search from emptying the candidate selector. Documented chart definitions and remaining manual browser checks in `docs/M8_FRONTEND.md` and `docs/M8_BACKEND.md`.
