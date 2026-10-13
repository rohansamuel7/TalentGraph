"""Focused standard-library tests for the M1 sampler."""

import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from talentgraph.m1_sampling import EXPECTED_POSTING_COLUMNS, inspect_archive, sample_postings


class M1SamplingTests(unittest.TestCase):
    def test_sampling_is_deterministic_and_records_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "source.zip"
            header = list(EXPECTED_POSTING_COLUMNS)
            header.sort()
            rows = []
            for i in range(10):
                row = [""] * len(header)
                row[header.index("job_id")] = str(i)
                row[header.index("listed_time")] = str(1700000000000 + i)
                row[header.index("title")] = f"Role {i}"
                rows.append(row)
            with ZipFile(archive, "w", ZIP_DEFLATED) as zipped:
                content = [header, *rows]
                zipped.writestr("postings.csv", "\n".join(",".join(r) for r in content) + "\n")
            first = root / "first.csv"
            second = root / "second.csv"
            first_meta = root / "first.json"
            second_meta = root / "second.json"
            first_rejects = root / "first_rejects.csv"
            second_rejects = root / "second_rejects.csv"
            sample_postings(archive, first, first_meta, first_rejects, sample_size=3)
            sample_postings(archive, second, second_meta, second_rejects, sample_size=3)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first_meta.read_text().split('"retrieved_at_utc"')[0], second_meta.read_text().split('"retrieved_at_utc"')[0])
            self.assertEqual(len(first.read_text().splitlines()), 4)
            self.assertEqual(first_rejects.read_text().splitlines(), ["source_row_number,reason"])

    def test_malformed_row_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "malformed.zip"
            header = sorted(EXPECTED_POSTING_COLUMNS)
            valid = [""] * len(header)
            valid[header.index("job_id")] = "1"
            valid[header.index("listed_time")] = "1700000000000"
            with ZipFile(archive, "w", ZIP_DEFLATED) as zipped:
                zipped.writestr("postings.csv", ",".join(header) + "\n" + ",".join(valid) + "\n1,too,short\n")
            output = root / "sample.csv"
            rejects = root / "rejects.csv"
            metadata = root / "metadata.json"
            result = sample_postings(archive, output, metadata, rejects, sample_size=1)
            self.assertEqual(result["sample_size_selected"], 1)
            self.assertEqual(result["reject_rows"], 1)
            self.assertIn("column_count_mismatch", rejects.read_text())

    def test_unsafe_archive_path_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "unsafe.zip"
            with ZipFile(archive, "w") as zipped:
                zipped.writestr("../postings.csv", "job_id\n1\n")
            with self.assertRaises(ValueError):
                inspect_archive(archive)


if __name__ == "__main__":
    unittest.main()
