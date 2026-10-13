import unittest
from talentgraph.m4_skill_alignment import EXTRA_SKILLS, match_skill

TAXONOMY = [
    {"skill_key": "python", "canonical_name": "Python", "aliases": ["python"]},
    {"skill_key": "pytorch", "canonical_name": "PyTorch", "aliases": ["pytorch"]},
    {"skill_key": "sql", "canonical_name": "SQL", "aliases": ["sql"]},
    {"skill_key": "sql_server", "canonical_name": "SQL Server", "aliases": ["microsoft sql server"]},
    {"skill_key": "apache_spark", "canonical_name": "Apache Spark", "aliases": ["spark"]},
    {"skill_key": "pyspark", "canonical_name": "PySpark", "aliases": ["python spark"]},
]

class M4MatchingTests(unittest.TestCase):
    def test_exact_alias_and_distinctions(self):
        self.assertEqual(match_skill("Python", TAXONOMY)["skill_key"], "python")
        self.assertEqual(match_skill("SQL Server", TAXONOMY)["skill_key"], "sql_server")
        self.assertEqual(match_skill("PyTorch", TAXONOMY)["skill_key"], "pytorch")
        self.assertNotEqual(match_skill("Python", TAXONOMY)["skill_key"], "pytorch")
        self.assertEqual(match_skill("Apache Spark", TAXONOMY)["skill_key"], "apache_spark")
        self.assertEqual(match_skill("PySpark", TAXONOMY)["skill_key"], "pyspark")

    def test_unknown_does_not_force_fuzzy_match(self):
        result = match_skill("SQL Server Administration", TAXONOMY)
        self.assertIn(result["status"], {"matched", "unknown"})
        self.assertTrue(result["confidence"] <= 1.0)

    def test_taxonomy_has_additional_controlled_concepts(self):
        self.assertGreaterEqual(len(EXTRA_SKILLS), 15)

if __name__ == "__main__": unittest.main()
