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

| Challenge | Impact | Investigation | Resolution / current status |
|---|---|---|---|
| CSV framing in M2 | Spark initially reported 1,516 records and 32 malformed entries from a 1,500-row sample. | The parser split valid multiline records containing legacy quoting. | Python's CSV reader frames the bounded input before Spark applies its explicit schema; the final recorded run accepted 1,500 and rejected zero. |
| Spark execution in restricted shells | Some test attempts could not start Java sockets; a separate Python worker version mismatch affected one run. | Error logs separated socket denial from the driver/worker interpreter mismatch. | Worker interpreter is pinned to the approved virtualenv in code. The restricted-shell socket limitation remains an environment constraint, not evidence of a failed production pipeline. |
| Broad M4 skills and sparse technical evidence | Occupational categories could mislead matching; few descriptions supply usable required technical evidence. | QA reviews compared taxonomy categories, source descriptions, and extractor output. | M7 excludes broad categories, retains required/preferred/other classifications, and reports insufficient evidence. Current API coverage is 80 required, 7 preferred-only, 44 non-required-only, and 1,369 without eligible technical evidence. Extraction quality remains limited. |
| Source-row traceability | Stored row numbers may be mistaken for stable source locations. | M2 assigns a Spark processing row index after framing, while evidence extraction enumerates archive CSV records. | Job ID, source file, and description hash aid tracing, but equivalence of all stored row numbers to archive physical rows has not been established. See [limitations](LIMITATIONS_AND_FUTURE_WORK.md). |
| DuckDB checksum labels | Earlier M8 notes called `b2314da8…` a production hash. | M8-INTEGRITY-01 hashed both known paths and compared read-only tables. | That hash belongs to `data/processed/talentgraph.duckdb`; production hashes to `663dbe12…`. The five base tables have matching logical schemas and rows. The record was mislabeled; no corruption was established. |
| WSL frontend builds and `.next` state | Early builds timed out under memory pressure; simultaneous development and build use of `.next` risks conflict. | Resource logs and build attempts isolated memory and telemetry constraints; the validation record checked for an active dev server before builds. | A later build passed with more visible RAM/swap. Run dev and production builds separately; a concurrent `.next` failure is a precaution, not a documented data defect. |
| Theme hydration and graph readability | Theme initialization produced a root attribute warning; graph controls needed clearer states. | M8 records traced the warning to pre-hydration theme initialization and reviewed graph interactions. | Root warning suppression was scoped to `<html>`; graph controls and contrast were improved. Browser-level visual checks remain manual. |

## Current outcome

Explore Network shows bounded candidate-skill-job neighborhoods; Discover Matches shows evidence-aware comparisons; Insights reports sample coverage and observed technical-skill frequency. The app is a local prototype over one deterministic sample and fictional candidates. It has no scheduled production ingestion, deployment guarantee, or basis for hiring decisions. Read [limitations and future work](LIMITATIONS_AND_FUTURE_WORK.md) before interpreting results.
