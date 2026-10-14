"""Reconcile the QA-FIX-03 worksheet against the QA-FIX-04 extractor."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any

from .qa_fix05_support import evidence_snippet, load_descriptions
from .qa_fix_extraction import _extract_from_text
OUTPUT_FIELDS = [
    "job_key", "competency", "original_extraction_decision", "original_classification",
    "updated_extraction_decision", "updated_classification", "confirmed_label",
    "reviewer_rationale", "classifier_changed", "evidence_snippet", "review_needed",
]
REVIEW_CLASSES = {"mentioned", "negated", "ambiguous", "no_candidate_term"}
def reconcile_rows(worksheet: Path, archive: Path) -> list[dict[str, str]]:
    """Re-evaluate rows while preserving original human-review fields."""
    descriptions = load_descriptions(archive)
    reconciled: list[dict[str, str]] = []
    with worksheet.open(encoding="utf-8", newline="") as stream:
        for original in csv.DictReader(stream):
            job_key = original["job_key"]
            competency_id = original["candidate_competency_id"] or None
            text, row_number = descriptions[job_key]
            matches = _extract_from_text(job_key, text, "postings.csv", row_number)
            match = next((item for item in matches if item["competency_id"] == competency_id), None)
            updated_class = match["evidence_classification"] if match else "no_candidate_term"
            changed = original["evidence_classification"] != updated_class
            reconciled.append({
                "job_key": job_key,
                "competency": original["candidate_competency_name"] or "[none detected]",
                "original_extraction_decision": original["extraction_decision"],
                "original_classification": original["evidence_classification"],
                "updated_extraction_decision": "extracted" if match else "not_extracted",
                "updated_classification": updated_class,
                "confirmed_label": original["confirmed_label"],
                "reviewer_rationale": original["reviewer_rationale"],
                "classifier_changed": "yes" if changed else "no",
                "evidence_snippet": evidence_snippet(text, competency_id),
                "review_needed": "yes" if not original["confirmed_label"] or changed or updated_class in REVIEW_CLASSES else "no",
            })
    return reconciled
def write_reconciliation(rows: list[dict[str, str]], output: Path) -> None:
    """Write the reconciled worksheet as a deterministic CSV."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
def write_summary(rows: list[dict[str, str]], output: Path) -> None:
    """Write the human-review summary without asserting ground truth."""
    changed = [row for row in rows if row["classifier_changed"] == "yes"]
    review = [row for row in rows if row["review_needed"] == "yes"]
    counts = Counter(row["updated_classification"] for row in rows)
    unique_keys = len({(row["job_key"], row["competency"]) for row in rows})

    def bullets(items: list[dict[str, str]], text: Any) -> str:
        return "\n".join(f"- {text(row)}" for row in items) or "- None."

    missed = [row for row in changed if row["original_extraction_decision"] == "not_extracted" and row["updated_classification"] == "required"]
    corrections = [row for row in changed if row["updated_classification"] in {"required", "preferred"}]
    edge = [row for row in rows if row["updated_classification"] in REVIEW_CLASSES]
    sections = [
        "# QA-FIX-05 Reconciliation Summary\n",
        f"- Records reconciled: {len(rows)}\n- Unique job/competency keys: {unique_keys}\n- Classifier changes: {len(changed)}\n- Records requiring review: {len(review)}\n",
        "Updated classification counts: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)) + ".\n",
        "## Previously missed explicit requirements now detected\n" + bullets(missed, lambda r: f"{r['job_key']} — {r['competency']}: {r['evidence_snippet']}"),
        "## Required versus preferred corrections\n" + bullets(corrections, lambda r: f"{r['job_key']} — {r['competency']}: {r['original_classification']} → {r['updated_classification']}"),
        "## Incidental and ambiguous cases\n" + bullets(edge, lambda r: f"{r['job_key']} — {r['competency']}: {r['updated_classification']}"),
        "## Remaining disagreements requiring human review\n" + bullets(review, lambda r: f"{r['job_key']} — {r['competency']}: original={r['original_classification']}; updated={r['updated_classification']}"),
        "AI-generated classifications remain proposals; blank human fields were preserved and are not ground truth.\n",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n\n".join(sections), encoding="utf-8")
def reconcile(worksheet: Path, archive: Path, output: Path, summary: Path) -> dict[str, Any]:
    """Run reconciliation and write its CSV and review summary."""
    rows = reconcile_rows(worksheet, archive)
    write_reconciliation(rows, output)
    write_summary(rows, summary)
    return {"records": len(rows), "unique_keys": len({(r["job_key"], r["competency"]) for r in rows}), "classifier_changes": sum(r["classifier_changed"] == "yes" for r in rows), "review_needed": sum(r["review_needed"] == "yes" for r in rows)}
def main() -> None:
    """Parse CLI paths and run QA-FIX-05."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--worksheet", type=Path, default=Path("data/processed/qa_fix03_human_review.csv"))
    parser.add_argument("--archive", type=Path, default=Path("data/raw/archive (2).zip"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/qa_fix05_reconciliation.csv"))
    parser.add_argument("--summary", type=Path, default=Path("docs/QA_FIX05_RECONCILIATION_SUMMARY.md"))
    args = parser.parse_args()
    print(reconcile(args.worksheet, args.archive, args.output, args.summary))


if __name__ == "__main__":
    main()
