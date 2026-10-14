# Error Log

## 2026-10-13 — M8-RELEASE-02 GitHub authentication boundary

- The reviewed local release commit was created with the owner's GitHub username and no-reply email after correcting an automatically generated laptop-hostname identity on the unpublished commit.
- `git push origin main` did not publish: HTTPS Git reported that it could not read a username. The GitHub CLI is absent and no SSH authentication agent is available. The remote remained at its prior commit; GitHub connection or local authentication is required before retrying the push.
- Resolved in follow-up: GitHub CLI was installed and authenticated in WSL; the unrestricted `gh auth status` check passed. A command-scoped CLI credential helper allowed the non-force push, and remote `main` matched the release commit afterward. The earlier failure was an authentication boundary, not a repository-content failure.

## 2026-10-13 — M8-RELEASE-01 release blockers and verification limits

- Initial audit concern: the source scene was a Phenom website screenshot and permission had not yet been established. Follow-up: the user explicitly confirmed permission for this repository's use of the artwork; this is no longer a release blocker. No separate license document was inspected.
- A restricted-shell FastAPI test-client request stalled after importing the app; the approved unrestricted retry returned HTTP 200 for all seven representative read-only routes. This was an environment boundary, not an observed API failure.
- No fresh browser-based light-theme or responsive screenshot review was available in this audit. Clean-machine startup remains unverified because the API depends on local ignored artifacts and a fixed database path, as disclosed publicly.

## 2026-10-13 — M8-DOCS-01 documentation audit

- The restricted-shell regression run had the previously recorded Spark Java socket startup error; an approved unrestricted rerun passed 44/44 tests. No new application defect was found.
- Source-row provenance remains unresolved: M2 stores a Spark processing index for sampled CSV rows, while the evidence artifact numbers archive CSV records. Their direct equivalence has not been validated.
- The exact published version of the local source archive and a clean-machine installation remain unverified. Earlier M8 checksum labels remain historically inaccurate; the separate file paths and hashes are documented without rewriting those records.

## 2026-10-13 — M8-POLISH-04 browser verification boundary

- Browser automation is unavailable, so rendered button appearance, pointer/keyboard selection, and viewport scrolling require manual verification. Automated frontend checks are running/completed as recorded in validation.

## 2026-10-13 — M8-POLISH-03 browser verification boundary

- No browser automation executable is available; split selection, responsive stacking, and rendered graph label appearance require manual browser verification.

## 2026-10-13 — M8-POLISH-02 environment note

- Avenir and Lato font files were not present in the local font inventory. The UI uses a Lato-first family with system fallbacks; no unlicensed font was bundled or downloaded.

## 2026-10-13 — M8-MIGRATE-06 release verification

- Browser automation remains unavailable; exact manual browser checks are listed in `agent/VALIDATION.md`.
- Full regression remains 42/43 in the restricted shell because Spark cannot create a Java network-interface socket. This is the same environment-only blocker recorded previously; no test was weakened or removed.

## 2026-10-13 — M8-MIGRATE-05A theme hydration

- Root cause confirmed: the inline theme initializer mutates the root `data-theme` attribute before hydration. This is intentional for no-flash behavior, but differed from server HTML.
- Resolved with a narrowly scoped `suppressHydrationWarning` on `<html>`; no broad suppression or client-only rendering was introduced.

## 2026-10-13 — M8-MIGRATE-05 validation environment

- Full Python regression reached 42/43 tests; the existing Spark framing test could not initialize because this restricted shell denies Java network-interface socket creation. No frontend or matching failure was observed.

## 2026-10-13 — M8-MIGRATE-04D browser verification boundary

- Playwright, Puppeteer, and accessible Chromium were not found in the current environment. No dependency or browser binary was installed without approval.

## 2026-10-12 — QA-FIX-01 extraction

