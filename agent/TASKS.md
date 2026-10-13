# Tasks

Statuses: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`.

| ID | Milestone / task | Priority | Dependencies | Acceptance criteria | Validation | Status |
|---|---|---|---|---|---|---|
| M0-01 | Verify Python, Java, Git, WSL2, Ubuntu, RAM, disk | High | None | Findings recorded with access limitations | Environment checks | DONE |
| M0-02 | Establish repository layout and documentation workflow | High | M0-01 | Source-of-truth Markdown exists | File and Git checks | DONE |
| M1-01 | Verify dataset schema, license, and bounded sample plan | High | M0 | Metadata-verified source and license; proposed contracts and deterministic sample plan documented; download-time uncertainties explicit | Manual metadata review; documentation checks | DONE |
| M1-02 | Define raw/curated schemas and synthetic generator contract | High | M1-01 | Physical archive inspected; schemas and bounded sample validated | Archive, sampling, and schema tests | DONE |
| M2-01 | Build bounded PySpark ingestion and normalization | High | M1-02 | Valid and malformed records handled | Spark smoke tests | DONE |
| M2-02 | Investigate and fix CSV record-count discrepancy | High | M2-01 | Logical CSV count matches Spark output; parser artifacts eliminated | CSV framing and Spark comparison tests | DONE |
| M3-01 | Build DuckDB models and SQL tests | High | M2-01 | Facts/dimensions have tested grain and keys | DuckDB tests | DONE |
| M4-01 | Implement controlled skill taxonomy and alignment | High | M1-02, M3-01 | Canonical IDs, aliases, provenance, confidence | Alignment tests | DONE |
| M5-01 | Implement deterministic entity resolution | High | M4-01 | Thresholds, tie-breaks, unknown path, reasons | Resolution tests | DONE |
| ENV-02 | Fix PySpark Python worker version mismatch | High | M2-01 | Driver and workers use approved Python; regression suite passes | M2 and full tests | DONE |
| M6-01 | Build graph and explainable matching | High | M3-01, M5-01 | Relationships and scores are reproducible | Graph/match tests | DONE |
| M7-01 | Add incremental and idempotent processing | High | M2-01, M6-01 | Repeated runs do not duplicate data | Rerun tests | DONE |
| QA-FIX-01 | Semantic taxonomy and evidence-based extraction | High | QA-01, M4-01 | Existing taxonomy classified; description evidence extracted with provenance and bounded quality checks | Extraction tests and regression suite | DONE |
| QA-FIX-02 | Validate competency extraction against real descriptions | High | QA-FIX-01 | Deterministic stratified review sample and failure-mode audit; no unverified accuracy claims | Review artifact and bounded diagnostics | DONE |
| QA-FIX-03 | Prepare human skill-evidence review worksheet | High | QA-FIX-02 | Compact 25-record worksheet with blank human-label fields and reproducible selection | CSV validation and repeat build | DONE |
| QA-FIX-04 | Improve requirement classification | High | QA-FIX-03 | Separate detection/classification with explicit required, preferred, mentioned, negated, and ambiguous classes | Phrase regression and full suite | DONE |
| M8-01 | Add data quality and observability checks | High | M2-01 | Failures and metrics are actionable | Quality tests | TODO |
| M9-01 | Create Airflow DAGs in WSL2 | High | M2-01–M8-01 | DAG loads and tasks are bounded | DAG validation | TODO |
| M10-01 | Build Streamlit demonstration | Medium | M3-01, M6-01 | Dashboard starts and displays verified outputs | Smoke test | TODO |
| M11-01 | Regression, documentation, and release readiness | High | M0–M10 | Demo runbook and regression suite complete | Full validation | TODO |
