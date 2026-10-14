"""FastAPI application for the read-only TalentGraph backend."""

from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from .api_models import CandidateSummary, Evidence, GraphResponse, JobSummary, Match, Page
from .api_service import candidate_summary, evidence_item, graph_root, job_summary, match_item
from .api_store import Store


app = FastAPI(title="TalentGraph API", version="m8-migrate-02")
store = Store()
Limit = Annotated[int, Query(ge=1, le=50)]
Offset = Annotated[int, Query(ge=0, le=100000)]


@app.get("/api/health")
def health() -> dict:
    """Report validated artifact readiness."""
    return {"status": "ok", "api_version": app.version, "evidence_version": "qa-fix-04-v1", "artifacts": {"jobs": len(store.jobs), "candidates": len(store.candidates), "database_read_only": True}}


@app.get("/api/overview")
def overview() -> dict:
    """Return sample counts and evidence coverage."""
    return {"sampled_jobs": len(store.jobs), "synthetic_candidates": len(store.candidates), "coverage": store.coverage(), "sample_note": "Deterministic sampled jobs; not statistically representative."}


@app.get("/api/insights/skill-frequency")
def skill_frequency() -> dict:
    """Count sampled jobs with required or preferred technical evidence by skill."""
    return {"items": store.skill_frequency(), "definition": "Distinct sampled jobs with extracted required or preferred technical competency evidence"}


@app.get("/api/jobs")
def jobs(q: str = "", evidence_status: str = "all", limit: Limit = 50, offset: Offset = 0) -> dict:
    """Search jobs with bounded pagination."""
    if evidence_status not in {"all", "required", "preferred_only", "insufficient"}:
        raise HTTPException(422, "Invalid evidence_status")
    rows = store.search(q, evidence_status)
    page = rows[offset:offset + limit]
    return {"items": [job_summary(store, row) for row in page], **Page(total=len(rows), limit=limit, offset=offset).model_dump()}


@app.get("/api/jobs/{job_id}")
def job_detail(job_id: str) -> dict:
    """Return job metadata and complete classified evidence."""
    job = store.job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    rows = [evidence_item(store, row) for row in store.evidence_rows(job_id)]
    return {"job": job_summary(store, job), "required": [row for row in rows if row.classification == "required"], "preferred": [row for row in rows if row.classification == "preferred"], "other_evidence": [row for row in rows if row.classification not in {"required", "preferred"}]}


@app.get("/api/candidates")
def candidates(q: str = "", role_family: str | None = None, seniority: str | None = None, limit: Limit = 50, offset: Offset = 0) -> dict:
    """Search synthetic candidates with bounded pagination."""
    text = q.lower().strip()
    rows = [row for row in store.candidates.values() if (not text or text in f"{row['candidate_key']} {row['fictional_name']}".lower()) and (not role_family or row["role_family"] == role_family) and (not seniority or row["experience_level"] == seniority)]
    rows = sorted(rows, key=lambda row: row["candidate_key"])
    page = rows[offset:offset + limit]
    return {"items": [candidate_summary(row) for row in page], **Page(total=len(rows), limit=limit, offset=offset).model_dump()}


@app.get("/api/candidates/{candidate_id}")
def candidate_detail(candidate_id: str) -> dict:
    """Return one synthetic candidate and canonical competencies."""
    row = store.candidate(candidate_id)
    if not row:
        raise HTTPException(404, "Candidate not found")
    return {"candidate": candidate_summary(row), "competencies": [{"id": skill, "name": store.reference["skill_names"].get(skill, skill)} for skill in sorted(row["skills"])]}


@app.get("/api/matches")
def matches(candidate_id: str | None = None, job_id: str | None = None, limit: Limit = 10) -> dict:
    """Return M7-ranked comparisons for exactly one subject."""
    if (candidate_id is None) == (job_id is None):
        raise HTTPException(422, "Provide exactly one of candidate_id or job_id")
    if candidate_id and not store.candidate(candidate_id):
        raise HTTPException(404, "Candidate not found")
    if job_id and not store.job(job_id):
        raise HTTPException(404, "Job not found")
    rows = store.candidate_matches(candidate_id, limit) if candidate_id else store.job_matches(job_id, limit)
    return {"items": [match_item(row) for row in rows], "limit": limit}


@app.get("/api/graph/neighborhood", response_model=GraphResponse)
def neighborhood(node_id: str, hops: Annotated[int, Query(ge=1, le=2)] = 1, limit: Limit = 50) -> GraphResponse:
    """Return a bounded candidate-centered graph neighborhood."""
    if not store.candidate(node_id) and not store.job(node_id) and node_id not in store.reference["skill_names"]:
        raise HTTPException(404, "Neighborhood root not found")
    nodes, edges = graph_root(store, node_id)
    if hops == 1 and store.candidate(node_id):
        direct = {node_id} | {edge.target for edge in edges if edge.source == node_id}
        nodes = [node for node in nodes if node.id in direct]
        edges = [edge for edge in edges if edge.source in direct and edge.target in direct]
    capped_nodes = nodes[:limit]
    node_ids = {node.id for node in capped_nodes}
    capped_edges = [edge for edge in edges if edge.source in node_ids and edge.target in node_ids][: limit * 4]
    return GraphResponse(root=node_id, nodes=capped_nodes, edges=capped_edges, truncated=len(capped_nodes) < len(nodes) or len(capped_edges) < len(edges))