- No extraction logic failures remain after adding `requires` to the explicit requirement context and rerunning the fixture.
- A full regression diagnostic rerun was blocked by the execution environment: Spark failed before test code with `java.net.SocketException: Operation not permitted (Socket creation failed)` while discovering the local interface. This is distinct from the resolved Python worker mismatch.
- The bounded fixture cannot establish production precision/recall. Production extraction should receive manual review before being treated as hiring-grade evidence.

## 2026-10-12 — QA-FIX-02 review audit

- No implementation error observed. Human review remains a required external step: the generated artifact intentionally contains no confirmed labels and therefore cannot support automated precision/recall claims.
- The 102 accepted jobs containing dictionary terms but no extracted evidence are a targeted false-negative review pool, not confirmed false negatives; many may be incidental or non-requirement mentions.

## 2026-10-12 — QA-FIX-03 worksheet

- No blocker. Worksheet deliberately contains no confirmed labels; human review remains pending.

## 2026-10-12 — QA-FIX-04 classification

- No unresolved implementation failure. The expanded classifier increases output by retaining non-required mentions and should not be used as a hiring-suitability signal until QA-FIX-03 is human-labeled.
- No production database, M4 source relationship, M6 candidate artifact, M7 matcher, or original review artifact was modified.

## 2026-10-13 — QA-FIX-05 reconciliation

- The first reconciliation scan exceeded the short restricted-shell command window while parsing the local raw archive; the bounded rerun completed successfully and produced the expected 25-row output.
- The first restricted-shell full regression attempt reproduced the known Spark Java socket restriction. An approved local rerun passed all 24 tests; no application failure remains.

## 2026-10-13 — QA-FIX-06 human-label import blocked

- Required input `data/processed/qa_fix06_human_labels.csv` was not present, so the 25 user-reviewed classifications could not be imported or validated.
- No labels, evidence outputs, extractor code, M6/M7 artifacts, or production DuckDB contents were modified. No AI-generated labels were substituted.

## 2026-10-13 — M6-REFINE-01

- No unresolved implementation error. The previous generator sampled broad taxonomy categories; this was replaced by controlled technical role-family templates without changing M7 scoring or production DuckDB.

## 2026-10-13 — M7-REFINE-01

- No unresolved implementation error. Preferred-only evidence is currently zero because the stable processed extraction artifact predates the full QA-FIX-04 five-class output; M7 documents this limitation instead of inferring preferred labels.

## 2026-10-13 — M7-REFINE-02

- Root cause of low coverage was stale QA-FIX-01 evidence and legacy requirement-context promotion, not a missing source-description scan. The canonical QA-FIX-04 rebuild corrected lineage without changing extraction rules or taxonomy.
- No unresolved implementation error. The remaining 1,369-job no-eligible-evidence group includes taxonomy coverage gaps and descriptions without controlled dictionary evidence; it is not treated as proof of no skills.

## 2026-10-13 — M8-01 Streamlit dashboard blocked

- Streamlit is unavailable in the approved environment (`ModuleNotFoundError: No module named 'streamlit'`). No existing Streamlit configuration or app was found.
- Installation was not attempted because the task prohibits package installation without explicit approval. Dashboard implementation and UI tests were intentionally not started.

## 2026-10-13 — M8-01 resumed

- Prior Streamlit blocker resolved: approved environment provides Streamlit 1.65.0.
- Restricted-shell startup smoke was blocked by socket permissions; the approved elevated local smoke test started localhost:8501 successfully. No unresolved application error remains.

## 2026-10-12 — Environment inspection limitations

- `Get-CimInstance Win32_ComputerSystem` returned access denied, so RAM was not reported.
- `wsl --status` and `wsl -l -v` returned access denied, so WSL2 and Ubuntu availability remain unverified.
- `Get-PSDrive C` returned unusable zero values in the restricted session, so available disk space remains unverified.
- No workaround or installation was attempted because the task prohibits system-level changes.

## Manual commands for unresolved checks

Run these in an elevated PowerShell window if exact values are needed:

