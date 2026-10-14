# Technology stack

Versions below were checked against the current local virtual environment, runtime commands, or `frontend/package-lock.json` on 2026-10-13. They are not a clean-install compatibility claim.

| Technology | Verified version | Purpose |
|---|---|---|
| Python | 3.12.15 | Sampling, transformations, extraction, graph, matching, and API code. |
| PySpark | 3.5.6 | Local-mode typed transformations over the bounded sample. |
| Apache Parquet | Format; no single runtime version | Curated, reusable columnar job and reject files written by Spark and read by DuckDB. |
| DuckDB | 1.5.6 | Local analytical warehouse and read-only application queries. |
| Pandas | 3.0.6 installed; not directly imported | Available in the environment; not a direct application requirement. |
| PyArrow | 25.0.1 installed; not directly imported | Available in the environment; not required by the current direct source imports. |
| RapidFuzz | 3.14.6 | Candidate matching for controlled M4 skill aliases and review thresholds. |
| NetworkX | 3.7 | In-memory typed graph relationships and traversal. |
| Canonical skill extractor | Project code, `qa-fix-04-v1` artifact version | Rule-based detection and five-class evidence classification. |
| Evidence-aware matcher | Project code, M7 | Required overlap, preferred matches, evidence status, and deterministic ranking. |
| FastAPI | 0.115.6 | Read-only application endpoints. |
| Uvicorn | 0.54.0 | Local ASGI server. |
| Pydantic | 2.10.6 | API response and request models. |
| HTTPX | 0.28.1 | Existing backend/test dependency declaration; not a core pipeline library. |
| Next.js | 15.2.4 (lockfile) | App Router frontend and local backend proxy. |
| React / React DOM | 19.0.0 (lockfile) | Browser UI. |
| TypeScript | 5.7.2 (lockfile) | Typed frontend. |
| React Flow (`@xyflow/react`) | 12.12.0 (lockfile) | Interactive browser graph neighborhoods. |
| Node.js / npm | 22.14.0 / 10.9.2 | Frontend development and builds. |
| OpenJDK | 17.0.20.1 | Java runtime for local Spark. |
| WSL Ubuntu | 26.04.1 LTS | Current Linux development environment. |
| Git | 2.53.0 | Source control. |
| VS Code | 1.108.2 in the earlier M0 record; current version not independently verified | Editor used during development. |

PySpark provides a structured transformation workflow on a small local machine; this project does not demonstrate distributed-scale performance. Parquet separates curated processing output from warehouse modeling. DuckDB is compact and suits local SQL validation. NetworkX models relationships in Python, while React Flow draws bounded API neighborhoods in the browser. FastAPI keeps database and artifact reads behind typed endpoints; Next.js handles navigation and interactions.

The main flow is source archive → deterministic sample → PySpark → Parquet → DuckDB → read-only FastAPI → Next.js. Classified description evidence is extracted from the archive and selected IDs into a separate JSON artifact. Fictional candidates are generated from the taxonomy into another JSON artifact. The API combines those artifacts with warehouse job metadata for comparisons and graph projections; the browser does not query DuckDB.

[`requirements.txt`](../requirements.txt) pins direct Python dependencies and includes the existing backend requirement file. [`frontend/package.json`](../frontend/package.json) and [`frontend/package-lock.json`](../frontend/package-lock.json) describe and lock frontend packages. Node.js and Java remain separate prerequisites. The source archive and processed artifacts are not distributed with Git. Follow the [README](../README.md) for the current local startup and validation commands; a fresh machine setup has not been independently reproduced.
