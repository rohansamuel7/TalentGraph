"""Evidence-aware, deterministic technical competency matching."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import duckdb

from .m7_evidence import load_job_evidence

EVIDENCE_PATH = Path("data/processed/job_competency_evidence_qa_fix04.json")
FORMULA = "matched required competencies / observed required competencies; not suitability or hiring probability"
STATUS_RANK = {"sufficient_for_limited_comparison": 0, "limited_evidence": 1, "insufficient_evidence": 2}


def load_reference_data(database: Path, candidates_path: Path, evidence_path: Path = EVIDENCE_PATH) -> tuple[list[dict[str, Any]], dict[str, set[str]], dict[str, dict[str, Any]]]:
    """Load jobs, synthetic candidates, and eligible evidence read-only."""
    artifact = json.loads(candidates_path.read_text(encoding="utf-8"))
    candidate_skills = {candidate["candidate_key"]: set(candidate["skills"]) for candidate in artifact["candidates"]}
    con = duckdb.connect(str(database), read_only=True)
    try:
        jobs = [{"job_key": row[0], "title": row[1], "company_name": row[2]} for row in con.execute("SELECT job_key, title, company_name FROM fact_job_posting ORDER BY job_key").fetchall()]
        names = {row[0]: row[1] for row in con.execute("SELECT skill_key, canonical_name FROM dim_skill").fetchall()}
        categories = {row[0]: row[1] for row in con.execute("SELECT skill_key, category FROM dim_skill").fetchall()}
    finally:
        con.close()
    return jobs, candidate_skills, {"skill_names": names, "job_evidence": load_job_evidence(evidence_path, categories), "candidates": artifact["candidates"]}


def _names(keys: set[str], names: dict[str, str]) -> list[str]:
    """Return stable display names."""
    return [names.get(key, key) for key in sorted(keys, key=lambda value: names.get(value, value))]


def score_candidate_job(candidate_key: str, candidate_skills: set[str], job: dict[str, Any], evidence: dict[str, Any], skill_names: dict[str, str]) -> dict[str, Any]:
    """Score observed required overlap and report optional evidence separately."""
    required = set(evidence.get("required", {})); preferred = set(evidence.get("preferred", {}))
    matched_required = candidate_skills & required; missing_required = required - candidate_skills
    matched_preferred = candidate_skills & preferred; missing_preferred = preferred - candidate_skills
    # No observed required evidence cannot support a zero-overlap judgment.
    # Preferred matches stay separate from the required-skill denominator.
    if not required:
        status, overlap = "insufficient_evidence", None
    elif len(required) == 1:
        status, overlap = "limited_evidence", len(matched_required) / len(required)
    else:
        status, overlap = "sufficient_for_limited_comparison", len(matched_required) / len(required)
    source_versions = sorted({item["version"] for item in (*evidence.get("required", {}).values(), *evidence.get("preferred", {}).values())})
    sources = sorted({item["source"] for item in (*evidence.get("required", {}).values(), *evidence.get("preferred", {}).values())})
    return {"candidate_key": candidate_key, "job_key": job["job_key"], "title": job.get("title"), "company_name": job.get("company_name"), "evidence_status": status, "required_skill_count": len(required), "matched_required_count": len(matched_required), "required_skill_overlap": overlap, "matched_skill_keys": sorted(matched_required), "matched_skills": _names(matched_required, skill_names), "missing_skill_keys": sorted(missing_required), "missing_skills": _names(missing_required, skill_names), "preferred_skill_count": len(preferred), "matched_preferred_count": len(matched_preferred), "matched_preferred_skills": _names(matched_preferred, skill_names), "missing_preferred_skills": _names(missing_preferred, skill_names), "evidence_source": sources, "extraction_version": source_versions, "explanation": (f"{len(matched_required)} of {len(required)} observed required competencies matched; this measures extracted-skill overlap only" if required else "No eligible extracted required competencies; suitability is not scored")}


def _rank_key(row: dict[str, Any]) -> tuple[Any, ...]:
    """Order usable evidence before insufficient evidence."""
    return (STATUS_RANK[row["evidence_status"]], -(row["required_skill_overlap"] or -1), -row["required_skill_count"], -row["matched_preferred_count"], row["job_key"])


def rank_jobs_for_candidate(candidate_key: str, jobs: list[dict[str, Any]], candidate_skills: dict[str, set[str]], reference: dict[str, Any], top_k: int = 10) -> list[dict[str, Any]]:
    """Rank jobs, with insufficient-evidence rows clearly marked last."""
    rows = [score_candidate_job(candidate_key, candidate_skills[candidate_key], job, reference["job_evidence"].get(job["job_key"], {}), reference["skill_names"]) for job in jobs]
    return sorted(rows, key=_rank_key)[:top_k]


def rank_candidates_for_job(job_key: str, jobs: list[dict[str, Any]], candidate_skills: dict[str, set[str]], reference: dict[str, Any], top_k: int = 10) -> list[dict[str, Any]]:
    """Rank candidates against one job using the same evidence rules."""
    job = next(job for job in jobs if job["job_key"] == job_key)
    evidence = reference["job_evidence"].get(job_key, {})
    rows = [score_candidate_job(key, skills, job, evidence, reference["skill_names"]) for key, skills in candidate_skills.items()]
    return sorted(rows, key=lambda row: (STATUS_RANK[row["evidence_status"]], -(row["required_skill_overlap"] or -1), -row["required_skill_count"], -row["matched_preferred_count"], row["candidate_key"]))[:top_k]


def main() -> None:
    """Run a candidate-to-job evidence-aware ranking query."""
    parser = argparse.ArgumentParser(); parser.add_argument("--database", type=Path, default=Path("/home/developer/talentgraph_data/talentgraph.duckdb")); parser.add_argument("--candidates", type=Path, default=Path("data/processed/synthetic_candidates.json")); parser.add_argument("--candidate", default="synthetic:candidate:000001"); parser.add_argument("--top-k", type=int, default=5); args = parser.parse_args()
    jobs, candidates, reference = load_reference_data(args.database, args.candidates)
    print(json.dumps({"formula": FORMULA, "recommendations": rank_jobs_for_candidate(args.candidate, jobs, candidates, reference, args.top_k)}, indent=2, sort_keys=True))


if __name__ == "__main__": main()
