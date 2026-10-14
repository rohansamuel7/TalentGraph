"""Shared read-only data queries for the FastAPI backend."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .m7_matching import load_reference_data


def load_dataset(database: Path, candidates: Path, evidence: Path) -> dict[str, Any]:
    """Load and validate the fixed M6/M7 sample through existing APIs."""
    jobs, candidate_skills, reference = load_reference_data(database, candidates, evidence)
    if len(jobs) != 1500 or len(candidate_skills) != 300:
        raise ValueError("Expected 1,500 jobs and 300 synthetic candidates")
    return {"jobs": jobs, "candidate_skills": candidate_skills, "reference": reference}


def coverage_counts(data: dict[str, Any]) -> dict[str, int]:
    """Return mutually exclusive evidence coverage groups."""
    groups = {"required": 0, "preferred_only": 0, "non_required": 0, "insufficient": 0}
    for job in data["jobs"]:
        evidence = data["reference"]["job_evidence"].get(job["job_key"], {})
        if evidence.get("required"):
            groups["required"] += 1
        elif evidence.get("preferred"):
            groups["preferred_only"] += 1
        elif evidence.get("non_scoring"):
            groups["non_required"] += 1
        else:
            groups["insufficient"] += 1
    return groups


def technical_skill_frequency(jobs: list[dict[str, Any]], reference: dict[str, Any], limit: int = 8) -> list[dict[str, Any]]:
    """Count distinct sampled jobs with required or preferred canonical evidence per skill."""
    counts: dict[str, int] = {}
    evidence_by_job = reference["job_evidence"]
    for job in jobs:
        evidence = evidence_by_job.get(job["job_key"], {})
        # A job contributes once per skill even if both eligible classes exist.
        for skill_id in set(evidence.get("required", {})) | set(evidence.get("preferred", {})):
            counts[skill_id] = counts.get(skill_id, 0) + 1
    names = reference["skill_names"]
    ordered = sorted(counts.items(), key=lambda item: (-item[1], names.get(item[0], item[0]), item[0]))
    return [{"competency_id": skill_id, "competency_name": names.get(skill_id, skill_id), "job_count": count} for skill_id, count in ordered[:limit]]


def search_jobs(jobs: list[dict[str, Any]], query: str, status: str, evidence: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Search job metadata using deterministic evidence filters."""
    text = query.lower().strip()
    rows = [job for job in jobs if not text or text in f"{job['job_key']} {job.get('title') or ''} {job.get('company_name') or ''} {job.get('location') or ''}".lower()]
    if status == "all":
        return rows
    def matches(job: dict[str, Any]) -> bool:
        item = evidence.get(job["job_key"], {})
        return {"required": bool(item.get("required")), "preferred_only": bool(item.get("preferred") and not item.get("required")), "insufficient": not item.get("required") and not item.get("preferred")} [status]
    return [job for job in rows if matches(job)]
