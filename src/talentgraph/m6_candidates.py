"""Deterministic synthetic candidates with technical role-family profiles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import duckdb

from .m6_profiles import ROLE_ORDER, SENIORITY_BANDS, choose_skills, technical_taxonomy

SEED = 20261012
LOCATIONS = ("Austin, TX", "Boston, MA", "Chicago, IL", "Denver, CO", "New York, NY", "Seattle, WA", "Remote - US")
FIRST_NAMES = ("Avery", "Casey", "Jordan", "Morgan", "Riley", "Taylor", "Cameron", "Quinn", "Parker", "Drew")
LAST_NAMES = ("North", "River", "Cedar", "Vale", "Rowan", "Hart", "Stone", "Reed", "Lane", "Briar")


def _load_taxonomy(database: Path) -> list[dict[str, str]]:
    """Read the production taxonomy without writing to the database."""
    con = duckdb.connect(str(database), read_only=True)
    try:
        return [{"skill_key": row[0], "canonical_name": row[1], "category": row[2]} for row in con.execute("SELECT skill_key, canonical_name, category FROM dim_skill ORDER BY skill_key").fetchall()]
    finally:
        con.close()


def _candidate(number: int, band: str, years: int, role: str, skills: list[dict[str, str]], seed: int) -> dict[str, Any]:
    """Build one explicitly synthetic candidate record."""
    key = f"synthetic:candidate:{number:06d}"
    return {"candidate_key": key, "candidate_number": number, "synthetic_label": True,
            "fictional_name": f"{FIRST_NAMES[(number - 1) % 10]} {LAST_NAMES[((number - 1) // 10) % 10]}",
            "role_family": role, "experience_level": band, "years_experience": years,
            "location_preference": LOCATIONS[(number - 1) % len(LOCATIONS)], "generation_seed": seed,
            "skills": [skill["skill_key"] for skill in skills]}


def generate_candidates(database: Path, output: Path, seed: int = SEED) -> dict[str, Any]:
    """Generate 300 deterministic technical candidates from role templates."""
    available = technical_taxonomy(_load_taxonomy(database))
    if not available:
        raise ValueError("No allowed technical taxonomy rows are available")
    candidates: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    number = 0
    # Fixed band counts, seed, and role order make the demonstration profiles
    # reproducible without implying they represent real applicants.
    for band, count, minimum, maximum in SENIORITY_BANDS:
        for offset in range(count):
            number += 1
            role = ROLE_ORDER[(number - 1) % len(ROLE_ORDER)]
            years = minimum + ((number * 7 + seed) % (maximum - minimum + 1))
            skills = choose_skills(role, band, available, number)
            candidate = _candidate(number, band, years, role, skills, seed)
            candidates.append(candidate)
            for rank, skill in enumerate(skills, 1):
                relationships.append({"relationship_key": f"{candidate['candidate_key']}:skill:{rank:02d}", "candidate_key": candidate["candidate_key"], "skill_key": skill["skill_key"], "skill_name": skill["canonical_name"], "source_type": "synthetic_role_template", "generation_seed": seed})
    artifact = {"schema_version": "m6-v2", "generation_seed": seed, "taxonomy_source": "dim_skill", "candidate_count": len(candidates), "candidates": candidates, "candidate_skills": relationships}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"candidate_count": len(candidates), "skill_relationship_count": len(relationships), "experience_levels": {band: sum(c["experience_level"] == band for c in candidates) for band, *_ in SENIORITY_BANDS}, "role_families": {role: sum(c["role_family"] == role for c in candidates) for role in ROLE_ORDER}, "distinct_skills_used": len({r["skill_key"] for r in relationships}), "seed": seed}


def main() -> None:
    """Parse paths and generate the synthetic candidate artifact."""
    parser = argparse.ArgumentParser(); parser.add_argument("--database", type=Path, default=Path("/home/developer/talentgraph_data/talentgraph.duckdb")); parser.add_argument("--output", type=Path, default=Path("data/processed/synthetic_candidates.json")); args = parser.parse_args()
    print(json.dumps(generate_candidates(args.database, args.output), indent=2, sort_keys=True))


if __name__ == "__main__": main()
