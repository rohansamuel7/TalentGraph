# TalentGraph Project Specification

## Problem and objectives
Recruiting data is fragmented across job postings, skills, candidate profiles, and taxonomies. TalentGraph will create a small, transparent analytical system that aligns these entities and explains why a candidate matches a job.

## Scope
The system will ingest approximately 1,000–2,000 sampled public job postings and about 300 synthetic candidates; normalize schemas; align skills to a controlled taxonomy; resolve entities; model analytical facts in DuckDB; build a NetworkX graph; calculate explainable matches; and present results in Streamlit.

## Requirements
- Preserve source provenance and distinguish public from synthetic data.
- Use Spark locally for ingestion/transformation and Airflow in WSL2 for orchestration.
- Use DuckDB for analytical models and SQL validation.
- Support malformed records, synthetic updates, incremental loading, and idempotent reruns.
- Expose match scores, contributing skills, gaps, confidence, and reasons.
- Keep the demonstration efficient on a modest laptop.

## Acceptance criteria
An end-to-end local run produces validated modeled data, graph relationships, deterministic explainable matches, and a working dashboard; tests cover critical transformations and failure paths; rerunning the same input does not duplicate results; and documentation explains setup and tradeoffs.

## Non-goals
Production-scale deployment, real-time streaming, personal-data collection, automated hiring decisions, Docker, Kafka, cloud infrastructure, local LLMs, and unsupported native-Windows Airflow.

## Dataset note
Candidate Kaggle reference: https://www.kaggle.com/dsv/9200871. Schema, licensing, and download size must be verified before use and only with approval.