```powershell
Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" | Select-Object DeviceID,Size,FreeSpace
Get-CimInstance Win32_ComputerSystem | Select-Object HypervisorPresent
Get-CimInstance Win32_Processor | Select-Object VirtualizationFirmwareEnabled,VMMonitorModeExtensions,SecondLevelAddressTranslationExtensions
```

Interpret disk values in bytes. `HypervisorPresent` confirms a running hypervisor, while firmware virtualization fields indicate whether virtualization is enabled at the processor/firmware level.

## 2026-10-12 — Ubuntu first launch blocked

- `wsl --install -d Ubuntu --no-launch` completed successfully after the catalog exposed only the generic `Ubuntu` name.
- The Ubuntu app registered the distro, but first launch and a focused `wsl -d Ubuntu` retry returned `Wsl/Service/E_UNEXPECTED`.
- `WslService` is running and Ubuntu appears registered and stopped; no Linux user account was created.
- Installation stopped after the focused retry. No Java, Python packages, Spark, Airflow, repository move, or system-setting change was attempted.

## 2026-10-12 — Safe WSL restart did not resolve launch failure

- Diagnostics confirmed WSL 2.1.5.0, Ubuntu registered as version 2 and stopped, and `WslService` running.
- `wsl --shutdown` completed successfully.
- A relaunch of `wsl -d Ubuntu` reproduced `Catastrophic failure / Wsl/Service/E_UNEXPECTED`.
- Final event-log query returned no usable WSL operational events; virtualization CIM fields also returned no usable values.
- No restart, unregister, reset, reinstall, firmware change, Docker-distro change, or repository change was performed.

## 2026-10-12 — WSL issue resolved

- Ubuntu 26.04.1 LTS launches successfully in WSL2 as Linux user `developer`.
- The previously recorded `Wsl/Service/E_UNEXPECTED` condition is resolved; no destructive recovery action was needed for this update.
- The Linux-side audit shell could not repeat the Spark smoke test because Java socket creation was denied (`Operation not permitted`). The user confirmed the same test passed in the connected WSL environment, so this remains an execution-sandbox limitation rather than an unresolved project error.
- WSL-visible memory and disk values were successfully collected and recorded in `agent/PROGRESS.md` and `agent/VALIDATION.md`.

## 2026-10-12 — M1-01 dataset verification boundary

- The referenced Kaggle metadata is accessible and identifies `arshkon/linkedin-job-postings`, its CC BY-SA 4.0 declaration, and the documented CSV field names.
- Kaggle page metadata does not establish physical CSV dtypes, checksums, exact per-file row counts, encoding, or future-version stability. These remain explicit download-time checks.
- No dataset was downloaded and no package was installed, per task constraints.

## 2026-10-12 — M1-02 acquisition blocked

- Preflight found that the official `kaggle` and `kagglehub` clients are unavailable and no local Kaggle credential file is present.
- `.gitignore` did not initially cover archive extensions, `artifacts/`, or Kaggle credential locations; these protections were added before any acquisition attempt.
- The Kaggle CC BY-SA declaration is recorded, but privacy/platform terms for local processing of LinkedIn-derived raw descriptions and application URLs remain unresolved. Download was intentionally not attempted.

## 2026-10-12 — M1-02 archive validation

- User-provided ZIP is technically valid, but its member layout differs from the earlier Kaggle metadata names and its filename does not prove version 13. The actual manifest and this uncertainty are documented.
- The archive contains raw descriptions, skills text, URLs, company descriptions/addresses, and location fields. These are treated as privacy-sensitive and remain local-only; no values were printed in logs or redistributed.
- No malformed production rows were found. A synthetic malformed-row fixture was tested and rejected deterministically.

## 2026-10-12 — M2-01 execution notes

- First Spark attempt was blocked by restricted-shell Java socket permissions; elevated local execution was approved for validation.
- Initial parser configuration split multiline descriptions and produced incorrect counts; adding `multiLine=true` fixed record framing.
- Spark identified 32 source rows with malformed quoting as `malformed_record`; they remain in the reject dataset and are not silently discarded.
- `pytest` is not installed in the approved environment; standard-library `unittest` was used without installing packages.

