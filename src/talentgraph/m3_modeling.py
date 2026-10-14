"""DuckDB analytical models for the validated M2 job-posting Parquet output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import duckdb


def build_models(input_parquet: Path, database: Path, sql_dir: Path | None = None) -> dict[str, Any]:
    """Rebuild the local analytical database deterministically and validate it."""
    sql_dir = sql_dir or Path("sql")
    database.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(database))
    try:
        con.execute("SET memory_limit='1GB'")
        con.execute("SET threads=2")
        parquet_glob = str(input_parquet / "*.parquet").replace("'", "''")
        models = (sql_dir / "m3_models.sql").read_text(encoding="utf-8").replace("{{INPUT_PARQUET}}", parquet_glob)
        con.execute(models)
        # Compare modeled fact grain with the actual curated input, not a fixed
        # count that could hide an upstream sample change.
        expected = con.execute("SELECT count(*) FROM read_parquet(?)", [parquet_glob]).fetchone()[0]
        validation_sql = (sql_dir / "m3_validation.sql").read_text(encoding="utf-8").replace("{{EXPECTED_ROWS}}", str(expected))
        validation = [dict(zip(("check_name", "check_value", "status"), row))
                      for row in con.execute(validation_sql).fetchall()]
        tables = {}
        for name in ("dim_company", "dim_location", "fact_job_posting"):
            tables[name] = con.execute(f"SELECT count(*) FROM {name}").fetchone()[0]
        views = {name: con.execute(f"SELECT count(*) FROM {name}").fetchone()[0]
                 for name in ("vw_job_counts_by_company_location_period", "vw_salary_analysis")}
        result = {"input_rows": expected, "tables": tables, "views": views, "validation": validation}
        (database.parent / "m3_validation_report.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if any(row["status"] != "PASS" for row in validation):
            raise ValueError(f"DuckDB validation failed: {validation}")
        return result
    finally:
        con.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/processed/m2_ingestion/job_postings"))
    parser.add_argument("--database", type=Path, default=Path("data/processed/talentgraph.duckdb"))
    args = parser.parse_args()
    print(json.dumps(build_models(args.input, args.database), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
