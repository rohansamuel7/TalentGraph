"""Deterministic synthetic candidate generator backed by the M4 taxonomy."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

import duckdb

SEED = 20261012
BANDS = (("junior", 100, 0, 2), ("mid", 120, 3, 7), ("senior", 80, 8, 20))
LOCATIONS = ("Austin, TX", "Boston, MA", "Chicago, IL", "Denver, CO", "New York, NY", "Seattle, WA", "Remote - US")
FIRST_NAMES = ("Avery", "Casey", "Jordan", "Morgan", "Riley", "Taylor", "Cameron", "Quinn", "Parker", "Drew")
LAST_NAMES = ("North", "River", "Cedar", "Vale", "Rowan", "Hart", "Stone", "Reed", "Lane", "Briar")


def _load_taxonomy(database: Path) -> list[dict[str, str]]:
    con = duckdb.connect(str(database), read_only=True)
    try:
        return [{"skill_key": r[0], "canonical_name": r[1], "category": r[2]}
                for r in con.execute("SELECT skill_key, canonical_name, category FROM dim_skill ORDER BY skill_key").fetchall()]
    finally:
        con.close()


def generate_candidates(database: Path, output: Path, seed: int = SEED) -> dict[str, Any]:
    taxonomy = _load_taxonomy(database)
    if not taxonomy:
        raise ValueError("dim_skill is empty")
    rng = random.Random(seed)
    candidates: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for band, count, min_years, max_years in BANDS:
        for _ in range(count):
            number = len(candidates) + 1
            years = rng.randint(min_years, max_years)
            # Vary coverage while keeping every profile grounded in taxonomy keys.
            skill_count = rng.randint(2, 4) if band == "junior" else rng.randint(3, 6) if band == "mid" else rng.randint(4, 8)
            selected = sorted(rng.sample(taxonomy, min(skill_count, len(taxonomy))), key=lambda x: x["skill_key"])
            candidate_key = f"synthetic:candidate:{number:06d}"
            candidate = {"candidate_key": candidate_key, "candidate_number": number, "synthetic_label": True,
                         "fictional_name": f"{FIRST_NAMES[(number - 1) % len(FIRST_NAMES)]} {LAST_NAMES[((number - 1) // len(FIRST_NAMES)) % len(LAST_NAMES)]}",
                         "experience_level": band, "years_experience": years,
                         "location_preference": LOCATIONS[rng.randrange(len(LOCATIONS))], "generation_seed": seed,
                         "skills": [s["skill_key"] for s in selected]}
            candidates.append(candidate)
            for rank, skill in enumerate(selected, 1):
                relationships.append({"relationship_key": f"{candidate_key}:skill:{rank:02d}", "candidate_key": candidate_key,
                                      "skill_key": skill["skill_key"], "skill_name": skill["canonical_name"],
                                      "source_type": "synthetic_taxonomy_sampling", "generation_seed": seed})
    artifact = {"schema_version": "m6-v1", "generation_seed": seed, "taxonomy_source": "dim_skill", "candidate_count": len(candidates),
                "candidates": candidates, "candidate_skills": relationships}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"candidate_count": len(candidates), "skill_relationship_count": len(relationships),
            "experience_levels": {band: sum(c["experience_level"] == band for c in candidates) for band, *_ in BANDS},
            "distinct_skills_used": len({r["skill_key"] for r in relationships}), "seed": seed}


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--database", type=Path, default=Path("/home/developer/talentgraph_data/talentgraph.duckdb")); parser.add_argument("--output", type=Path, default=Path("data/processed/synthetic_candidates.json")); args = parser.parse_args()
    print(json.dumps(generate_candidates(args.database, args.output), indent=2, sort_keys=True))


if __name__ == "__main__": main()
