"""Pure response shaping for the FastAPI routes."""

from __future__ import annotations

from typing import Any

from .api_models import CandidateSummary, Evidence, GraphEdge, GraphNode, JobSummary, Match
from .api_store import Store


def job_summary(store: Store, job: dict[str, Any]) -> JobSummary:
    """Build a readable job summary."""
    evidence = store.reference["job_evidence"].get(job["job_key"], {})
    status = "required" if evidence.get("required") else "preferred_only" if evidence.get("preferred") else "insufficient_evidence"
    return JobSummary(job_id=job["job_key"], title=job.get("title") or "Untitled job", company_name=job.get("company_name") or "Company not listed", location=job.get("location"), evidence_status=status)


def candidate_summary(row: dict[str, Any]) -> CandidateSummary:
    """Build a readable synthetic candidate summary."""
    return CandidateSummary(candidate_id=row["candidate_key"], display_name=row["fictional_name"], role_family=row["role_family"], seniority=row["experience_level"], competency_count=len(row["skills"]))


def evidence_item(store: Store, row: dict[str, Any]) -> Evidence:
    """Preserve canonical evidence and source provenance."""
    return Evidence(competency_id=row["competency_id"], competency_name=row["competency_name"], classification=row["classification"], evidence_text=row["evidence_text"], source=row["evidence_source"], extraction_rule=row["extraction_rule_id"], extraction_version=row["extraction_version"], source_description_sha256=row["source_description_sha256"], source_location={"source_file": row.get("source_file"), "source_row_number": row.get("source_row_number")})


def match_item(row: dict[str, Any]) -> Match:
    """Expose M7 output without recalculating or relabeling it."""
    return Match(candidate_id=row["candidate_key"], job_id=row["job_key"], title=row.get("title") or "Untitled job", company_name=row.get("company_name") or "Company not listed", evidence_status=row["evidence_status"], required_skill_count=row["required_skill_count"], matched_required_count=row["matched_required_count"], required_skill_overlap=row["required_skill_overlap"], matched_skills=row["matched_skills"], missing_skills=row["missing_skills"], matched_preferred_skills=row["matched_preferred_skills"], evidence_source=row["evidence_source"], extraction_version=row["extraction_version"], explanation=row["explanation"])


def graph_nodes(store: Store, candidate_id: str, job_id: str | None = None) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Build a bounded candidate-centered projection with provenance edges."""
    candidate = store.candidate(candidate_id)
    if not candidate:
        return [], []
    skill_ids = set(candidate["skills"])
    nodes = [GraphNode(id=candidate_id, type="candidate", label=candidate["fictional_name"], properties={"role_family": candidate["role_family"], "synthetic": True})]
    for skill in sorted(skill_ids):
        nodes.append(GraphNode(id=skill, type="competency", label=store.reference["skill_names"].get(skill, skill)))
    edges = [GraphEdge(source=candidate_id, target=skill, relationship="HAS_SKILL") for skill in sorted(skill_ids)]
    jobs = [store.job(job_id)] if job_id else store.jobs
    for job in sorted((item for item in jobs if item), key=lambda item: item["job_key"]):
        rows = [row for row in store.evidence_rows(job["job_key"]) if row["competency_id"] in skill_ids and row["classification"] in {"required", "preferred"}]
        if not rows:
            continue
        nodes.append(GraphNode(id=job["job_key"], type="job", label=job.get("title") or "Untitled job", properties={"company_name": job.get("company_name") or "Company not listed"}))
        for row in sorted(rows, key=lambda value: (value["competency_id"], value["classification"])):
            relationship = "REQUIRES_SKILL" if row["classification"] == "required" else "PREFERS_SKILL"
            edges.append(GraphEdge(source=job["job_key"], target=row["competency_id"], relationship=relationship, classification=row["classification"], provenance={"source": row["evidence_source"], "source_file": row.get("source_file"), "source_row_number": row.get("source_row_number"), "extraction_rule": row["extraction_rule_id"], "extraction_version": row["extraction_version"], "source_description_sha256": row["source_description_sha256"]}))
    return nodes, edges


def graph_root(store: Store, node_id: str) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Resolve candidate or job roots without changing graph semantics."""
    if store.candidate(node_id):
        return graph_nodes(store, node_id)
    job = store.job(node_id)
    if not job and node_id in store.reference["skill_names"]:
        label = store.reference["skill_names"][node_id]
        nodes = [GraphNode(id=node_id, type="competency", label=label)]
        edges: list[GraphEdge] = []
        for item in store.jobs:
            rows = [row for row in store.evidence_rows(item["job_key"]) if row["competency_id"] == node_id and row["classification"] in {"required", "preferred"}]
            if rows:
                nodes.append(GraphNode(id=item["job_key"], type="job", label=item.get("title") or "Untitled job"))
                edges.extend(GraphEdge(source=item["job_key"], target=node_id, relationship="REQUIRES_SKILL" if row["classification"] == "required" else "PREFERS_SKILL", classification=row["classification"]) for row in rows)
        return nodes, edges
    if not job:
        return [], []
    rows = [row for row in store.evidence_rows(node_id) if row["classification"] in {"required", "preferred"}]
    skills = sorted({row["competency_id"] for row in rows})
    nodes = [GraphNode(id=node_id, type="job", label=job.get("title") or "Untitled job", properties={"company_name": job.get("company_name") or "Company not listed"})]
    nodes.extend(GraphNode(id=skill, type="competency", label=store.reference["skill_names"].get(skill, skill)) for skill in skills)
    edges = [GraphEdge(source=node_id, target=row["competency_id"], relationship="REQUIRES_SKILL" if row["classification"] == "required" else "PREFERS_SKILL", classification=row["classification"], provenance={"source": row["evidence_source"], "extraction_version": row["extraction_version"], "source_description_sha256": row["source_description_sha256"]}) for row in rows]
    return nodes, edges
