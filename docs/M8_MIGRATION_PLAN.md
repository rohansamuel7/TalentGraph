# M8 migration audit: Next.js and FastAPI

## Audit result

The repository was ready for an incremental architecture migration. Node.js and npm remain absent from PATH. M8-MIGRATE-02 installed FastAPI 0.115.6 and Pydantic 2.10.6; Uvicorn 0.54.0, DuckDB 1.5.6, and NetworkX 3.7 remain available. Streamlit was retired after backend validation. No frontend directory, package manifest, TypeScript configuration, or Next.js configuration exists.

The host reports 3.5 GiB RAM, approximately 1.1 GiB available, and a 1 GiB swap file. Development should remain laptop-scale, avoid large client bundles, and keep DuckDB access in a single read-only backend process.

Recommended implementation pins, subject to a separate approved installation step, are Node.js 22 LTS with npm 10+, Next.js 15 with the App Router, React 19, TypeScript 5.6+, `@xyflow/react` 12, FastAPI 0.115+, Pydantic 2, and the existing Uvicorn line. Exact versions must be locked in a new manifest and verified together before coding.

## Reusable backend interfaces

| Need | Existing interface | Migration use |
|---|---|---|
| Jobs and metadata | `m7_matching.load_reference_data()`; read-only DuckDB query in `src/talentgraph/m7_matching.py` | Thin service adapter with bounded search, stable ordering, and neutral null display values |
| Job search | `api_data.search_jobs()` | Reuse deterministic filtering semantics in the FastAPI service |
| Candidates | M6 `synthetic_candidates.json`; `load_reference_data()` | Validate schema once, expose synthetic label, role family, seniority, and technical skills |
| Competency names | `reference["skill_names"]` from `dim_skill` | Use canonical IDs internally and names in display fields |
| Candidate-to-job matching | `rank_jobs_for_candidate()` and `score_candidate_job()` | Call directly; do not reproduce scoring in FastAPI or TypeScript |
| Job-to-candidate matching | `rank_candidates_for_job()` | Call directly with a bounded `limit` |
| Evidence | `m7_evidence.load_job_evidence()` and canonical QA-FIX-04 artifact | Preserve required, preferred, mentioned, negated, ambiguous, provenance, and version fields; only required/preferred enter graph requirement paths |
| Graph lineage | `m5_graph.build_graph()` | Preserve as lineage/reference; do not expose M4 `POSTED_BY`, `LOCATED_IN`, or broad legacy skill relationships as verified requirements |
| Current projection | `network_projection.build_projection()` | Reusable read-only candidate-centered projection for the first React Flow adapter |

`api_store.Store` establishes the current artifact paths and validates them at backend startup. The FastAPI service fails clearly on incompatible or missing artifacts rather than falling back to stale evidence.

## Graph projection contract

Build a deterministic projection from the M6 candidate artifact and canonical M7 evidence:

- Candidate nodes: `candidate:{stable_id}`, display name, role family, seniority, and synthetic flag.
- Competency nodes: canonical `skill:{id}`, canonical display name, and taxonomy provenance.
- Job nodes: `job:{stable_id}`, title, company fallback, and sampled-job metadata.
- `HAS_SKILL`: candidate to competency for every stored M6 technical competency.
- `REQUIRES_SKILL`: job to competency only for `required` evidence.
- `PREFERS_SKILL`: job to competency only for `preferred` evidence, rendered distinctly.

Incidental, mentioned, negated, ambiguous, missing-dictionary, and unsupported category relationships remain available as evidence detail but never become requirement edges. The projection should be candidate-centered by default, capped by a server-side limit, sorted by stable IDs, and expanded by one or two hops through an explicit neighborhood request. Every edge should carry evidence classification, source location, extraction version, and source-description integrity reference when applicable.

## Minimal API contract

All responses should be JSON with stable identifiers, readable display fields, deterministic ordering, and explicit `limit`/`offset` bounds. Suggested maximum page size is 50; neighborhood nodes and edges should be capped at 200 and 400 respectively.

### `GET /api/health`

No inputs. Returns `{ "status": "ok", "api_version": "m8-migrate-01", "evidence_version": "qa-fix-04-v1", "artifacts": { ... } }`. Return 503 when required artifacts, schema versions, or the read-only database cannot be validated.

### `GET /api/overview`

No inputs. Returns sample counts, candidate count, mutually exclusive evidence coverage counts, artifact versions, and a nonrepresentative-sample note. It must not expose a numeric production accuracy claim.

### `GET /api/jobs`

Query: `q`, `evidence_status` (`all|required|preferred_only|insufficient`), `limit`, `offset`. Returns `{ "items": [{ "job_id", "title", "company_name", "location", "evidence_status" }], "total", "limit", "offset" }`. Empty searches return 200 with an empty list.

### `GET /api/jobs/{job_id}`

Returns job metadata plus separate `required`, `preferred`, and `other_evidence` arrays. Evidence items include canonical competency ID/name, classification, text, source location, extraction rule/version, and source hash. Missing IDs return 404; unsupported evidence remains visible but not promoted.

### `GET /api/candidates`

Query: `q`, `role_family`, `seniority`, `limit`, `offset`. Returns stable synthetic candidate IDs, display name, role family, seniority, `synthetic: true`, and competency summaries. No protected demographics or personal-data fields.

### `GET /api/candidates/{candidate_id}`

Returns the candidate profile, canonical technical competencies, and synthetic marker. Missing IDs return 404. It may include bounded top matches, but matching should remain a separate endpoint for clear semantics.

### `GET /api/matches`

