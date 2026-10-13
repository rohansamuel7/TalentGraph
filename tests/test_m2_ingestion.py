import unittest
import csv
import tempfile
from pathlib import Path

from talentgraph.m2_ingestion import (OUTPUT_COLUMNS, RAW_SCHEMA, SOURCE_COLUMNS,
                                       _read_csv_records, create_spark, _timestamp)


class M2ContractTests(unittest.TestCase):
    def test_explicit_source_schema_matches_observed_header(self):
        self.assertEqual(tuple(field.name for field in RAW_SCHEMA.fields[:-1]), SOURCE_COLUMNS)
        self.assertTrue(all(field.dataType.simpleString() == "string" for field in RAW_SCHEMA.fields))
        self.assertIn("raw_record_hash", OUTPUT_COLUMNS)
        self.assertNotIn("description", OUTPUT_COLUMNS)
        self.assertNotIn("application_url", OUTPUT_COLUMNS)

    def test_timestamp_expression_is_defined(self):
        self.assertTrue(callable(_timestamp))

    def test_python_framing_preserves_multiline_commas_and_quotes(self):
        spark = create_spark("M2-test-framing")
        try:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "fixture.csv"
                row = [""] * len(SOURCE_COLUMNS)
                row[0], row[2], row[3], row[22] = "1", "Role", 'line 1, "quoted"\nline 2', "1710000000000"
                with path.open("w", newline="", encoding="utf-8") as stream:
                    writer = csv.writer(stream)
                    writer.writerow(SOURCE_COLUMNS)
                    writer.writerow(row)
                    stream.write("2,too,short\n")
                parsed = _read_csv_records(spark, path)
                self.assertEqual(parsed.count(), 2)
                self.assertEqual(parsed.where("_corrupt_record is null").count(), 1)
                self.assertEqual(parsed.where("_corrupt_record is not null").count(), 1)
        finally:
            spark.stop()


if __name__ == "__main__":
    unittest.main()
