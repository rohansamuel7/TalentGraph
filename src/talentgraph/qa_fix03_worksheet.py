"""Create a compact deterministic human-review worksheet from QA-FIX-02."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

OUTPUT_FIELDS = [
    "job_key", "source_row_number", "candidate_competency_id", "candidate_competency_name",
    "snippet", "extraction_decision", "extraction_rule_id", "evidence_classification",
    "confirmed_label", "reviewer_rationale",
]
ALLOWED_LABELS = ("required", "preferred", "incidental", "negated", "ambiguous")


def build_worksheet(source: Path, output: Path, limit: int = 25) -> dict[str, int]:
    records = json.loads(source.read_text(encoding="utf-8"))["records"]
    # Priority ensures required coverage, then fills deterministically by stable IDs.
    selected: list[dict[str, object]] = []
    used: set[tuple[str, object]] = set()

    def add_first(predicate, count: int) -> None:
        for row in sorted(records, key=lambda x: (x["job_key"], str(x["candidate_competency_id"]), x["snippet"])):
            key = (row["job_key"], row["candidate_competency_id"])
            if key not in used and predicate(row):
                selected.append(row); used.add(key)
                if sum(1 for item in selected if predicate(item)) >= count:
                    return

    # Include extracted positives and the three high-frequency review targets.
    add_first(lambda r: r["extraction_decision"] == "extracted", 10)
    for competency in ("comp:excel", "comp:sql", "comp:python"):
        add_first(lambda r, c=competency: r["candidate_competency_id"] == c, 3)
    add_first(lambda r: r["extraction_decision"] == "not_extracted" and r["evidence_classification"] == "explicit_incidental_mention", 4)
    add_first(lambda r: r["extraction_decision"] == "not_extracted" and r["evidence_classification"] == "requirement_context", 4)
    add_first(lambda r: r["extraction_decision"] == "not_extracted", limit)
    selected = sorted(selected[:limit], key=lambda x: (x["job_key"], str(x["candidate_competency_id"])))

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for row in selected:
            writer.writerow({field: row.get(field, "") if field not in ("confirmed_label", "reviewer_rationale") else "" for field in OUTPUT_FIELDS})
    return {"records": len(selected), "unique_jobs": len({row["job_key"] for row in selected})}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("data/processed/qa_fix02_review_sample.json"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/qa_fix03_human_review.csv"))
    args = parser.parse_args()
    print(json.dumps(build_worksheet(args.source, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
