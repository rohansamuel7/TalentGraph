import json
import tempfile
import unittest
from pathlib import Path

from talentgraph.m6_candidates import generate_candidates


class M6CandidateTests(unittest.TestCase):
    def test_generation_is_valid_and_deterministic(self):
        database = Path("/home/developer/talentgraph_data/talentgraph.duckdb")
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "first.json", Path(directory) / "second.json"
            result = generate_candidates(database, first)
            generate_candidates(database, second)
            self.assertEqual(result["candidate_count"], 300)
            self.assertEqual(result["experience_levels"], {"junior": 100, "mid": 120, "senior": 80})
            self.assertEqual(first.read_bytes(), second.read_bytes())
            artifact = json.loads(first.read_text())
            con = __import__("duckdb").connect(str(database), read_only=True)
            try:
                keys = {s[0] for s in con.execute("select skill_key from dim_skill").fetchall()}
            finally:
                con.close()
            self.assertEqual(len({c["candidate_key"] for c in artifact["candidates"]}), 300)
            self.assertTrue(all(c["synthetic_label"] and c["years_experience"] >= 0 for c in artifact["candidates"]))
            self.assertTrue(all(r["skill_key"] in keys for r in artifact["candidate_skills"]))
            self.assertEqual(len(artifact["candidate_skills"]), result["skill_relationship_count"])


if __name__ == "__main__": unittest.main()
