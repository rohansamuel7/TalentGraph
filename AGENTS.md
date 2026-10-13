# TalentGraph Agent Instructions

## Mission
TalentGraph is an end-to-end talent intelligence and data engineering platform that ingests job postings and synthetic candidate profiles, standardizes skills, builds a knowledge graph, and provides transparent, evidence-based job matching.

## Project Goals
Prioritize reliable ingestion, schema design, SQL, Spark transformations, data quality, orchestration, incremental processing, documentation, and clear technical tradeoffs. Demonstrate production-minded engineering at laptop scale.

## Stack and restrictions
Use Python, Apache Airflow in WSL2 Ubuntu, local-mode PySpark, DuckDB, SQL, Pandas, NetworkX, RapidFuzz, Streamlit, Plotly, Pytest, and PyArrow. Do not use Docker, Kafka, local LLMs, paid cloud infrastructure, or heavyweight services. Do not install packages, download data, or make system changes without explicit approval.

## Repository structure
Keep application code under `src/`, tests under `tests/`, DAGs under `dags/`, SQL under `sql/`, configuration under `config/`, documentation under `docs/`, agent state under `agent/`, and local data/artifacts under ignored directories such as `data/`, `datasets/`, `downloads/`, and `artifacts/`.

## Standards
Use typed, small Python modules; clear names; deterministic transformations; structured logging; explicit schemas; parameterized SQL; and focused tests. Format and lint only with approved project tooling. Avoid speculative abstractions and broad refactors.

## Data engineering rules
Preserve raw inputs and provenance, separate real from synthetic records, validate contracts at boundaries, make transformations deterministic and idempotent, avoid unnecessary memory use, and design Spark for a small local machine. Never assume the Kaggle schema or license.

## SQL rules
Use explicit columns, stable aliases, readable CTEs, dialect-aware DuckDB SQL, no `SELECT *` in modeled outputs, documented keys, and tests for grain, nulls, duplicates, and joins.

## Ontology and entity resolution
Maintain a controlled skill taxonomy with canonical IDs, aliases, provenance, and confidence. Preserve raw values. Normalize case, whitespace, punctuation, and approved aliases only. Use RapidFuzz candidates with thresholds, deterministic tie-breaking, explainable match reasons, and an explicit review/unknown path. Never silently overwrite source terms.

## Quality and testing
Test schemas, constraints, transformations, matching calculations, graph relationships, incremental behavior, idempotency, DAG loading, and application smoke paths. Tests must be repeatable and resource-conscious. Never claim a test passed unless it was executed.

## Security
Never commit credentials, tokens, `.env` files, private keys, virtual environments, databases, logs, or downloaded datasets. Use environment variables and sanitized examples. Review staged files before every commit.

## Documentation and Git
Read this file and relevant `docs/` and `agent/` files before each task. Keep progress, validation, errors, and decisions current. Use focused commits such as `feat:`, `fix:`, `test:`, and `docs:`. Do not push without explicit approval.

## Agent execution rules
Follow `agent/LOOP_ENGINEERING.md`. Select one task, define measurable acceptance criteria, implement the smallest coherent change, test it, repair a failure at most three focused times, document results, and stop on an unresolved blocker. Do not change major architecture without approval.

## Definition of Done
A task has met its acceptance criteria; relevant tests and regression checks were executed; no unresolved errors are hidden; documentation and agent state are updated; staged files contain no sensitive or excluded artifacts; and the change is reviewable.

## Source-of-truth files
Consult `docs/PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, `docs/ENGINEERING_STANDARDS.md`, `docs/IMPLEMENTATION_PLAN.md`, and `agent/TASKS.md` before implementation. Record material choices in `docs/DECISIONS.md`; record execution in `agent/PROGRESS.md`, `agent/VALIDATION.md`, and `agent/ERROR_LOG.md`.
