# Implementation Plan

| Milestone | Deliverable | Dependencies | Estimate |
|---|---|---|---:|
| M0 | Environment, repository layout, conventions | None | 1–2 h |
| M1 | Approved dataset strategy, raw schema, synthetic generator | M0, license/schema review | 3–4 h |
| M2 | PySpark ingestion, normalization, malformed-record handling | M1 | 4–6 h |
| M3 | DuckDB schemas, dimensions, facts, SQL tests | M2 | 4–5 h |
| M4 | Skill ontology, aliases, provenance, alignment | M1, M3 | 3–4 h |
| M5 | Entity resolution with RapidFuzz and review thresholds | M4 | 3–5 h |
| M6 | NetworkX graph and relationship tests | M3–M5 | 3–4 h |
| M7 | Incremental keys, checkpoints, idempotent writes | M2–M6 | 3–4 h |
| M8 | Data quality checks, logging, observability artifacts | M2–M7 | 3–4 h |
| M9 | Airflow DAGs in WSL2 and local validation | M2–M8 | 4–6 h |
| M10 | Streamlit demonstration and efficient visualizations | M3–M6 | 4–6 h |
| M11 | Regression suite, documentation, and demonstration readiness | M0–M10 | 4–6 h |

Work one small task at a time. Core ingestion, modeling, quality, matching, and reproducibility precede optional dashboard polish.