## 2026-10-12 — M2-02 CSV discrepancy

- Spark's Univocity CSV parser split/flagged valid multiline records containing legacy unescaped quotes, even with `multiLine=true`; `STOP_AT_CLOSING_QUOTE` did not preserve the Python-writer record contract.
- Corrected by framing the bounded sample with Python `csv.reader` and creating a Spark DataFrame with the existing explicit schema. True width mismatches remain rejectable as `column_count_mismatch`.
- Spark worker Python mismatch appeared in one elevated shell run; configuring `spark.pyspark.python` and `spark.pyspark.driver.python` to the approved Python 3.12 interpreter resolved it.

## 2026-10-12 — M3-01 DuckDB modeling

- Initial non-elevated full unittest run could not start the existing Spark framing test because Java socket creation was denied by the restricted shell. Elevated rerun passed all 7 tests.
- No DuckDB modeling errors remain. Real database and reports are under ignored `data/processed/` paths.

## 2026-10-12 — M4-DEBUG DuckDB lock diagnosis

- Static audit found no nested connections, import-time connections, or unclosed M3/M4 connections; both builders close in `finally`.
- Disposable logging showed the first problematic phase was the 2,498-row `con.executemany()` bridge insert; taxonomy insertion completed first and close was not reached before the process stalled.
- A second issue appeared when copying an already-locked database: stale WAL state caused a transactional DDL lock at `DROP TABLE`. Freshly built disposable databases avoid that copied-WAL condition.
- Replaced bridge `executemany()` with a temporary non-sensitive CSV plus one set-based `read_csv` insert. Fresh `/tmp/` builds now close cleanly and pass all M4 integrity checks.

## 2026-10-12 — M4-01 production validation

- `BACKUP DATABASE TO ?` was unsupported in DuckDB 1.5.6; no data was changed. The safe supported `ATTACH` plus `COPY FROM DATABASE` method succeeded and the backup was validated.
- Production Linux-native M4 build and second rebuild completed without recurring PID 0 locks. Original Windows database was not modified.

## 2026-10-12 — M5-01 graph validation

- NetworkX 3.7 graph build and read-only DuckDB access passed. No production database writes occurred.
- Full regression was environment-limited by the existing PySpark worker mismatch: Python 3.14 worker versus Python 3.12 driver. This is unrelated to M5 graph code; M5 tests passed 3/3.

## 2026-10-12 — ENV-02 Spark Python worker mismatch

- Root cause confirmed: Spark driver ran Python 3.12.15 from the TalentGraph virtualenv while workers inherited system Python 3.14.4 because `PYSPARK_PYTHON` and `PYSPARK_DRIVER_PYTHON` were unset.
- Correction: `create_spark()` now sets both environment variables and the corresponding Spark/Python executor configuration to `sys.executable`.
- M2 tests and the full 13-test M1–M5 suite passed. No system Python or packages were changed.

## 2026-10-12 — M6-01 synthetic candidates

- One test initially used DuckDB tuple rows as mappings; corrected to positional access and reran successfully.
- Production DuckDB was opened read-only and was not modified. Candidate output is synthetic and Git-ignored.

## 2026-10-12 — M7-01 matching

- No implementation errors remain. Matching uses only explicit canonical skill overlap and does not infer suitability, hiring probability, experience, or location fit.
- Some generated candidates receive zero coverage for many jobs because M6 intentionally samples the full taxonomy while jobs use explicit source skill categories; this is retained as an honest scored outcome, not corrected by inference.

## 2026-10-13 — M8-02 dashboard validation

- Initial AppTest rejected the Data Quality navigation icon because `✓` is not a valid Streamlit emoji. Replaced it with valid `📊` and assigned unique URL paths to all callable pages. AppTest then completed with zero exceptions; no unresolved dashboard error remains.
- The first unprivileged full regression attempt was blocked by Spark socket permissions. The same suite completed successfully under the required elevated local execution context; no code failure was observed.

