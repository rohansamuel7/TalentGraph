"""Read-only application store built on existing M6/M7 interfaces."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import duckdb

from .api_data import coverage_counts, load_dataset, search_jobs, technical_skill_frequency
from .m7_matching import load_reference_data, rank_candidates_for_job, rank_jobs_for_candidate


ROOT = Path(__file__).resolve().parents[2]
DATABASE = Path("/home/developer/talentgraph_data/talentgraph.duckdb")
CANDIDATES = ROOT / "data/processed/synthetic_candidates.json"
EVIDENCE = ROOT / "data/processed/job_competency_evidence_qa_fix04.json"


class Store:
    """Load validated immutable artifacts once per backend process."""

    def __init__(self) -> None:
        dataset = load_dataset(DATABASE, CANDIDATES, EVIDENCE)
        self.jobs, self.candidate_skills, self.reference = dataset["jobs"], dataset["candidate_skills"], dataset["reference"]
        self._add_locations()
        self.candidates = {row["candidate_key"]: row for row in self.reference["candidates"]}
        artifact = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.raw_evidence = artifact["relationships"]
        if artifact.get("schema_version") != "m7-evidence-v2":
            raise ValueError("Incompatible canonical evidence schema")

    def _add_locations(self) -> None:
        """Add read-only display metadata without changing M7 records."""
        # API serving may read the modeled warehouse; writes belong to the
        # separate preparation workflow, never to a request path.
        con = duckdb.connect(str(DATABASE), read_only=True)
        try:
            rows = con.execute("SELECT job_key, location FROM fact_job_posting ORDER BY job_key").fetchall()
        finally:
            con.close()
        locations = dict(rows)
        for job in self.jobs:
            job["location"] = locations.get(job["job_key"])

    def job(self, job_id: str) -> dict[str, Any] | None:
        """Find one stable job record."""
        return next((row for row in self.jobs if row["job_key"] == job_id), None)

    def candidate(self, candidate_id: str) -> dict[str, Any] | None:
        """Find one stable candidate record."""
        return self.candidates.get(candidate_id)

    def evidence_rows(self, job_id: str) -> list[dict[str, Any]]:
        """Return all canonical evidence rows for one job."""
        return [row for row in self.raw_evidence if row["job_key"] == job_id]

    def coverage(self) -> dict[str, int]:
        """Return mutually exclusive evidence coverage counts."""
        return coverage_counts({"jobs": self.jobs, "reference": self.reference})

    def skill_frequency(self, limit: int = 8) -> list[dict[str, Any]]:
        """Return read-only job counts from validated M7 technical evidence."""
        return technical_skill_frequency(self.jobs, self.reference, limit)

    def search(self, query: str, status: str) -> list[dict[str, Any]]:
        """Reuse existing deterministic job filtering semantics."""
        return search_jobs(self.jobs, query, status, self.reference["job_evidence"])

    def candidate_matches(self, candidate_id: str, limit: int) -> list[dict[str, Any]]:
        """Reuse M7 candidate-to-job ranking."""
        return rank_jobs_for_candidate(candidate_id, self.jobs, self.candidate_skills, self.reference, limit)

    def job_matches(self, job_id: str, limit: int) -> list[dict[str, Any]]:
        """Reuse M7 job-to-candidate ranking."""
        return rank_candidates_for_job(job_id, self.jobs, self.candidate_skills, self.reference, limit)
