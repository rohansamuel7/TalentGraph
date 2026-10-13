import tempfile
import unittest
from pathlib import Path

import duckdb

from talentgraph.m3_modeling import build_models


class M3ModelingTests(unittest.TestCase):
    def test_build_counts_constraints_and_repeatability(self):
        source = Path("data/processed/m2_ingestion/job_postings")
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.duckdb"
            second = Path(directory) / "second.duckdb"
            result1 = build_models(source, first)
            result2 = build_models(source, second)
            self.assertEqual(result1["tables"]["fact_job_posting"], 1500)
            self.assertEqual(result1["tables"], result2["tables"])
            self.assertTrue(all(row["status"] == "PASS" for row in result1["validation"]))
            with duckdb.connect(str(first)) as con:
                self.assertEqual(con.execute("select count(*) from fact_job_posting where job_key is null").fetchone()[0], 0)
                self.assertEqual(con.execute("select count(*) from fact_job_posting f left join dim_company c using(company_key) where c.company_key is null").fetchone()[0], 0)
                self.assertEqual(con.execute("select count(*) from vw_salary_analysis where representative_salary < 0").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
