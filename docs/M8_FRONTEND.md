# M8 Next.js frontend foundation

## Local setup

The frontend uses the user-scoped Node.js 22.14.0 installation under `.tools/` and the pinned dependencies in `frontend/package-lock.json`.

```bash
export PATH="$PWD/.tools/node-v22.14.0-linux-x64/bin:$PATH"
cd frontend
npm ci
npm run dev
```

Run the backend separately:

```bash
PYTHONPATH=src /home/developer/venvs/talentgraph/bin/uvicorn talentgraph.api:app --app-dir src
```

The Next.js rewrite proxies `/backend/*` to the local FastAPI service at `127.0.0.1:8000`.

## Routes

- `/network` — bounded React Flow graph of source-backed candidates, technical skills, and jobs.
- `/matches` — candidate comparisons in a selectable split view, with title/company search, sorting, comparable-only filtering, and evidence details.
- `/insights` — sampled-job KPIs, mutually exclusive evidence coverage, and observed technical-skill frequency.
- `/` redirects to `/network`.

TypeScript and ESLint passed. Route smoke testing returned successful responses for all three routes. After the approved WSL resource adjustment, the production build completed successfully on the first controlled attempt with telemetry disabled: Next.js 15.2.4 compiled, linted, type-checked, prerendered all seven static pages, and exited 0 in 2:55.42. Peak build RSS was 385,316 KiB (~376 MiB), with zero swap operations.

Production verification on 2026-10-13 used 3.8 GiB visible RAM, 3.0 GiB swap, and 2 CPUs. `/network`, `/matches`, and `/insights` returned HTTP 200; `/` returned HTTP 307 with `Location: /network`. The production server's rewrite proxy returned live FastAPI health, overview, job, and candidate data. The FastAPI regression suite passed 43/43, and the production DuckDB SHA-256 remained `b2314da8faf5aea8ad8643a1790c96ce7b116bb0ce544473883f45e37f889160` at that milestone.

## Interactive graph explorer

M8-MIGRATE-04 adds `@xyflow/react` 12.12.0 and replaces the network foundation with a bounded, read-only graph explorer. It starts from the first deterministic synthetic candidate with competencies, loads `/api/graph/neighborhood` with `hops=1` and `limit=35`, and expands a selected node to at most two hops. Candidate, technical competency, and job nodes use restrained colors; `REQUIRES_SKILL` is solid and `PREFERS_SKILL` is dashed. Incidental, negated, ambiguous, and unsupported evidence never enters the rendered graph.

Launch locally with the FastAPI command above, then run `npm run dev` in `frontend/`. Use the candidate selector or graph search, select nodes for contextual details, use Expand for a bounded neighborhood, Reset to restore the initial view, and follow a candidate action to Discover Matches. React Flow provides pan, wheel zoom, fit-to-view, minimap, and keyboard-accessible controls. Browser automation was unavailable; automated API, type, lint, build, and regression checks are recorded in the agent validation log.

The M8-MIGRATE-04B readability pass keeps the graph visually dominant, removes the workspace label and redundant node subtitles, uses dark text on light node cards, simplifies the toolbar to candidate/search/expand/reset, and keeps IDs/provenance inside an optional Evidence details disclosure. Candidate, skill, and job details show readable names and connected skills; validated required/preferred evidence remains unchanged.

## Release-readiness verification

The three routes build successfully and use the read-only FastAPI service. Current coverage is 1,500 sampled jobs, 300 synthetic candidates, 80 jobs with required technical evidence, 7 preferred-only, 44 non-required-only, and 1,369 with no eligible technical evidence. Browser automation is unavailable in the current environment; manual interaction checks remain required.

## M8-MIGRATE-05 matches refinement

Discover Matches presents compact expandable comparison rows. Candidate selection, title/company search, observed-overlap or observed-required-skill sorting, and an explicit comparable-only filter use the existing `/api/matches` response without changing scoring semantics. Required-skill counts are primary; overlap percentages are secondary, and insufficient evidence remains unavailable rather than numeric. Native scrollbars use light/dark theme-aware colors on page and internal scroll containers.

## M8-POLISH-02 presentation pass

The frontend uses a Lato-first system font stack, professional role-family labels, consistent control sizing, and a compact candidate-to-job comparison workspace. Matches use observed required-skill counts as the primary signal, with matched/missing/preferred skill chips and expandable evidence limitations. Explore Network graph behavior and M7 matching semantics are unchanged.

## M8-POLISH-03 split view

Discover Matches uses a selectable, scrollable job list beside a comparison detail panel. The detail view separates overview, matched/missing required skills, preferred skills, and evidence limitations. React Flow edges no longer render the redundant floating `preferred` text label; their relationship descriptions remain accessible and the edge styles and legend preserve required/preferred meaning.

## M8-FRONTEND-FINAL-01 dashboard and theme audit

Light and dark colors now come from shared theme tokens. The previous light-mode mismatch was caused by dark navy `--match-*` values in the default root theme and hardcoded light text in comparison components. The split view retains independent scrolling and clear selection/focus states; technical explanation stays in the evidence disclosure. The job-node action was removed because Discover Matches only accepts candidate context; candidate links still pass the selected candidate ID. Explore Network keeps candidate selection separate from temporary expanded graph roots, so Reset returns to the selected candidate and search does not empty the selector.

Insights uses live `/api/overview` coverage for four KPI cards and a four-group donut. The groups are mutually exclusive: 80 required, 7 preferred-only, 44 non-required-only, and 1,369 without eligible technical evidence, totaling 1,500 sampled jobs. The 1,420 jobs lacking required evidence is a separate measure and must not be confused with the 1,369 without any eligible evidence. The frequency chart uses `/api/insights/skill-frequency`: distinct sampled jobs per canonical technical competency with required or preferred evidence, not candidate-profile counts. Current top values include SQL 42 and Python 35; these are observations in this sample, not labor-market estimates. The 300 candidates are fictional, and observed overlap is not hiring suitability.

The chart uses lightweight SVG/CSS and visible counts, percentages, labels, and native tooltips; no chart dependency was added. Browser-level visual and interaction checks remain manual at 1366×768 and 1920×1080 in both themes. Check theme persistence and system preference, split-view selection/filter/scroll behavior, candidate navigation, graph expansion/show-more/zoom/minimap, chart labels and tooltips, and browser console/hydration warnings. Automated results are in `agent/VALIDATION.md`.
