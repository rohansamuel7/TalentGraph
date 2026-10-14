"""Load eligible technical job evidence for M7 matching."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ELIGIBLE_CATEGORIES = {"technical", "cloud", "data_engineering"}
REQUIRED_CLASSES = {"required"}
PREFERRED_CLASSES = {"preferred"}
EXPECTED_SCHEMA = "m7-evidence-v2"
EXPECTED_EXTRACTION = "qa-fix-04-v1"


def load_job_evidence(evidence_path: Path, skill_categories: dict[str, str]) -> dict[str, dict[str, Any]]:
    """Load canonical evidence, failing clearly on stale or malformed artifacts."""
    artifact = json.loads(evidence_path.read_text(encoding="utf-8"))
    if artifact.get("schema_version") != EXPECTED_SCHEMA:
        raise ValueError(f"Incompatible evidence schema: {artifact.get('schema_version')!r}; expected {EXPECTED_SCHEMA!r}")
    if artifact.get("extraction_version") != EXPECTED_EXTRACTION:
        raise ValueError(f"Stale evidence extraction: {artifact.get('extraction_version')!r}; expected {EXPECTED_EXTRACTION!r}")
    required_fields = {"job_key", "competency_id", "classification", "evidence_text", "source_description_sha256", "extraction_rule_id", "extraction_version"}
    if any(not required_fields <= set(row) for row in artifact.get("relationships", [])):
        raise ValueError("Evidence artifact is missing required provenance fields")
    evidence: dict[str, dict[str, Any]] = {}
    for row in artifact["relationships"]:
        skill_key = row["competency_id"]
        classification = row["classification"]
        if skill_categories.get(skill_key) not in ELIGIBLE_CATEGORIES:
            continue
        job = evidence.setdefault(row["job_key"], {"required": {}, "preferred": {}, "non_scoring": {}})
        # Preserve observed mentions for review, but only required/preferred
        # buckets can contribute to comparisons or current graph edges.
        if classification in REQUIRED_CLASSES:
            bucket = "required"
        elif classification in PREFERRED_CLASSES:
            bucket = "preferred"
        else:
            bucket = "non_scoring"
        job[bucket][skill_key] = {"classification": classification, "source": row["evidence_source"], "rule_id": row["extraction_rule_id"], "version": row["extraction_version"], "evidence_text": row["evidence_text"], "source_description_sha256": row["source_description_sha256"]}
    return evidence
