"""Role-family templates for synthetic technical candidate profiles."""

from __future__ import annotations

from typing import Iterable

ROLE_FAMILIES = {
    "data_engineering": ("skill:python", "skill:sql", "skill:apache_spark", "skill:pyspark", "skill:airflow", "skill:duckdb", "skill:spark_sql"),
    "analytics": ("skill:python", "skill:sql", "skill:pandas", "skill:duckdb", "skill:spark_sql", "skill:networkx"),
    "software_engineering": ("skill:python", "skill:java", "skill:scala", "skill:sql", "skill:networkx"),
    "cloud_platform": ("skill:python", "skill:aws", "skill:azure", "skill:gcp", "skill:airflow", "skill:apache_spark", "skill:sql"),
}
ROLE_ORDER = tuple(ROLE_FAMILIES)
SENIORITY_BANDS = (("junior", 100, 0, 2), ("mid", 120, 3, 7), ("senior", 80, 8, 15))


def technical_taxonomy(taxonomy: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    """Index only technical taxonomy rows allowed in candidate bridges."""
    allowed = {"technical", "cloud", "data_engineering"}
    return {row["skill_key"]: row for row in taxonomy if row["category"] in allowed}


def choose_skills(role_family: str, level: str, available: dict[str, dict[str, str]], variation: int) -> list[dict[str, str]]:
    """Select a coherent core plus deterministic optional competencies."""
    keys = [key for key in ROLE_FAMILIES[role_family] if key in available]
    core_count = 3 if level == "junior" else 4 if level == "mid" else 5
    optional = [key for index, key in enumerate(keys[core_count:]) if (variation + index) % 3 != 1]
    selected = keys[:core_count] + optional[: (1 if level == "junior" else 2)]
    return [available[key] for key in selected]