Query: exactly one candidate ID or job ID, optional `limit`. Returns ranked comparison rows with evidence status, matched/missing required competencies, preferred matches, and provenance. `required_skill_overlap` is nullable for insufficient evidence. Do not return a numeric score for `insufficient_evidence`; do not label overlap as suitability, probability, or confidence.

### `GET /api/graph/neighborhood`

Query: `node_id`, `hops` (1–2), optional node/evidence filters, `limit`. Returns `{ "nodes": [...], "edges": [...], "root": "...", "truncated": false }`. Reject unknown node IDs with 404 and invalid limits with 422. Edges must be source-backed and include their evidence class and provenance.

## Frontend structure

Use a small Next.js App Router application:

```text
frontend/
  app/
    layout.tsx
    page.tsx                 # Explore Network
    matches/page.tsx         # Discover Matches
    insights/page.tsx        # Insights
  components/
    network/NetworkCanvas.tsx
    network/NodeDetails.tsx
    matches/MatchCard.tsx
    shared/StatusMessage.tsx
  lib/api.ts
  lib/types.ts
  styles/tokens.css
```

React Flow should receive typed API nodes and edges, with three restrained node colors and a distinct dashed preferred edge. Keep the details panel contextual, use skeleton/loading/empty/error states, and keep internal IDs secondary. Use server-side data fetching where appropriate and client state only for graph selection, filters, and neighborhood expansion.

## Staged implementation plan

### M8-MIGRATE-02 — FastAPI backend

Deliverables: read-only application factory, typed Pydantic response models, artifact/version validation, the endpoints above, bounded search, and service-level tests. Dependencies: approved FastAPI/Pydantic installation. Risks: DuckDB connection lifecycle, stale artifacts, accidental scoring duplication. Validation: endpoint contract tests, read-only database checks, deterministic responses, and 404/422/503 behavior. Status: completed as M8-MIGRATE-02; Streamlit retirement is documented in `docs/M8_BACKEND.md`.

### M8-MIGRATE-03 — Next.js foundation

Deliverables: locked frontend manifest, App Router shell, design tokens, typed API client, three destinations, and accessible loading/error states. Dependencies: Node/npm and M8-MIGRATE-02 contract. Risks: constrained memory and API URL configuration. Validation: TypeScript build, lint/type checks if approved, route smoke tests, and no raw IDs in primary labels. Current status: COMPLETE. The approved 3.0 GiB swap / approximately 3.8 GiB visible RAM environment supported a successful production build on 2026-10-13; TypeScript, ESLint, live routes, FastAPI proxy integration, and the 43-test backend regression all passed. M8-MIGRATE-04 remains the next task and was not started.

### M8-MIGRATE-04 — Interactive knowledge graph

Deliverables: React Flow canvas, deterministic neighborhood loading, node selection, pan/zoom, one/two-hop expansion, edge legend, and contextual details. Dependencies: graph endpoint and typed projection. Risks: oversized graph payloads and category/evidence misrepresentation. Validation: source-backed node/edge tests, bounded payload tests, required/preferred visual distinction, and browser interaction checks. Status: COMPLETE. `@xyflow/react` 12.12.0 is locked; the explorer uses real candidate, competency, and job records with bounded lazy expansion. Browser automation was unavailable, so visual interactions remain unverified beyond code-level and production-build validation.

### M8-MIGRATE-05 — Matching experience and product polish

Deliverables: candidate/job discovery, M7 explanation cards, insufficient-evidence handling, insights metrics, empty states, responsive styling, and accessibility pass. Dependencies: stable API contracts and graph navigation. Risks: implying suitability or accuracy, inconsistent display semantics. Validation: matching contract tests, visual checks, accessibility review, and null-score assertions.

### M8-MIGRATE-06 — End-to-end verification and Streamlit retirement decision

Deliverables: integrated local runbook, regression suite, deterministic artifact comparison, performance/resource findings, deployment decision, and an explicit Streamlit retain/retire recommendation. Dependencies: all prior stages. Risks: parity gaps, hidden Streamlit workflows, operational complexity. Validation: clean-environment startup, API/frontend smoke tests, full regression, read-only DuckDB audit, and stakeholder review.

## Migration risks and immediate next step

The largest blockers are missing Node/npm and FastAPI, limited available memory, the absence of a frontend build baseline, and the need to keep evidence semantics identical across Python and TypeScript. React Flow also requires careful payload limits; it must not receive the full 1,500-job graph by default.

The next frontend migration step is M8-MIGRATE-03: obtain approval to install/pin Node.js/npm and implement the Next.js foundation against the tested FastAPI contract. No frontend work should begin until the backend schemas remain stable.

## M8-MIGRATE-02 completion

The FastAPI backend is implemented in `src/talentgraph/api.py` and focused supporting modules. Streamlit-only source files, tests, and dashboard documentation were removed after import auditing. The replacement backend runbook is `docs/M8_BACKEND.md`; pinned backend dependencies are in `requirements-backend.txt`. The Next.js toolchain remains intentionally uninstalled for M8-MIGRATE-03.
# M8-MIGRATE-05

The matches UX refinement is frontend-only: it consumes the existing evidence-aware API, preserves nullable overlap and preferred-skill separation, and adds compact filtering/sorting plus expandable provenance details. No M1–M7 logic or DuckDB artifact is changed.

## Current release status — M8-MIGRATE-06

The Next.js/FastAPI migration is implemented with `/network`, `/matches`, and `/insights`. The backend remains read-only over the validated artifacts. End-to-end code-level verification confirms source-backed graph relationships, evidence-aware matching, accurate coverage counts, stable synthetic IDs, and successful production builds. Browser automation is not installed or available, so manual visual and interaction checks remain an explicit release follow-up.
