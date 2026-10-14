import csv
import tempfile
import unittest
from pathlib import Path

from talentgraph.qa_fix07_evaluation import write_outputs


ROOT = Path(__file__).parents[1]


class QAFix07EvaluationTests(unittest.TestCase):
    def test_java_resolution_and_comparable_count(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "final.csv"
            report = Path(temp_dir) / "report.md"
            result = write_outputs(ROOT / "data/processed/qa_fix06_clean_evidence_review.csv", output, report)
            self.assertEqual(result, {"records": 25, "comparable": 17, "unresolved": 5})
            with output.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))
            java = next(row for row in rows if row["competency"] == "Java")
            self.assertEqual(java["human_label_raw"], "required/preferred")
            self.assertEqual(java["finalized_label"], "preferred")
            self.assertEqual(java["resolution_status"], "resolved")

    def test_coverage_suggestions_are_not_label_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "final.csv"
            report = Path(temp_dir) / "report.md"
            write_outputs(ROOT / "data/processed/qa_fix06_clean_evidence_review.csv", output, report)
            with output.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))
            no_terms = [row for row in rows if row["competency"] == "[none detected]"]
            self.assertEqual(len(no_terms), 5)
            self.assertTrue(all(row["finalized_label"] == "ambiguous" for row in no_terms))
            self.assertTrue(all(row["suggestion_quote"] for row in no_terms))


if __name__ == "__main__":
    unittest.main()
