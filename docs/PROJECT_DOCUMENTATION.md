# TalentGraph engineering overview

TalentGraph is a local prototype for talent intelligence and workforce analytics. It connects sampled job postings, a controlled set of technical competencies, and fictional candidate profiles. A user can inspect job-skill relationships, explore candidate-to-role comparisons, and see where the available posting text supports or fails to support a technical skill comparison. The result is an explanation of observed evidence, not a prediction of hiring outcomes.

## Architecture

Python handles source inspection, deterministic sampling, extraction, and data preparation. Local PySpark transforms the bounded posting sample and writes curated Parquet. DuckDB stores modeled jobs, companies, locations, and the M4 skill taxonomy. Classified job-description evidence and synthetic candidates remain separate JSON artifacts. NetworkX represents relationships in Python; the current browser graph is a bounded projection of candidate and evidence relationships. FastAPI reads the validated database and artifacts through read-only connections, and Next.js with React Flow presents the three application pages.

These boundaries keep source processing separate from application requests. The API does not rerun ingestion or write the warehouse. See [Data pipeline](DATA_PIPELINE.md) for paths, validation, and the relationship between the database and parallel artifacts.

## Development milestones

| Milestone | Delivered |
|---|---|
| M1 | Inspected the user-provided archive and its actual CSV headers; selected 1,500 jobs deterministically and recorded source metadata. The archive's exact published version is unverified. |
| M2 | Built bounded local PySpark cleaning, curated Parquet, rejects, and quality reports. Corrected CSV record framing after Spark's parser split valid multiline records. |
| M3 | Modeled job facts, company and location dimensions, analytical views, and SQL quality checks in DuckDB. |
| M4 | Added a controlled skill taxonomy and source-skill bridge with aliases, match provenance, and validation. |
| M5 | Built a NetworkX graph over warehouse jobs, companies, locations, and M4 skills for lineage and traversal. |
| M6 | Generated 300 reproducible, explicitly fictional technical profiles from taxonomy-backed role templates. |
| M7 | Added evidence-aware comparisons and a versioned classified-evidence artifact. Required and preferred competencies are separate; insufficient evidence leaves overlap unavailable. Earlier M7 work also covered repeat-run/idempotency checks. |
| M8 | Replaced the earlier Streamlit demonstration with a read-only FastAPI service and Next.js application: Explore Network, Discover Matches, and Insights. UI and API validation is recorded in `agent/VALIDATION.md`. |

## Key decisions

- **Repeatable sample:** the lowest SHA-256 ranks of stable job IDs select the same 1,500 records from the same source. This supports repeat tests, but is not statistical sampling.
- **Preserved boundaries:** raw input stays local; the sampled CSV and curated Parquet are distinct from DuckDB models. Descriptions and URLs are excluded from curated M2 output, while evidence extraction reads the source archive separately.
- **Modeled warehouse:** explicit job, company, and location keys make row counts and joins testable. DuckDB keeps this small warehouse local.
- **Controlled competency meaning:** M4 broad occupational categories remain available as source lineage but do not become technical requirements. The later extractor maps recognized terms to canonical technical IDs with classifications and source evidence.
- **Careful comparison:** only eligible required evidence forms the overlap denominator. Preferred evidence is reported separately; no required evidence produces a null overlap rather than a misleading zero. The graph only promotes supported required or preferred evidence to job-skill edges.
- **Read-only serving:** FastAPI opens the configured production database with `read_only=True`; Next.js consumes bounded API results rather than reading data files directly.

## Engineering challenges

### 1. CSV framing in M2

**Problem:** Spark initially counted 1,516 records and 32 malformed entries in a 1,500-posting sample. **Why:** Some descriptions contained line breaks and older quoting patterns that Spark split into separate records. **Solution / status:** Python's CSV reader first identifies each complete record; Spark then applies the expected column types (the schema). The final recorded run accepted 1,500 and rejected zero. **Lesson learned:** Check record boundaries before trusting row counts or applying a schema.

### 2. Spark execution in restricted shells

**Problem:** Some test runs could not start Spark, and one separate run used different Python versions for Spark's main process and its workers (the processes that run tasks). **Why:** The restricted shell denied Java socket creation; the workers also inherited a different Python interpreter. **Solution / status:** The code points the main process and workers to the approved virtual environment. Restricted-shell socket failures remain an environment constraint. **Lesson learned:** Diagnose runtime permissions and interpreter versions separately from data-processing errors.

### 3. Broad M4 skill categories and sparse technical evidence

**Problem:** M4 includes broad occupational categories that could look like technical requirements. Few descriptions provide usable required technical skills. **Why:** Source categories describe kinds of work, while job descriptions vary in how clearly they state specific requirements. **Solution / status:** M7 uses classified description evidence for technical comparisons and keeps broad M4 categories for source tracing. Of 1,500 postings, 80 have required technical evidence, 7 have preferred-only evidence, 44 have non-required-only evidence, and 1,369 have no eligible technical evidence. Extraction remains imperfect. **Lesson learned:** Keep a source category's original meaning; do not promote it to a verified requirement without evidence.

### 4. Source-row traceability

**Problem:** A stored row number may appear to identify the same source record across outputs. **Why:** M2 numbers records during Spark processing, while the evidence extractor numbers logical CSV records in the archive. **Solution / status:** Job IDs, source names, and description hashes help trace records, but direct row-number equivalence remains unverified. **Lesson learned:** Provenance (where a record came from) needs identifiers that can be checked across processing stages. See [limitations](LIMITATIONS_AND_FUTURE_WORK.md).

### 5. DuckDB checksum labels

**Problem:** Earlier M8 notes labeled `b2314da8…` as the production database hash. **Why:** That hash belongs to the repository database at `data/processed/talentgraph.duckdb`; the production database hashes to `663dbe12…`. A checksum is a file hash used to identify exact bytes. **Solution / status:** A read-only check found matching schemas and rows in all five base tables, despite different file hashes. The earlier label was wrong; the check found no logical mismatch in those tables. **Lesson learned:** Record the full file path beside each checksum, and compare table contents when byte-level hashes differ.

### 6. WSL frontend builds and `.next` state

**Problem:** Early frontend builds timed out, and a development server and production build could interfere if both use Next.js's `.next` build directory. **Why:** WSL had limited memory during the early builds; the shared directory can also hold state from another process. **Solution / status:** A later production build passed with more available RAM and swap. Running development and production builds separately avoids the potential directory conflict; a concurrent `.next` failure was not documented. **Lesson learned:** Check available resources and running processes when a build fails.

### 7. Theme hydration and graph readability

**Problem:** Theme setup caused a root-element warning, and graph controls were hard to read in some states. **Why:** The theme was set before React attached to the page (hydration), so the root HTML attribute could differ; some controls also needed clearer contrast. **Solution / status:** Warning suppression was limited to `<html>`, and graph controls and contrast were improved. Browser visual checks remain manual. **Lesson learned:** Keep theme setup predictable and verify visual changes in the browser.

## Current outcome

Explore Network shows bounded candidate-skill-job neighborhoods; Discover Matches shows evidence-aware comparisons; Insights reports sample coverage and observed technical-skill frequency. The app is a local prototype over one deterministic sample and fictional candidates. It has no scheduled production ingestion, deployment guarantee, or basis for hiring decisions. Read [limitations and future work](LIMITATIONS_AND_FUTURE_WORK.md) before interpreting results.
