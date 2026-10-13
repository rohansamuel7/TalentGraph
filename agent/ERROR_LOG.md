# Error Log

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
