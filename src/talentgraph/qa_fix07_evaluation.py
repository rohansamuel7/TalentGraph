"""Finalize QA-FIX-06 labels and evaluate comparable extractor predictions."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
LABELS = ("required", "preferred", "incidental", "negated", "ambiguous")
SUGGESTIONS = {
    "linkedin:3884806695": ("basic math; problem-solving", "You will need to possess basic math and solid problem-solving skills"),
    "linkedin:3884856205": ("SaaS; sales-funnel optimization; go-to-market strategy", "Your mission: to optimize our sales funnel, create powerful go-to-market strategies"),
    "linkedin:3884875543": ("SaaS platform", "What We Do: J. Galt Finance Suite offers a SaaS platform and consultative services"),
    "linkedin:3887480827": ("Foundation software", "Foundation software experience preferred, but not required."),
    "linkedin:3887575585": ("SharePoint; Work Management Information System; data entry; report generation", "The Administrative Assistant - Maintenance role provides administrative support and clerical assistance, timekeeping, data entry, report generation services, and SharePoint site overview"),
}
OUTPUT_FIELDS = [
    "job_key", "competency", "human_label_raw", "finalized_label", "resolution_status",
    "resolution_reason", "updated_classification", "prediction_comparable", "suggested_coverage_gap",
    "suggestion_quote", "classification_disagreement", "unresolved_review_flag",
]
def read_rows(path: Path) -> list[dict[str, str]]:
    """Read a UTF-8 review artifact."""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))
def finalize_row(row: dict[str, str]) -> dict[str, str]:
    """Resolve only the explicitly authorized Java judgment."""
    raw = row["human_label_raw"]
    is_java = row["competency"] == "Java"
    if is_java and raw == "required/preferred":
        label = "preferred"
        status = "resolved"
        reason = "Full description presents Java as an alternative: two or more development languages such as Java or Python."
        unresolved = "no"
    else:
        label = raw
        status = "unchanged"
        reason = "Preserved user-entered label without coercion."
        unresolved = row["unresolved_review_flag"]
    gap, quote = SUGGESTIONS.get(row["job_key"], ("", ""))
    comparable = "yes" if row["updated_classification"] in LABELS and not (is_java and raw == "required/preferred") else "no"
    if is_java and raw == "required/preferred":
        comparable = "yes"
    return {"job_key": row["job_key"], "competency": row["competency"], "human_label_raw": raw,
            "finalized_label": label, "resolution_status": status, "resolution_reason": reason,
            "updated_classification": row["updated_classification"], "prediction_comparable": comparable,
            "suggested_coverage_gap": gap, "suggestion_quote": quote,
            "classification_disagreement": "yes" if label != row["updated_classification"] else "no",
            "unresolved_review_flag": unresolved}
def evaluate(rows: list[dict[str, str]]) -> tuple[Counter, dict[str, dict[str, float | int]]]:
    """Return the comparable confusion matrix and supported per-class metrics."""
    comparable = [row for row in rows if row["prediction_comparable"] == "yes"]
    matrix = Counter((row["finalized_label"], row["updated_classification"]) for row in comparable)
    metrics: dict[str, dict[str, float | int]] = {}
    for label in LABELS:
        tp = matrix[label, label]
        predicted = sum(matrix[actual, label] for actual in LABELS)
        actual = sum(matrix[label, predicted_label] for predicted_label in LABELS)
        if not actual and not predicted:
            continue
        precision = tp / predicted if predicted else 0.0
        recall = tp / actual if actual else 0.0
        metrics[label] = {"support": actual, "precision": precision, "recall": recall, "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0}
    return matrix, metrics
def write_outputs(source: Path, output: Path, report: Path) -> dict[str, int]:
    """Create final labels and a documented evaluation report."""
    rows = [finalize_row(row) for row in read_rows(source)]
    matrix, metrics = evaluate(rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_FIELDS)
        writer.writeheader(); writer.writerows(rows)
    write_report(rows, matrix, metrics, report)
    return {"records": len(rows), "comparable": sum(r["prediction_comparable"] == "yes" for r in rows), "unresolved": sum(r["unresolved_review_flag"] == "yes" for r in rows)}
def write_report(rows: list[dict[str, str]], matrix: Counter, metrics: dict[str, dict[str, float | int]], path: Path) -> None:
    """Write public-safe label, coverage, and metric findings."""
    counts = Counter(row["finalized_label"] for row in rows)
    lines = ["# QA-FIX-07 Extraction Quality Evaluation\n", f"- Records: {len(rows)}\n- Comparable prediction records: {sum(r['prediction_comparable'] == 'yes' for r in rows)}\n- Unresolved records: {sum(r['unresolved_review_flag'] == 'yes' for r in rows)}\n", "Final label counts: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)) + ".\n", "## Java resolution\n\nThe raw human label `required/preferred` is preserved. It is resolved to `preferred` because the full description says: `two or more development languages such as Java or Python`; Java is an example/alternative, not individually mandatory.\n", "## Confusion matrix\n\nRows are finalized human labels; columns are QA-FIX-04 predictions.\n\n| Actual \\ Predicted | required | preferred | incidental | negated | ambiguous |\n|---|---:|---:|---:|---:|---:|\n"]
    for actual in LABELS:
        lines.append("| " + actual + " | " + " | ".join(str(matrix[actual, predicted]) for predicted in LABELS) + " |")
    lines += ["\n## Supported metrics\n", "Metrics use only the 17 records with a five-class prediction. Five no-dictionary-term cases have `no_candidate_term`, and three explicit mentions have `mentioned`; both are outside the five-class comparison and are reported as detection/classification gaps.\n", "| Class | Support | Precision | Recall | F1 |\n|---|---:|---:|---:|---:|"]
    for label, values in metrics.items():
        lines.append(f"| {label} | {values['support']} | {values['precision']:.3f} | {values['recall']:.3f} | {values['f1']:.3f} |")
    lines += ["\n## No-dictionary-term review\n", "The five descriptions do not establish absence of skills. Coverage suggestions are evidence-backed prompts only:\n"]
    for row in rows:
        if row["suggested_coverage_gap"]:
            lines.append(f"- **{row['job_key']}** — possible coverage: {row['suggested_coverage_gap']}. Exact source quotation: `{row['suggestion_quote']}`")
    lines += ["\n## Interpretation\n", "The set is selected and only 25 records; these metrics do not establish production-wide accuracy. Disagreements involving explicit dictionary terms are extractor classification/detection issues. The five no-term records are taxonomy coverage gaps or non-technical competency cases, not confirmed extractor false negatives. Human labels remain reviewed judgments, not general ground truth.\n"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
def main() -> None:
    """Run QA-FIX-07 from the QA-FIX-06 review artifact."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("data/processed/qa_fix06_clean_evidence_review.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/qa_fix07_final_review.csv"))
    parser.add_argument("--report", type=Path, default=Path("docs/QA_FIX07_EVALUATION.md"))
    args = parser.parse_args()
    print(write_outputs(args.source, args.output, args.report))
if __name__ == "__main__":
    main()
