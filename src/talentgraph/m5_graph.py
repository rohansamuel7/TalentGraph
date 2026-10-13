"""Deterministic, explainable NetworkX graph over the M4 DuckDB models."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable

import duckdb
import networkx as nx


def _node(kind: str, key: str) -> str:
    return f"{kind.lower()}:{key}"


def build_graph(database: Path) -> nx.DiGraph:
    """Build a typed graph using only explicit M3/M4 keys and relationships."""
    graph = nx.DiGraph()
    con = duckdb.connect(str(database), read_only=True)
    try:
        for key, name, count in con.execute("SELECT company_key, company_name, posting_count FROM dim_company ORDER BY company_key").fetchall():
            graph.add_node(_node("Company", key), node_type="Company", company_key=key, name=name, posting_count=count)
        for key, name, count in con.execute("SELECT location_key, location_name, posting_count FROM dim_location ORDER BY location_key").fetchall():
            graph.add_node(_node("Location", key), node_type="Location", location_key=key, name=name, posting_count=count)
        for key, name, category, aliases, version, provenance in con.execute("SELECT skill_key, canonical_name, category, aliases_json, taxonomy_version, provenance FROM dim_skill ORDER BY skill_key").fetchall():
            graph.add_node(_node("Skill", key), node_type="Skill", skill_key=key, name=name, category=category, aliases_json=aliases, taxonomy_version=version, provenance=provenance)
        for row in con.execute("SELECT job_key, title, company_key, location_key, source_file, source_row_number, ingestion_run_id, raw_record_hash FROM fact_job_posting ORDER BY job_key").fetchall():
            job, title, company, location, source_file, row_number, run_id, record_hash = row
            job_node = _node("Job", job)
            graph.add_node(job_node, node_type="Job", job_key=job, title=title, source_file=source_file, source_row_number=row_number, ingestion_run_id=run_id, raw_record_hash=record_hash)
            graph.add_edge(job_node, _node("Company", company), relationship="POSTED_BY")
            graph.add_edge(job_node, _node("Location", location), relationship="LOCATED_IN")
        for relationship_key, job, skill, abbreviation, method, confidence, source_file, source_definition, version in con.execute("SELECT relationship_key, job_key, skill_key, source_skill_abbreviation, match_method, confidence, source_mapping_file, source_definition_file, taxonomy_version FROM bridge_job_skill ORDER BY relationship_key").fetchall():
            graph.add_edge(_node("Job", job), _node("Skill", skill), relationship="REQUIRES_SKILL", relationship_key=relationship_key, source_skill_abbreviation=abbreviation, match_method=method, confidence=confidence, source_mapping_file=source_file, source_definition_file=source_definition, taxonomy_version=version)
    finally:
        con.close()
    return graph


def graph_summary(graph: nx.DiGraph) -> dict[str, object]:
    nodes = sorted((n, graph.nodes[n].get("node_type")) for n in graph.nodes)
    edges = sorted((u, v, graph.edges[u, v].get("relationship")) for u, v in graph.edges)
    digest = hashlib.sha256(json.dumps([nodes, edges], separators=(",", ":")).encode()).hexdigest()
    return {"nodes": graph.number_of_nodes(), "edges": graph.number_of_edges(), "node_types": dict(sorted((t, sum(1 for _, d in graph.nodes(data=True) if d.get("node_type") == t)) for t in {d.get("node_type") for _, d in graph.nodes(data=True)})), "edge_types": dict(sorted((t, sum(1 for _, _, d in graph.edges(data=True) if d.get("relationship") == t)) for t in {d.get("relationship") for _, _, d in graph.edges(data=True)})), "summary_sha256": digest}


def most_required_skills(graph: nx.DiGraph, limit: int = 10) -> list[tuple[str, int]]:
    counts = [(graph.nodes[n]["name"], graph.in_degree(n)) for n, d in graph.nodes(data=True) if d.get("node_type") == "Skill"]
    return sorted(counts, key=lambda x: (-x[1], x[0]))[:limit]


def companies_requesting_skill(graph: nx.DiGraph, skill_key: str) -> list[str]:
    skill = _node("Skill", skill_key)
    companies = {graph.nodes[company].get("name") for job in graph.predecessors(skill) if graph.nodes[job].get("node_type") == "Job" for _, company, data in graph.out_edges(job, data=True) if data.get("relationship") == "POSTED_BY" and graph.nodes[company].get("name") is not None}
    return sorted(companies)


def cooccurring_skills(graph: nx.DiGraph, limit: int = 10) -> list[tuple[tuple[str, str], int]]:
    counts: dict[tuple[str, str], int] = {}
    for job, data in graph.nodes(data=True):
        if data.get("node_type") != "Job": continue
        skills = sorted(graph.nodes[s]["name"] for s in graph.successors(job) if graph.nodes[s].get("node_type") == "Skill")
        for i, left in enumerate(skills):
            for right in skills[i + 1:]: counts[(left, right)] = counts.get((left, right), 0) + 1
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:limit]


def jobs_with_skills(graph: nx.DiGraph, skill_keys: Iterable[str]) -> list[str]:
    required = {_node("Skill", key) for key in skill_keys}
    return sorted(job for job, data in graph.nodes(data=True) if data.get("node_type") == "Job" and required <= {s for s in graph.successors(job)})


def jobs_without_explicit_skills(graph: nx.DiGraph) -> int:
    return sum(1 for job, data in graph.nodes(data=True) if data.get("node_type") == "Job" and not any(graph.nodes[s].get("node_type") == "Skill" for s in graph.successors(job)))


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--database", type=Path, default=Path("/home/developer/talentgraph_data/talentgraph.duckdb")); args = parser.parse_args()
    graph = build_graph(args.database)
    print(json.dumps({"summary": graph_summary(graph), "top_skills": most_required_skills(graph), "no_skill_jobs": jobs_without_explicit_skills(graph)}, indent=2, sort_keys=True))


if __name__ == "__main__": main()
