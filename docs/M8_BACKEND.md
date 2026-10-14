# M8 FastAPI backend

## Run locally

From the repository root, using the TalentGraph virtual environment:

```bash
PYTHONPATH=src /home/developer/venvs/talentgraph/bin/uvicorn talentgraph.api:app --app-dir src --reload
```

The service is read-only. It loads the M6 synthetic candidate artifact, canonical `m7-evidence-v2` evidence, and job metadata from production DuckDB using read-only connections. It does not run Spark, rebuild artifacts, or write to DuckDB.

## Endpoints

- `GET /api/health`
- `GET /api/overview`
- `GET /api/insights/skill-frequency`
- `GET /api/jobs?q=&evidence_status=&limit=&offset=`
- `GET /api/jobs/{job_id}`
- `GET /api/candidates?q=&role_family=&seniority=&limit=&offset=`
- `GET /api/candidates/{candidate_id}`
- `GET /api/matches?candidate_id=...` or `?job_id=...`
- `GET /api/graph/neighborhood?node_id=...&hops=1&limit=...`

Matching delegates to M7. `required_skill_overlap` is null when evidence is insufficient and is never a suitability or hiring-probability measure. Graph requirement edges use only `required` or `preferred` canonical evidence; incidental, negated, ambiguous, and broad legacy category relationships are not promoted.

The skill-frequency endpoint counts distinct sampled jobs with validated required or preferred technical evidence for each canonical competency. It excludes non-required and unsupported evidence, and does not count duplicate evidence rows for the same job and competency. The endpoint is read-only and reuses the existing M7 evidence index. Streamlit was retired in M8-MIGRATE-02.
