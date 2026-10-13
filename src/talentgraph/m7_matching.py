"""Deterministic, skill-overlap-only candidate-to-job matching."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import duckdb

FORMULA = "matched_explicit_skills / total_explicit_job_skills; zero when evidence is absent"


def load_reference_data(database: Path, candidates_path: Path) -> tuple[list[dict[str, Any]], dict[str, set[str]], dict[str, dict[str, Any]]]:
    candidates_artifact = json.loads(candidates_path.read_text(encoding="utf-8"))
    candidate_skills: dict[str, set[str]] = {c["candidate_key"]: set(c["skills"]) for c in candidates_artifact["candidates"]}
    con = duckdb.connect(str(database), read_only=True)
    try:
        jobs = [{"job_key": r[0], "title": r[1], "company_name": r[2]} for r in con.execute("SELECT job_key, title, company_name FROM fact_job_posting ORDER BY job_key").fetchall()]
        skills: dict[str, set[str]] = {job: set() for job in (j["job_key"] for j in jobs)}
        for job, skill in con.execute("SELECT job_key, skill_key FROM bridge_job_skill ORDER BY job_key, skill_key").fetchall():
            skills.setdefault(job, set()).add(skill)
        names = {r[0]: r[1] for r in con.execute("SELECT skill_key, canonical_name FROM dim_skill").fetchall()}
    finally:
        con.close()
    return jobs, candidate_skills, {"skill_names": names, "job_skills": skills, "candidates": candidates_artifact["candidates"]}


def score_candidate_job(candidate_key: str, candidate_skills: set[str], job: dict[str, Any], required: set[str], skill_names: dict[str, str]) -> dict[str, Any]:
    matched = sorted(candidate_skills & required, key=lambda key: skill_names.get(key, key))
    missing = sorted(required - candidate_skills, key=lambda key: skill_names.get(key, key))
    if not required:
        status, score = "insufficient_skill_evidence", 0.0
    else:
        status, score = "scored", len(matched) / len(required)
    return {"candidate_key": candidate_key, "job_key": job["job_key"], "title": job.get("title"), "company_name": job.get("company_name"),
            "skill_coverage": score, "matched_skill_keys": matched, "matched_skills": [skill_names.get(k, k) for k in matched],
            "missing_skill_keys": missing, "missing_skills": [skill_names.get(k, k) for k in missing],
            "required_skill_count": len(required), "matched_skill_count": len(matched), "evidence_status": status,
            "explanation": (f"{len(matched)} of {len(required)} explicit job skills matched" if required else "No explicit job-skill evidence; coverage is not awarded")}


def rank_jobs_for_candidate(candidate_key: str, jobs: list[dict[str, Any]], candidate_skills: dict[str, set[str]], reference: dict[str, Any], top_k: int = 10) -> list[dict[str, Any]]:
    results = [score_candidate_job(candidate_key, candidate_skills[candidate_key], job, reference["job_skills"].get(job["job_key"], set()), reference["skill_names"]) for job in jobs]
    return sorted(results, key=lambda r: (-r["skill_coverage"], r["job_key"]))[:top_k]


def rank_candidates_for_job(job_key: str, jobs: list[dict[str, Any]], candidate_skills: dict[str, set[str]], reference: dict[str, Any], top_k: int = 10) -> list[dict[str, Any]]:
    job = next(job for job in jobs if job["job_key"] == job_key)
    rows = [score_candidate_job(key, skills, job, reference["job_skills"].get(job_key, set()), reference["skill_names"]) for key, skills in candidate_skills.items()]
    return sorted(rows, key=lambda r: (-r["skill_coverage"], r["candidate_key"]))[:top_k]


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--database", type=Path, default=Path("/home/developer/talentgraph_data/talentgraph.duckdb")); parser.add_argument("--candidates", type=Path, default=Path("data/processed/synthetic_candidates.json")); parser.add_argument("--candidate", default="synthetic:candidate:000001"); parser.add_argument("--top-k", type=int, default=5); args = parser.parse_args()
    jobs, candidate_skills, reference = load_reference_data(args.database, args.candidates)
    print(json.dumps({"formula": FORMULA, "recommendations": rank_jobs_for_candidate(args.candidate, jobs, candidate_skills, reference, args.top_k)}, indent=2, sort_keys=True))


if __name__ == "__main__": main()
