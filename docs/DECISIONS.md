# Architecture Decision Records

The early Streamlit decision below records the initial direction. M8 later retired Streamlit in favor of read-only FastAPI and Next.js; see [M8 backend](M8_BACKEND.md) and [Engineering overview](PROJECT_DOCUMENTATION.md). This note preserves the historical decision without presenting it as the current architecture.

## ADR-001: Local-first architecture
**Status:** Accepted. **Decision:** Use local Spark, DuckDB, NetworkX, and Streamlit. **Reason:** The project must be reproducible on a modest laptop without paid infrastructure. **Tradeoff:** It is not production-scale.

## ADR-002: Airflow in WSL2
**Status:** Proposed pending environment verification. **Decision:** Run Airflow in Ubuntu under WSL2. **Reason:** Native Windows Airflow support is unsuitable. **Tradeoff:** Requires WSL2 setup and filesystem discipline.

## ADR-003: Hybrid real and synthetic data
**Status:** Accepted. **Decision:** Use a bounded, licensed public job sample plus synthetic candidates and controlled updates. **Reason:** Enables realistic structure without exposing personal data. **Tradeoff:** Synthetic candidates are not representative of every real-world edge case.

## ADR-004: Explainable deterministic matching
**Status:** Accepted. **Decision:** Combine documented features, taxonomy alignment, and entity-resolution evidence with thresholds and reasons. **Reason:** Users and technical reviewers must be able to inspect outcomes. **Tradeoff:** Less flexible than opaque learned ranking.

## ADR-005: Bounded hash-ranked public job sample
**Status:** Proposed for approval. **Decision:** Use 1,500 valid postings selected by lowest SHA-256 rank of stable source `job_id`, then filter related tables by selected IDs. **Reason:** Reproducible and memory-bounded on approximately 3.5 GiB WSL-visible memory; independent of CSV order. **Tradeoff:** It is not statistically stratified and depends on stable source IDs.

## ADR-006: Synthetic candidate-only profiles
**Status:** Accepted. **Decision:** Generate approximately 300 fictional candidates from controlled vocabularies with a fixed seed and explicit synthetic labels; never ingest real resumes or personal data. **Reason:** Enables matching demonstrations without collecting personal information. **Tradeoff:** Synthetic profiles do not represent the full diversity or messiness of real candidates.

## ADR-007: Acquisition gate for LinkedIn-derived raw data
**Status:** Blocked pending approval. **Decision:** Do not acquire the Kaggle archive until an official access method is available and local processing of descriptions, application URLs, and possible incidental personal data is explicitly approved. **Reason:** The Kaggle page declares CC BY-SA 4.0, but that declaration does not by itself resolve underlying platform terms or privacy obligations. **Tradeoff:** M1-02 acquisition and physical validation remain paused.

## ADR-008: Use the observed archive manifest, not the metadata projection
**Status:** Accepted for local development. **Decision:** Process the observed `postings.csv` and related `companies/`, `jobs/`, and `mappings/` members only after recording their actual headers; do not rename them to the earlier metadata projection or claim the ZIP proves version 13. **Reason:** The user-provided archive is technically valid but its manifest differs from the accessible Kaggle description. **Tradeoff:** Version identity remains an explicit provenance uncertainty until the source download/version receipt is available.

## ADR-009: Template-based technical synthetic candidates
**Status:** Accepted. **Decision:** Generate M6 candidates from four explicit technical role families and canonical technical taxonomy keys; exclude business, occupational, industry, and operations labels from candidate-skill bridges. **Reason:** Random full-taxonomy sampling produced incoherent candidate profiles and weakened M7 explanations. **Tradeoff:** The synthetic population covers a deliberately narrow technical vocabulary and is not a labor-market distribution.

## ADR-010: Read-only technical-skill frequency for Insights
**Status:** Accepted. **Decision:** Count each sampled job once per canonical competency with required or preferred M7 evidence and expose the top eight via a read-only FastAPI endpoint. **Reason:** The Insights chart needs verified job-posting frequencies without altering extraction or matching. **Tradeoff:** Counts reflect observed evidence in a deterministic, non-representative sample and omit incidental or unsupported mentions.
