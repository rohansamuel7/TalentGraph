"""Controlled taxonomy and explicit job-skill alignment for TalentGraph."""

from __future__ import annotations

import argparse
import csv
import json
import tempfile
import re
import zipfile
from pathlib import Path
from typing import Any

import duckdb
from rapidfuzz import fuzz, process


TAXONOMY_VERSION = "m4-v1"
FUZZY_THRESHOLD = 92
FUZZY_MARGIN = 5

# The source definitions are retained exactly; additional concepts are controlled
# vocabulary entries for later evidence sources and do not create job relationships.
EXTRA_SKILLS = (
    ("python", "Python", "technical", ("python3",)), ("sql", "SQL", "technical", ("structured query language",)),
    ("sql_server", "SQL Server", "technical", ("microsoft sql server",)), ("apache_spark", "Apache Spark", "technical", ("spark",)),
    ("pyspark", "PySpark", "technical", ("python spark",)), ("java", "Java", "technical", ()),
    ("scala", "Scala", "technical", ()), ("aws", "Amazon Web Services", "cloud", ("amazon aws",)),
    ("azure", "Microsoft Azure", "cloud", ()), ("gcp", "Google Cloud Platform", "cloud", ("google cloud",)),
    ("airflow", "Apache Airflow", "data_engineering", ("workflow orchestration",)), ("duckdb", "DuckDB", "data_engineering", ()),
    ("pandas", "Pandas", "technical", ()), ("spark_sql", "Spark SQL", "technical", ()), ("networkx", "NetworkX", "technical", ()),
)


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def match_skill(source_name: str, taxonomy: list[dict[str, Any]]) -> dict[str, Any]:
    """Match a source label deterministically without conflating related skills."""
    normalized = _norm(source_name)
    exact = [s for s in taxonomy if normalized == _norm(s["canonical_name"]) or normalized in s["aliases"]]
    if exact:
        return {"skill_key": exact[0]["skill_key"], "method": "exact_or_alias", "confidence": 1.0, "status": "matched"}
    choices = {s["skill_key"]: s["canonical_name"] for s in taxonomy}
    candidates = process.extract(normalized, choices, scorer=fuzz.token_set_ratio, limit=2)
    if candidates and candidates[0][1] >= FUZZY_THRESHOLD and (len(candidates) == 1 or candidates[0][1] - candidates[1][1] >= FUZZY_MARGIN):
        return {"skill_key": candidates[0][2], "method": "fuzzy", "confidence": candidates[0][1] / 100, "status": "matched"}
    return {"skill_key": None, "method": "unmatched", "confidence": 0.0, "status": "unknown"}


