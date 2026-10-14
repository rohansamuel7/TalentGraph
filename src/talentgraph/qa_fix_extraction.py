"""Semantic taxonomy classification and conservative description evidence extraction."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any

import duckdb

EXTRACTION_VERSION = "qa-fix-04-v1"

# Classification is deliberately independent of M4's operational category field.
SEMANTIC_TYPES = {
    "skill:airflow": "technical_competency", "skill:apache_spark": "technical_competency", "skill:aws": "technical_competency", "skill:azure": "technical_competency", "skill:duckdb": "technical_competency", "skill:gcp": "technical_competency", "skill:java": "technical_competency", "skill:networkx": "technical_competency", "skill:pandas": "technical_competency", "skill:pyspark": "technical_competency", "skill:python": "technical_competency", "skill:scala": "technical_competency", "skill:spark_sql": "technical_competency", "skill:sql": "technical_competency", "skill:sql_server": "technical_competency",
    "skill:source:acct": "functional_skill", "skill:source:advr": "functional_skill", "skill:source:anls": "functional_skill", "skill:source:art": "functional_skill", "skill:source:bd": "functional_skill", "skill:source:cnsl": "functional_skill", "skill:source:cust": "functional_skill", "skill:source:dsgn": "functional_skill", "skill:source:edu": "functional_skill", "skill:source:fin": "functional_skill", "skill:source:hr": "functional_skill", "skill:source:lgl": "functional_skill", "skill:source:mgmt": "functional_skill", "skill:source:mrkt": "functional_skill", "skill:source:pr": "functional_skill", "skill:source:prch": "functional_skill", "skill:source:prdm": "functional_skill", "skill:source:prjm": "functional_skill", "skill:source:qa": "functional_skill", "skill:source:rsch": "functional_skill", "skill:source:sale": "functional_skill", "skill:source:stra": "functional_skill", "skill:source:supl": "functional_skill", "skill:source:trng": "functional_skill", "skill:source:wrt": "functional_skill",
    "skill:source:adm": "industry_or_occupational_category", "skill:source:dist": "industry_or_occupational_category", "skill:source:eng": "industry_or_occupational_category", "skill:source:genb": "industry_or_occupational_category", "skill:source:hcpr": "industry_or_occupational_category", "skill:source:it": "industry_or_occupational_category", "skill:source:mnfc": "industry_or_occupational_category", "skill:source:othr": "ambiguous_or_other", "skill:source:prod": "industry_or_occupational_category", "skill:source:sci": "industry_or_occupational_category", "skill:source:trng": "functional_skill",
}

RULES = {
    "comp:python": ("Python", (r"\bpython(?:\s*3(?:\.\d+)?)?\b",)),
    "comp:sql": ("SQL", (r"\bsql\b(?!\s+server)",)),
    "comp:sql_server": ("SQL Server", (r"\b(?:microsoft\s+)?sql\s+server\b",)),
    "comp:pyspark": ("PySpark", (r"\bpyspark\b", r"\bpython\s+spark\b")),
    "comp:apache_spark": ("Apache Spark", (r"\bapache\s+spark\b", r"\bspark\s+(?:sql|framework|cluster)\b")),
    "comp:java": ("Java", (r"\bjava\b",)),
    "comp:aws": ("Amazon Web Services", (r"\baws\b", r"\bamazon\s+web\s+services\b")),
    "comp:azure": ("Microsoft Azure", (r"\bazure\b",)),
    "comp:power_bi": ("Power BI", (r"\bpower\s*bi\b",)),
    "comp:tableau": ("Tableau", (r"\btableau\b",)),
    "comp:excel": ("Microsoft Excel", (r"\bexcel\b", r"\bmicrosoft\s+excel\b")),
    "comp:snowflake": ("Snowflake", (r"\bsnowflake\b",)),
    "comp:databricks": ("Databricks", (r"\bdatabricks\b",)),
    "comp:airflow": ("Apache Airflow", (r"\bapache\s+airflow\b", r"\bairflow\b")),
    "comp:docker": ("Docker", (r"\bdocker\b",)),
    "comp:kubernetes": ("Kubernetes", (r"\bkubernetes\b", r"\bk8s\b")),
    "comp:git": ("Git", (r"\bgit(?:hub|lab)?\b",)),
    "comp:machine_learning": ("Machine Learning", (r"\bmachine\s+learning\b", r"\bml\s+models?\b")),
    "comp:etl": ("ETL", (r"\betl\b", r"\bextract(?:ion)?[,\s]+transform(?:ation)?[,\s]+load\b")),
    "comp:r": ("R", (r"\br\s+(?:programming\s+)?language\b", r"\brstudio\b",)),
    "comp:go": ("Go", (r"\b(?:golang|go\s+programming(?:\s+language)?)\b",)),
}
REQUIRED_CONTEXT = re.compile(r"\b(?:required|requires|requirements?|must|proficien(?:t|cy)|experience\s+(?:with|in)|knowledge\s+of|skills?\s+(?:in|include)|working\s+skills?\s+of|computer\s+literate\s+in|using|develop(?:ed|ment)?\s+with)\b", re.I)
PREFERRED_CONTEXT = re.compile(r"\b(?:preferred|preferable|highly\s+desirable|desirable|experience\s+a\s+plus|a\s+plus|nice\s+to\s+have|would\s+be\s+an?\s+advantage)\b", re.I)
NEGATED_CONTEXT = re.compile(r"\b(?:not\s+required|no\s+experience|without\s+(?:experience|knowledge)|do\s+not\s+use|never\s+use|not\s+needed)\b", re.I)
AMBIGUOUS_CONTEXT = re.compile(r"\b(?:familiarity\s+with|exposure\s+to|as\s+needed|may\s+use)\b", re.I)
# Backward-compatible name for the QA-FIX-02 review generator.
REQUIREMENT_CONTEXT = REQUIRED_CONTEXT
ORDINARY_EXCEL = re.compile(r"\bexcel\s+in\s+(?:a|an|the)\s+(?:team|work|professional|role|environment)", re.I)


def classify_taxonomy(rows: list[tuple[str, str, str]]) -> list[dict[str, str]]:
    return [{"skill_key": key, "canonical_name": name, "source_category": category, "semantic_type": SEMANTIC_TYPES.get(key, "ambiguous_or_other"), "classification_version": EXTRACTION_VERSION} for key, name, category in rows]


def _classify_context(text: str, start: int, end: int) -> str:
    # Keep negation and uncertainty ahead of positive requirement language:
    # a phrase can contain both, but should not become a scored requirement.
    left_boundary = max([text.rfind(mark, 0, start) for mark in ".;!?\n"])
    right_candidates = [text.find(mark, end) for mark in ".;!?\n" if text.find(mark, end) >= 0]
    right_boundary = min(right_candidates) if right_candidates else len(text)
    context = text[left_boundary + 1:right_boundary]
    if NEGATED_CONTEXT.search(context):
        return "negated"
    if AMBIGUOUS_CONTEXT.search(context):
        return "ambiguous"
    if PREFERRED_CONTEXT.search(context):
        return "preferred"
    return "required" if REQUIRED_CONTEXT.search(context) else "mentioned"


def _extract_from_text(job_key: str, text: str, source_file: str, source_row_number: int) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    lower = text.lower()
    for competency_id, (name, patterns) in RULES.items():
        for rule_id, pattern in enumerate(patterns, 1):
            for match in re.finditer(pattern, lower, re.I):
                start, end = match.span()
                context = lower[max(0, start - 100):min(len(lower), end + 100)]
                if competency_id == "comp:excel" and ORDINARY_EXCEL.search(context):
                    continue
                classification = _classify_context(lower, start, end)
                found.append({"job_key": job_key, "competency_id": competency_id, "competency_name": name, "evidence_source": "postings.csv.description", "extraction_rule_id": f"{competency_id}:rule:{rule_id}", "evidence_classification": classification, "source_file": source_file, "source_row_number": source_row_number, "extraction_version": EXTRACTION_VERSION})
    unique = {(x["job_key"], x["competency_id"]): x for x in found}
    return [unique[k] for k in sorted(unique)]


def extract_evidence(archive: Path, accepted_ids: set[str], output: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    with zipfile.ZipFile(archive) as z, z.open("postings.csv") as stream:
        reader = csv.DictReader(__import__("io").TextIOWrapper(stream, encoding="utf-8-sig", newline=""))
        for source_row_number, record in enumerate(reader, 2):
            if record["job_id"] in accepted_ids:
                rows.extend(_extract_from_text("linkedin:" + record["job_id"], record.get("description") or "", "postings.csv", source_row_number))
    rows = sorted(rows, key=lambda r: (r["job_key"], r["competency_id"]))
    artifact = {"schema_version": EXTRACTION_VERSION, "source_dataset": "local user-provided archive", "relationship_count": len(rows), "relationships": rows}
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"relationship_count": len(rows), "jobs_with_evidence": len({r["job_key"] for r in rows}), "distinct_competencies": len({r["competency_id"] for r in rows}), "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}


def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--database", type=Path, default=Path("/home/developer/talentgraph_data/talentgraph.duckdb")); p.add_argument("--archive", type=Path, default=Path("data/raw/archive (2).zip")); p.add_argument("--accepted", type=Path, default=Path("data/processed/job_postings_sample.csv")); p.add_argument("--output", type=Path, default=Path("data/processed/job_competency_evidence.json")); args = p.parse_args()
    con = duckdb.connect(str(args.database), read_only=True)
    try: taxonomy = classify_taxonomy(con.execute("select skill_key,canonical_name,category from dim_skill order by skill_key").fetchall())
    finally: con.close()
    accepted = {r["job_id"] for r in csv.DictReader(args.accepted.open(encoding="utf-8", newline=""))}
    result = extract_evidence(args.archive, accepted, args.output); result["taxonomy_counts"] = {t: sum(x["semantic_type"] == t for x in taxonomy) for t in sorted({x["semantic_type"] for x in taxonomy})}; print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__": main()
