"""Build the versioned canonical QA-FIX-04 evidence artifact for M7."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from typing import Any

from .qa_fix_extraction import EXTRACTION_VERSION, RULES, _extract_from_text

SCHEMA_VERSION = "m7-evidence-v2"
CLASSIFICATIONS = {"required", "preferred", "mentioned", "negated", "ambiguous"}


def _excerpt(text: str, competency_id: str, rule_id: str) -> str:
    """Extract a bounded auditable sentence/list item without changing source text."""
    rule_number = int(rule_id.rsplit(":", 1)[-1]) - 1
    pattern = RULES[competency_id][1][rule_number]
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return ""
    left = max(text.rfind(mark, 0, match.start()) for mark in ".!?\n") + 1
    right_candidates = [text.find(mark, match.end()) for mark in ".!?\n" if text.find(mark, match.end()) >= 0]
    right = min(right_candidates) + 1 if right_candidates else len(text)
    return text[left:right].strip()


def _source_hash(text: str) -> str:
    """Hash the exact source description bytes represented as UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sample_ids(path: Path) -> set[str]:
    """Load accepted sample job IDs as extractor keys."""
    with path.open(encoding="utf-8", newline="") as stream:
        return {"linkedin:" + row["job_id"] for row in csv.DictReader(stream)}


def build_artifact(archive: Path, accepted: Path, output: Path) -> dict[str, Any]:
    """Re-run QA-FIX-04 over all accepted descriptions and write canonical evidence."""
    accepted_ids = _sample_ids(accepted)
    relationships: list[dict[str, Any]] = []
    seen_jobs: set[str] = set()
    with zipfile.ZipFile(archive) as source:
        with source.open("postings.csv") as stream:
            reader = csv.DictReader(io.TextIOWrapper(stream, encoding="utf-8-sig", newline=""))
            # This counts logical archive CSV records. M2's Spark processing
            # index is different and must not be treated as the same row ID.
            for row_number, record in enumerate(reader, 2):
                job_key = "linkedin:" + record["job_id"]
                if job_key not in accepted_ids:
                    continue
                seen_jobs.add(job_key)
                description = record.get("description") or ""
                digest = _source_hash(description)
                extracted = _extract_from_text(job_key, description, "postings.csv", row_number)
                for item in extracted:
                    classification = item["evidence_classification"]
                    if classification not in CLASSIFICATIONS:
                        raise ValueError(f"Unsupported extractor classification: {classification}")
                    relationships.append({"job_key": job_key, "competency_id": item["competency_id"].replace("comp:", "skill:", 1), "source_competency_id": item["competency_id"], "competency_name": item["competency_name"], "classification": classification, "evidence_text": _excerpt(description, item["competency_id"], item["extraction_rule_id"]), "evidence_source": item["evidence_source"], "source_file": item["source_file"], "source_row_number": row_number, "source_description_sha256": digest, "extraction_rule_id": item["extraction_rule_id"], "extraction_version": item["extraction_version"]})
    relationships.sort(key=lambda row: (row["job_key"], row["competency_id"], row["classification"], row["extraction_rule_id"]))
    artifact = {"schema_version": SCHEMA_VERSION, "extraction_version": EXTRACTION_VERSION, "source_dataset": "local user-provided archive", "sample_job_count": len(accepted_ids), "jobs_seen": len(seen_jobs), "relationship_count": len(relationships), "relationships": relationships}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"sample_job_count": len(accepted_ids), "jobs_seen": len(seen_jobs), "relationship_count": len(relationships), "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}


def main() -> None:
    """Parse paths and build the canonical evidence artifact."""
    parser = argparse.ArgumentParser(); parser.add_argument("--archive", type=Path, default=Path("data/raw/archive (2).zip")); parser.add_argument("--accepted", type=Path, default=Path("data/processed/job_postings_sample.csv")); parser.add_argument("--output", type=Path, default=Path("data/processed/job_competency_evidence_qa_fix04.json")); args = parser.parse_args()
    print(json.dumps(build_artifact(args.archive, args.accepted, args.output), indent=2, sort_keys=True))


if __name__ == "__main__": main()