def _source_data(archive: Path, accepted: set[str]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    with zipfile.ZipFile(archive) as z:
        with z.open("mappings/skills.csv") as stream:
            definitions = list(csv.DictReader(__import__("io").TextIOWrapper(stream, encoding="utf-8-sig", newline="")))
        with z.open("jobs/job_skills.csv") as stream:
            mappings = [r for r in csv.DictReader(__import__("io").TextIOWrapper(stream, encoding="utf-8-sig", newline="")) if r["job_id"] in accepted]
    return definitions, mappings


def build_skill_models(archive: Path, database: Path, sql_dir: Path | None = None) -> dict[str, Any]:
    sql_dir = sql_dir or Path("sql")
    con = duckdb.connect(str(database))
    try:
        con.execute("SET memory_limit='1GB'"); con.execute("SET threads=2")
        accepted = {r[0] for r in con.execute("SELECT source_job_id FROM fact_job_posting").fetchall()}
        definitions, mappings = _source_data(archive, accepted)
        taxonomy: list[dict[str, Any]] = []
        categories = {"Engineering": "business", "Information Technology": "technical", "Science": "technical", "Research": "technical", "Quality Assurance": "technical", "Accounting/Auditing": "business", "Finance": "business", "Manufacturing": "operations", "Production": "operations", "Supply Chain": "operations", "Distribution": "operations", "Other": "other"}
        for d in definitions:
            key = "skill:source:" + d["skill_abr"].lower()
            taxonomy.append({"skill_key": key, "canonical_name": d["skill_name"], "category": categories.get(d["skill_name"], "business"), "aliases": [_norm(d["skill_abr"]), _norm(d["skill_name"])]})
        for key, name, category, aliases in EXTRA_SKILLS:
            taxonomy.append({"skill_key": "skill:" + key, "canonical_name": name, "category": category, "aliases": [_norm(a) for a in aliases]})
        rows = []
        by_abr = {d["skill_abr"]: d for d in definitions}
        for m in mappings:
            definition = by_abr[m["skill_abr"]]
            result = match_skill(definition["skill_name"], taxonomy)
            rows.append(("jobskill:" + m["job_id"] + ":" + m["skill_abr"], "linkedin:" + m["job_id"], m["skill_abr"], definition["skill_name"], result["skill_key"], result["method"], result["confidence"], "jobs/job_skills.csv", "mappings/skills.csv", TAXONOMY_VERSION))
        con.execute("DROP TABLE IF EXISTS dim_skill"); con.execute("DROP TABLE IF EXISTS bridge_job_skill")
        con.execute("CREATE TABLE dim_skill(skill_key VARCHAR PRIMARY KEY, canonical_name VARCHAR NOT NULL, category VARCHAR NOT NULL, aliases_json VARCHAR NOT NULL, taxonomy_version VARCHAR NOT NULL, provenance VARCHAR NOT NULL)")
        con.executemany("INSERT INTO dim_skill VALUES (?, ?, ?, ?, ?, ?)", [(s["skill_key"], s["canonical_name"], s["category"], json.dumps(s["aliases"], sort_keys=True), TAXONOMY_VERSION, "controlled_taxonomy:m4") for s in taxonomy])
        con.execute("CREATE TABLE bridge_job_skill(relationship_key VARCHAR PRIMARY KEY, job_key VARCHAR NOT NULL, source_skill_abbreviation VARCHAR NOT NULL, source_skill_name VARCHAR NOT NULL, skill_key VARCHAR, match_method VARCHAR NOT NULL, confidence DOUBLE NOT NULL, source_mapping_file VARCHAR NOT NULL, source_definition_file VARCHAR NOT NULL, taxonomy_version VARCHAR NOT NULL)")
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".csv", delete=False) as bridge_file:
            writer = csv.writer(bridge_file)
            writer.writerow(["relationship_key", "job_key", "source_skill_abbreviation", "source_skill_name", "skill_key", "match_method", "confidence", "source_mapping_file", "source_definition_file", "taxonomy_version"])
            writer.writerows(rows)
            bridge_path = bridge_file.name
        try:
            con.execute("INSERT INTO bridge_job_skill SELECT * FROM read_csv(?, header=true, columns={" +
                        "'relationship_key':'VARCHAR','job_key':'VARCHAR','source_skill_abbreviation':'VARCHAR'," +
                        "'source_skill_name':'VARCHAR','skill_key':'VARCHAR','match_method':'VARCHAR','confidence':'DOUBLE'," +
                        "'source_mapping_file':'VARCHAR','source_definition_file':'VARCHAR','taxonomy_version':'VARCHAR'})", [bridge_path])
        finally:
            Path(bridge_path).unlink(missing_ok=True)
        con.execute("CREATE OR REPLACE VIEW vw_skill_coverage AS SELECT count(DISTINCT job_key) AS jobs_with_skills, (SELECT count(*) FROM fact_job_posting) AS total_jobs, count(*) AS bridge_rows, count(DISTINCT source_skill_abbreviation) AS source_skill_count FROM bridge_job_skill")
        result = {"taxonomy_count": len(taxonomy), "source_definition_count": len(definitions), "bridge_rows": len(rows), "jobs_with_skills": len({r[1] for r in rows}), "accepted_jobs": len(accepted), "unmatched": sum(r[4] is None for r in rows)}
        return result
    finally:
        con.close()


def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--archive", type=Path, default=Path("data/raw/archive (2).zip")); p.add_argument("--database", type=Path, default=Path("data/processed/talentgraph.duckdb")); args = p.parse_args()
    print(json.dumps(build_skill_models(args.archive, args.database), indent=2, sort_keys=True))

if __name__ == "__main__": main()