## 2026-10-13 — M8-04 graph technology decision

- No approved interactive graph package was installed. Plotly, PyVis, and `streamlit-agraph` were unavailable. A lightweight dependency-free SVG component was selected for pan, zoom, and highlighting; Streamlit controls handle deterministic node inspection and comparison context.

## 2026-10-13 — M8-MIGRATE-01 environment blockers

- Node.js/npm are not installed or available on PATH, so Next.js/TypeScript readiness cannot be verified yet.
- FastAPI is not installed in the approved Python environment. Uvicorn is available, but it is not sufficient to implement the backend.
- These are documented migration prerequisites. No installation was attempted because this task prohibits package changes.

## 2026-10-13 — M8-MIGRATE-02 resolved environment issue

- FastAPI TestClient could not run initially because HTTPX was absent; HTTPX 0.28.1 was installed as the authorized FastAPI test dependency. Direct route tests and live Uvicorn HTTP requests then passed.
- Installing FastAPI temporarily exposed a Starlette version conflict with Streamlit. Streamlit was subsequently retired and uninstalled as authorized; no backend dependency conflict remains.

## 2026-10-13 — M8-MIGRATE-03 build blocker

- Next.js typecheck and ESLint pass, but `next build` did not complete on the WSL environment. During the final attempt, available memory was approximately 33 MiB and swap usage was approximately 854 MiB. A native `/tmp` build attempt also exceeded its bounded timeout.
- The frontend foundation and lockfile are preserved; production build verification remains the only unresolved acceptance item. No further dependency installation or architecture change was attempted.

## 2026-10-13 — M8-MIGRATE-03A controlled build diagnosis

- Next telemetry initially attempted to write `/home/developer/.config/nextjs-nodejs/config.json.*`; the restricted runner returned `EROFS`. A per-process `NEXT_TELEMETRY_DISABLED=1` retry compiled on `/mnt/c` but timed out during lint/type checking at 180 seconds.
- A frontend-only `/tmp` build copy timed out at 240 seconds during optimized compilation. No run emitted OOM/ENOMEM evidence, no observed OOM kill occurred, and no Node/Next process remained. Resources were 3.5 GiB RAM and 1 GiB swap, nearly full at inspection. Any WSL adjustment requires user approval; task remains `IN_PROGRESS`.

## 2026-10-13 — M8-MIGRATE-03B restricted socket check

- Unprivileged local server startup and curl checks returned `EPERM`/HTTP 000 because the restricted runner disallows socket bind/connect operations. This was an execution-environment limitation, not a Next.js or FastAPI response.
- The same production frontend/backend smoke checks were rerun in the approved elevated local WSL context and passed. No unresolved application error remains.

## 2026-10-13 — M8-MIGRATE-04 browser automation unavailable

- No browser automation tool is available in this environment, so actual React Flow click, drag, zoom, expansion, and matches-navigation behavior could not be independently exercised. TypeScript, ESLint, production build, API smoke, focused graph tests, and full regression all passed.

## 2026-10-13 — M8-FRONTEND-FINAL-01 validation limits

- Light-mode mismatch was traced to default dark comparison tokens and hardcoded pale text, not the hydration-safe root theme script. Styles were consolidated; actual browser rendering and hydration-console behavior remain unverified without browser automation.
- Discover Matches previously ignored the `job` query parameter emitted by a graph job-node action. That misleading action was removed; candidate-context navigation remains.
- Explore Network previously bound its candidate selector and Reset to the current graph root, which becomes a skill/job after expansion. Candidate identity is now tracked separately; browser interaction remains unverified.
- An optional in-process `TestClient` HTTP smoke call stalled in the restricted runner's AnyIO portal and was stopped; the diagnostic timed out at 15 seconds with the route coroutine waiting in the portal. It was not retained as a hanging regression test. Direct route/unit tests and route registration checks pass; live HTTP for the new endpoint remains unverified here.
- No unresolved direct-unit/build failure or production-data write was observed. Browser-only interaction and viewport checks remain manual.
