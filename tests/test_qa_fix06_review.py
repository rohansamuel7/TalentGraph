import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from talentgraph.qa_fix06_review import build_review


ROOT = Path(__file__).parents[1]


class QAFix06ReviewTests(unittest.TestCase):
    def test_review_preserves_labels_hashes_and_no_term_descriptions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "review.csv"
            result = build_review(
                ROOT / "data/processed/qa_fix05_reconciliation.csv",
                ROOT / "data/processed/qa_fix06_human_labels.csv",
                ROOT / "data/processed/qa_fix03_human_review.csv",
                ROOT / "data/raw/archive (2).zip",
                output,
            )
            self.assertEqual(result, {"records": 25, "disagreements": 13, "unresolved": 6})
            with output.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 25)
            self.assertTrue(all(len(row["description_sha256"]) == 64 for row in rows))
            self.assertTrue(all(row["human_label_raw"] for row in rows))
            no_terms = [row for row in rows if row["extraction_method"].startswith("no-dictionary")]
            self.assertEqual(len(no_terms), 5)
            self.assertTrue(all(row["human_label_raw"] == "ambiguous" for row in no_terms))
            self.assertTrue(all(len(row["full_description_original"]) >= len(row["evidence_cleaned_full"]) for row in no_terms))

    def test_hash_is_exact_utf8_source_hash(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "review.csv"
            build_review(
                ROOT / "data/processed/qa_fix05_reconciliation.csv",
                ROOT / "data/processed/qa_fix06_human_labels.csv",
                ROOT / "data/processed/qa_fix03_human_review.csv",
                ROOT / "data/raw/archive (2).zip",
                output,
            )
            with output.open(encoding="utf-8", newline="") as stream:
                row = next(csv.DictReader(stream))
            expected = hashlib.sha256(row["full_description_original"].encode("utf-8")).hexdigest()
            self.assertEqual(row["description_sha256"], expected)


if __name__ == "__main__":
    unittest.main()
