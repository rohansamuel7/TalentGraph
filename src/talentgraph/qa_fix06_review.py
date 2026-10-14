"""Build the QA-FIX-06 evidence review import."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

from .qa_fix06_support import evidence_excerpt, load_descriptions, source_hash, validate_labels
OUTPUT_FIELDS = [
    "job_key", "competency", "source_file", "source_row_number", "description_sha256",
    "full_description_original", "evidence_original", "evidence_cleaned_full", "evidence_preview",
    "extraction_method", "original_classification", "updated_classification", "ai_proposed_label",
    "human_label_raw", "human_rationale_raw", "ai_proposed_rationale", "ai_review_priority",
    "classification_disagreement", "unresolved_review_flag",
]
def _read_rows(path: Path) -> list[dict[str, str]]:
    """Read a UTF-8 CSV while retaining human fields as strings."""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))
def _build_row(model: dict[str, str], human: dict[str, str], description: str, row_number: int) -> dict[str, str]:
    competency_id = human.get("competency_id", "") or None
    original, cleaned, preview = evidence_excerpt(description, competency_id)
    label = human["confirmed_label"]
    disagreement = "yes" if label != model["updated_classification"] else "no"
    unresolved = "yes" if label == "required/preferred" or (not competency_id and label == "ambiguous") else "no"
    return {
        "job_key": human["job_key"], "competency": human["competency"], "source_file": "postings.csv",
        "source_row_number": str(row_number), "description_sha256": source_hash(description),
        "full_description_original": description, "evidence_original": original,
        "evidence_cleaned_full": cleaned, "evidence_preview": preview,
        "extraction_method": "qa-fix-04-rule-match" if competency_id else "no-dictionary-term-complete-description",
        "original_classification": model["original_classification"],
        "updated_classification": model["updated_classification"], "ai_proposed_label": human.get("ai_proposed_label", ""),
        "human_label_raw": label, "human_rationale_raw": human.get("reviewer_rationale", ""),
        "ai_proposed_rationale": human.get("ai_proposed_rationale", ""),
        "ai_review_priority": human.get("ai_review_priority", ""),
        "classification_disagreement": disagreement, "unresolved_review_flag": unresolved,
    }
def build_review(model_path: Path, labels_path: Path, worksheet_path: Path, archive: Path, output: Path) -> dict[str, int]:
    """Import labels and produce auditable full-description review rows."""
    model_rows = _read_rows(model_path)
    label_rows = _read_rows(labels_path)
    worksheet_rows = _read_rows(worksheet_path)
    competency_ids = {(row["job_key"], row["candidate_competency_name"] or "[none detected]"): row["candidate_competency_id"] for row in worksheet_rows}
    model_by_key = {(row["job_key"], row["competency"]): row for row in model_rows}
    label_keys = {(row["job_key"], row["competency"]): row for row in label_rows}
    validate_labels(label_rows, set(model_by_key))
    descriptions = load_descriptions(archive, {key[0] for key in model_by_key})
    if len(descriptions) != len({key[0] for key in model_by_key}):
        raise ValueError("Source archive is missing one or more reviewed job descriptions")
    rows = []
    for key in sorted(model_by_key):
        human = {**label_keys[key], "competency_id": competency_ids[key]}
        rows.append(_build_row(model_by_key[key], human, *descriptions[key[0]]))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_FIELDS)
        writer.writeheader(); writer.writerows(rows)
    return {"records": len(rows), "disagreements": sum(row["classification_disagreement"] == "yes" for row in rows), "unresolved": sum(row["unresolved_review_flag"] == "yes" for row in rows)}
def write_report(review_path: Path, report_path: Path) -> None:
    """Write public-safe QA-FIX-06 integrity and review metrics."""
    rows = _read_rows(review_path)
    labels = Counter(row["human_label_raw"] for row in rows)
    repaired = sum(row["evidence_original"] != row["evidence_cleaned_full"] for row in rows)
    report = [
        "# QA-FIX-06 Evidence Quality Report\n",
        f"- Records retained: {len(rows)}\n- Unique job/competency keys: {len({(r['job_key'], r['competency']) for r in rows})}\n- Source descriptions with deterministic SHA-256: {len({r['description_sha256'] for r in rows})} distinct hashes\n",
        "Human-label counts: " + ", ".join(f"{key}={labels[key]}" for key in sorted(labels)) + ".\n",
        f"Classification disagreements: {sum(r['classification_disagreement'] == 'yes' for r in rows)}.\n",
        f"Evidence snippets with display cleaning applied: {repaired}.\n",
        "## Evidence preservation\n\nEvery row contains the complete unmodified source description, its UTF-8 SHA-256, source file/row location, an original evidence excerpt, a cleaned display excerpt, and a bounded preview. Cleaning only normalizes layout whitespace and selected HTML separators; it does not replace missing words.\n",
        "## Missing dictionary-term cases\n\n" + "\n".join(f"- {r['job_key']}: complete description retained; human label `{r['human_label_raw']}`." for r in rows if r["extraction_method"].startswith("no-dictionary")) or "- None.",
        "## Unresolved review cases\n\n" + "\n".join(f"- {r['job_key']} — {r['competency']}: human label `{r['human_label_raw']}` requires review." for r in rows if r["unresolved_review_flag"] == "yes") or "- None.",
        "\nHuman labels are preserved review inputs, not validated ground truth. AI proposal fields remain separate and are not imported as confirmed labels.\n",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n\n".join(report), encoding="utf-8")


def main() -> None:
    """Parse QA-FIX-06 paths and write the review artifact."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, default=Path("data/processed/qa_fix05_reconciliation.csv"))
    parser.add_argument("--labels", type=Path, default=Path("data/processed/qa_fix06_human_labels.csv"))
    parser.add_argument("--worksheet", type=Path, default=Path("data/processed/qa_fix03_human_review.csv"))
    parser.add_argument("--archive", type=Path, default=Path("data/raw/archive (2).zip"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/qa_fix06_clean_evidence_review.csv"))
    parser.add_argument("--report", type=Path, default=Path("docs/QA_FIX06_EVIDENCE_QUALITY_REPORT.md"))
    args = parser.parse_args()
    print(build_review(args.model, args.labels, args.worksheet, args.archive, args.output))
    write_report(args.output, args.report)


if __name__ == "__main__":
    main()
