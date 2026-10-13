"""Create a deterministic, sanitized review sample for competency extraction."""

from __future__ import annotations

import argparse
import csv
import io
import json
import random
import re
import zipfile
from pathlib import Path
from typing import Any

from talentgraph.qa_fix_extraction import NEGATED_CONTEXT, REQUIREMENT_CONTEXT, RULES, _extract_from_text

SEED = 20261012
SAMPLE_SIZE_BY_STRATUM = 20
MAX_SNIPPET = 280


def _redact(text: str) -> str:
    text = re.sub(r"https?://\S+|www\.\S+", "[URL]", text, flags=re.I)
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[EMAIL]", text)
    text = re.sub(r"\b(?:\+?\d[\d(). -]{7,}\d)\b", "[PHONE]", text)
    return re.sub(r"\s+", " ", text).strip()


def _snippet(text: str, start: int, end: int) -> str:
    left = max(0, start - 100)
    right = min(len(text), end + 160)
    value = _redact(text[left:right])
    return value[:MAX_SNIPPET]


def _term_hits(text: str) -> list[dict[str, Any]]:
    hits = []
    for competency_id, (name, patterns) in RULES.items():
        for rule_number, pattern in enumerate(patterns, 1):
            match = re.search(pattern, text, re.I)
            if match:
                context = text[max(0, match.start() - 100):min(len(text), match.end() + 100)]
                hits.append({
                    "competency_id": competency_id,
                    "competency_name": name,
                    "rule_id": f"{competency_id}:rule:{rule_number}",
                    "snippet": _snippet(text, match.start(), match.end()),
                    "proposed_context": "negated_or_not_required" if NEGATED_CONTEXT.search(context) else ("requirement_context" if REQUIREMENT_CONTEXT.search(context) else "explicit_incidental_mention"),
                })
                break
    return sorted(hits, key=lambda x: x["competency_id"])


def build_review_sample(archive: Path, accepted_csv: Path, output: Path) -> dict[str, Any]:
    accepted = {row["job_id"] for row in csv.DictReader(accepted_csv.open(encoding="utf-8", newline=""))}
    extracted_ids: set[str] = set()
    records: dict[str, dict[str, Any]] = {}
    with zipfile.ZipFile(archive) as z, z.open("postings.csv") as stream:
        reader = csv.DictReader(io.TextIOWrapper(stream, encoding="utf-8-sig", newline=""))
        for row_number, row in enumerate(reader, 2):
            if row["job_id"] not in accepted:
                continue
            job_key = "linkedin:" + row["job_id"]
            hits = _term_hits(row.get("description") or "")
            extracted = _extract_from_text(job_key, row.get("description") or "", "postings.csv", row_number)
            extracted_ids.add(job_key) if extracted else None
            records[job_key] = {"job_key": job_key, "source_row_number": row_number, "hits": hits, "extracted": {x["competency_id"]: x for x in extracted}}

    strata = {"with_extracted_evidence": [], "terms_without_extracted_evidence": [], "without_dictionary_terms": []}
    for job_key, record in records.items():
        if record["extracted"]:
            strata["with_extracted_evidence"].append(job_key)
        elif record["hits"]:
            strata["terms_without_extracted_evidence"].append(job_key)
        else:
            strata["without_dictionary_terms"].append(job_key)

    rng = random.Random(SEED)
    selected = {}
    for name, values in strata.items():
        values = sorted(values)
        rng.shuffle(values)
        selected[name] = values[:SAMPLE_SIZE_BY_STRATUM]

    review_records = []
    for stratum in sorted(selected):
        for job_key in sorted(selected[stratum]):
            record = records[job_key]
            candidates = record["hits"] or [{"competency_id": None, "competency_name": None, "rule_id": None, "snippet": "[No dictionary term detected in sampled description]", "proposed_context": "no_candidate_term"}]
            for candidate in candidates:
                extracted = record["extracted"].get(candidate["competency_id"] or "")
                review_records.append({
                    "job_key": job_key,
                    "source_row_number": record["source_row_number"],
                    "stratum": stratum,
                    "snippet": candidate["snippet"],
                    "candidate_competency_id": candidate["competency_id"],
                    "candidate_competency_name": candidate["competency_name"],
                    "extraction_decision": "extracted" if extracted else "not_extracted",
                    "extraction_rule_id": extracted["extraction_rule_id"] if extracted else candidate["rule_id"],
                    "evidence_classification": extracted["evidence_classification"] if extracted else candidate["proposed_context"],
                    "proposed_review_label": None,
                    "confirmed_ground_truth": None,
                    "reviewer_rationale": None,
                })
    artifact = {"schema_version": "qa-fix-02-review-v1", "sampling_seed": SEED, "sample_size_by_stratum": SAMPLE_SIZE_BY_STRATUM, "ground_truth_status": "not_reviewed", "records": review_records}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"strata": {key: len(value) for key, value in selected.items()}, "review_records": len(review_records), "output": str(output)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=Path("data/raw/archive (2).zip"))
    parser.add_argument("--accepted", type=Path, default=Path("data/processed/job_postings_sample.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/qa_fix02_review_sample.json"))
    args = parser.parse_args()
    print(json.dumps(build_review_sample(args.archive, args.accepted, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
