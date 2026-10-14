# Architecture

**Current implementation (M8):** the local pipeline prepares sampled data with Python and PySpark, writes curated Parquet, and models jobs and taxonomy in DuckDB. Classified job evidence and fictional candidates are separate processed JSON artifacts. FastAPI loads those artifacts and DuckDB read-only; Next.js serves Explore Network, Discover Matches, and Insights. React Flow renders bounded graph neighborhoods. See [Data pipeline](DATA_PIPELINE.md) for the implemented flow.

The diagram and Streamlit/Airflow description below record the original design direction. Streamlit was retired during M8 migration. Production Airflow scheduling has not been implemented.

```text
Kaggle job data + synthetic candidates
        -> Airflow orchestration
        -> PySpark ingestion and transformations
        -> DuckDB analytical models
        -> ontology alignment and entity resolution
        -> NetworkX knowledge graph
        -> explainable matching
        -> Streamlit dashboard
```

Airflow schedules and observes tasks. PySpark reads bounded raw files, applies explicit schemas, standardizes fields, and writes curated artifacts. DuckDB provides lightweight analytical storage and SQL models. Ontology services map raw skills to canonical concepts and retain confidence/provenance. Entity resolution links equivalent jobs, skills, companies, and candidates deterministically. NetworkX represents relationships for traversal and explanations. Matching combines documented features and produces reasons, not opaque decisions. Streamlit reads curated outputs and presents filters, summaries, graph context, and match explanations.

All components run locally; Airflow runs in WSL2 Ubuntu. Inputs, intermediate outputs, and final models have explicit boundaries, validation, and provenance. Data volume and concurrency remain bounded for laptop resources.
