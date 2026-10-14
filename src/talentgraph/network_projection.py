"""Build a small, auditable graph projection for the dashboard."""

from __future__ import annotations

from typing import Any


def build_projection(data: dict[str, Any], candidate_key: str, hop_limit: int = 2) -> dict[str, Any]:
    """Return candidate/skill/job nodes and verified evidence edges only."""
    candidates = {row["candidate_key"]: row for row in data["reference"]["candidates"]}
    candidate = candidates[candidate_key]
    names = data["reference"]["skill_names"]
    skills = set(candidate["skills"])
    evidence = data["reference"]["job_evidence"]
    jobs = {row["job_key"]: row for row in data["jobs"]}
    edges: set[tuple[str, str, str]] = set()
    connected_jobs: set[str] = set()
    for job_key, item in evidence.items():
        required = set(item.get("required", {})) & skills
        preferred = set(item.get("preferred", {})) & skills
        for skill in sorted(required):
            connected_jobs.add(job_key)
            edges.add((candidate_key, skill, "has_skill"))
            edges.add((job_key, skill, "requires_skill"))
        for skill in sorted(preferred - required):
            connected_jobs.add(job_key)
            edges.add((job_key, skill, "prefers_skill"))
    selected_jobs = sorted(connected_jobs)[:24]
    selected = {key for key in selected_jobs if key in jobs}
    nodes = [{"id": candidate_key, "type": "candidate", "label": candidate["fictional_name"]}]
    nodes.extend({"id": key, "type": "skill", "label": names.get(key, key)} for key in sorted(skills))
    nodes.extend({"id": key, "type": "job", "label": jobs[key].get("title") or "Untitled job"} for key in selected)
    rendered_edges = [{"source": source, "target": target, "kind": kind} for source, target, kind in sorted(edges)]
    return {"nodes": nodes, "edges": [edge for edge in rendered_edges if edge["source"] in selected or edge["source"] == candidate_key], "hop_limit": hop_limit}


def readable_nodes(projection: dict[str, Any]) -> list[tuple[str, str]]:
    """Return stable node choices for Streamlit controls."""
    return [(node["id"], f"{node['type'].title()}: {node['label']}") for node in projection["nodes"]]
