"""Bounded, deterministic PySpark ingestion for sampled job postings."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructField, StructType

SOURCE_COLUMNS = (
    "job_id", "company_name", "title", "description", "max_salary", "pay_period",
    "location", "company_id", "views", "med_salary", "min_salary",
    "formatted_work_type", "applies", "original_listed_time", "remote_allowed",
    "job_posting_url", "application_url", "application_type", "expiry", "closed_time",
    "formatted_experience_level", "skills_desc", "listed_time", "posting_domain",
    "sponsored", "work_type", "currency", "compensation_type", "normalized_salary",
    "zip_code", "fips",
)
RAW_SCHEMA = StructType([StructField(c, StringType(), True) for c in SOURCE_COLUMNS] +
                        [StructField("_corrupt_record", StringType(), True)])
OUTPUT_COLUMNS = (
    "job_key", "source_job_id", "source_company_id", "company_name_raw", "company_name",
    "title_raw", "title", "location_raw", "location", "work_type", "experience_level",
    "listed_at", "original_listed_at", "expires_at", "closed_at", "remote_allowed",
    "min_salary", "med_salary", "max_salary", "currency", "pay_period",
    "compensation_type", "source_file", "source_row_number", "ingestion_run_id",
    "retrieved_at_utc", "raw_record_hash",
)


def create_spark(app_name: str = "TalentGraph-M2-Ingestion") -> SparkSession:
    # Set launcher environment explicitly; Spark workers otherwise inherit the
    # system WSL Python even when the driver runs in the approved virtualenv.
    approved_python = sys.executable
    os.environ["PYSPARK_PYTHON"] = approved_python
    os.environ["PYSPARK_DRIVER_PYTHON"] = approved_python
    return (SparkSession.builder.master("local[2]").appName(app_name)
            .config("spark.driver.memory", "1g")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.default.parallelism", "2")
            .config("spark.pyspark.python", approved_python)
            .config("spark.pyspark.driver.python", approved_python)
            .config("spark.executorEnv.PYSPARK_PYTHON", approved_python)
            .config("spark.ui.enabled", "false").getOrCreate())


def _clean(column: str) -> F.Column:
    return F.when(F.trim(F.col(column)) == "", F.lit(None)).otherwise(F.trim(F.col(column)))


def _timestamp(column: str) -> F.Column:
    return F.when(F.col(column).rlike(r"^[0-9]+(?:\.[0-9]+)?$"),
                  F.to_timestamp(F.from_unixtime(F.col(column).cast("double") / 1000)))


def _reason(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "reject_reason",
        F.when(F.col("_corrupt_record").isNotNull(), "malformed_record")
        .when(F.col("job_id").isNull() | (F.trim("job_id") == ""), "missing_job_id")
        .when(F.col("listed_time").isNull() | (F.trim("listed_time") == ""), "missing_listed_time")
        .when(~F.col("listed_time").rlike(r"^[0-9]+(?:\.[0-9]+)?$"), "invalid_listed_time")
        .when(_timestamp("listed_time").isNull(), "invalid_listed_time")
        .otherwise(F.lit(None).cast("string")),
    )


def _read_csv_records(spark: SparkSession, input_csv: Path) -> DataFrame:
    """Frame CSV records with Python's RFC-4180 reader before Spark transforms them.

    The bounded M1 sample contains multiline fields and legacy unescaped quotes.
    Python's reader matches the writer contract and avoids Spark's parser-specific
    record splitting while retaining explicit Spark schema and transformations.
    """
    records: list[list[str | None]] = []
    with input_csv.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        header = next(reader)
        if header != list(SOURCE_COLUMNS):
            raise ValueError("input CSV header differs from observed posting schema")
        for row in reader:
            if len(row) == len(SOURCE_COLUMNS):
                records.append(row + [None])
            else:
                records.append((row[:len(SOURCE_COLUMNS)] +
                                [None] * max(0, len(SOURCE_COLUMNS) - len(row)) +
                                ["column_count_mismatch"]))
    # This is a sampled-CSV processing index, not the archive's logical row number.
    return (spark.createDataFrame(records, schema=RAW_SCHEMA)
            .withColumn("_source_row_number", F.monotonically_increasing_id()))


def _normalized(valid: DataFrame, source_file: str, run_id: str, retrieved: str) -> DataFrame:
    parsed = valid.withColumn("listed_ts", _timestamp("listed_time"))
    parsed = parsed.withColumn("original_ts", _timestamp("original_listed_time"))
    parsed = parsed.withColumn("expiry_ts", _timestamp("expiry")).withColumn("closed_ts", _timestamp("closed_time"))
    window = Window.partitionBy("job_id").orderBy(F.col("listed_ts").desc_nulls_last(), F.col("_source_row_number").asc())
    parsed = parsed.withColumn("_rn", F.row_number().over(window)).where(F.col("_rn") == 1)
    return parsed.select(
        F.concat(F.lit("linkedin:"), F.trim("job_id")).alias("job_key"),
        _clean("job_id").alias("source_job_id"), _clean("company_id").alias("source_company_id"),
        F.col("company_name").alias("company_name_raw"), _clean("company_name").alias("company_name"),
        F.col("title").alias("title_raw"), _clean("title").alias("title"),
        F.col("location").alias("location_raw"), _clean("location").alias("location"),
        _clean("work_type").alias("work_type"), _clean("formatted_experience_level").alias("experience_level"),
        F.col("listed_ts").alias("listed_at"), F.col("original_ts").alias("original_listed_at"),
        F.col("expiry_ts").alias("expires_at"), F.col("closed_ts").alias("closed_at"),
        F.when(F.lower(_clean("remote_allowed")).isin("1", "true", "yes"), True)
         .when(F.lower(_clean("remote_allowed")).isin("0", "false", "no"), False).otherwise(None).alias("remote_allowed"),
        *[F.col(c).cast("decimal(18,2)").alias(c) for c in ("min_salary", "med_salary", "max_salary")],
        _clean("currency").alias("currency"), _clean("pay_period").alias("pay_period"),
        _clean("compensation_type").alias("compensation_type"), F.lit(source_file).alias("source_file"),
        F.col("_source_row_number").alias("source_row_number"), F.lit(run_id).alias("ingestion_run_id"),
        F.lit(retrieved).alias("retrieved_at_utc"),
        F.sha2(F.concat_ws("|", *[F.coalesce(F.col(c), F.lit("")) for c in SOURCE_COLUMNS]), 256).alias("raw_record_hash"),
    )


def run_ingestion(input_csv: Path, output_dir: Path, spark: SparkSession | None = None) -> dict[str, Any]:
    own = spark is None
    spark = spark or create_spark()
    digest = hashlib.sha256(input_csv.read_bytes()).hexdigest()
    run_id = "m2-" + digest[:16]
    retrieved = datetime.fromtimestamp(input_csv.stat().st_mtime, timezone.utc).isoformat()
    raw = _read_csv_records(spark, input_csv)
    classified = _reason(raw)
    rejects = classified.where(F.col("reject_reason").isNotNull()).select(
        "job_id", "_source_row_number", "reject_reason", "_corrupt_record")
    valid = classified.where(F.col("reject_reason").isNull())
    normalized = _normalized(valid, input_csv.name, run_id, retrieved).orderBy("job_key")
    output_dir.mkdir(parents=True, exist_ok=True)
    normalized.write.mode("overwrite").parquet(str(output_dir / "job_postings"))
    rejects.write.mode("overwrite").parquet(str(output_dir / "rejects"))
    metrics = {"input_rows": raw.count(), "accepted_rows": normalized.count(), "rejected_rows": rejects.count(),
               "duplicate_job_ids_removed": raw.count() - normalized.count() - rejects.count(),
               "reject_reasons": {r["reject_reason"]: r["count"] for r in rejects.groupBy("reject_reason").count().collect()},
               "source_file": input_csv.name, "run_id": run_id, "retrieved_at_utc": retrieved}
    (output_dir / "quality_report.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if own:
        spark.stop()
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/processed/job_postings_sample.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/m2_ingestion"))
    args = parser.parse_args()
    print(json.dumps(run_ingestion(args.input, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
