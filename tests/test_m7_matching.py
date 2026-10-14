import unittest
import json
import tempfile
from pathlib import Path

from talentgraph.m7_matching import rank_candidates_for_job, rank_jobs_for_candidate, score_candidate_job
from talentgraph.m7_evidence import load_job_evidence


class M7MatchingTests(unittest.TestCase):
    def setUp(self):
        self.job = {"job_key": "linkedin:test", "title": "Test", "company_name": "Synthetic"}
        self.names = {"skill:a": "Alpha", "skill:b": "Beta", "skill:python": "Python"}

    def test_single_requirement_is_limited_evidence(self):
        evidence = {"required": {"skill:a": {"version": "v", "source": "description"}}, "preferred": {}}
        row = score_candidate_job("c", {"skill:a"}, self.job, evidence, self.names)
        self.assertEqual(row["required_skill_overlap"], 1.0)
        self.assertEqual(row["evidence_status"], "limited_evidence")
        self.assertIn("1 of 1", row["explanation"])

    def test_no_requirements_have_no_numeric_score(self):
        row = score_candidate_job("c", {"skill:a"}, self.job, {}, self.names)
        self.assertIsNone(row["required_skill_overlap"])
        self.assertEqual(row["evidence_status"], "insufficient_evidence")

    def test_preferred_is_separate_and_missing_is_explained(self):
        evidence = {"required": {"skill:a": {"version": "v", "source": "description"}, "skill:b": {"version": "v", "source": "description"}}, "preferred": {"skill:python": {"version": "v", "source": "description"}}}
        row = score_candidate_job("c", {"skill:a"}, self.job, evidence, self.names)
        self.assertEqual(row["matched_required_count"], 1)
        self.assertEqual(row["missing_skills"], ["Beta"])
        self.assertEqual(row["matched_preferred_count"], 0)
        self.assertEqual(row["missing_preferred_skills"], ["Python"])

    def test_ranking_prioritizes_evidence_and_is_deterministic(self):
        jobs = [{"job_key": "linkedin:a", "title": "A", "company_name": "X"}, {"job_key": "linkedin:b", "title": "B", "company_name": "Y"}]
        evidence = {"linkedin:a": {"required": {"skill:a": {"version": "v", "source": "description"}}, "preferred": {}}, "linkedin:b": {}}
        reference = {"job_evidence": evidence, "skill_names": self.names}
        candidates = {"synthetic:candidate:000001": {"skill:a"}, "synthetic:candidate:000002": {"skill:python"}}
        first = rank_jobs_for_candidate("synthetic:candidate:000001", jobs, candidates, reference, 2)
        second = rank_jobs_for_candidate("synthetic:candidate:000001", jobs, candidates, reference, 2)
        self.assertEqual(first, second)
        self.assertEqual(first[0]["job_key"], "linkedin:a")
        reverse = rank_candidates_for_job("linkedin:a", jobs, candidates, reference, 2)
        self.assertEqual(reverse[0]["candidate_key"], "synthetic:candidate:000001")

    def test_real_data_integration_and_repeatability(self):
        from talentgraph.m7_matching import load_reference_data
        database = Path("/home/developer/talentgraph_data/talentgraph.duckdb")
        jobs, candidate_skills, reference = load_reference_data(database, Path("data/processed/synthetic_candidates.json"))
        first = rank_jobs_for_candidate("synthetic:candidate:000001", jobs, candidate_skills, reference, 5)
        second = rank_jobs_for_candidate("synthetic:candidate:000001", jobs, candidate_skills, reference, 5)
        self.assertEqual(first, second)
        self.assertEqual(len(jobs), 1500)
        self.assertEqual(len(candidate_skills), 300)
        self.assertTrue(reference["job_evidence"])

    def test_stale_evidence_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "stale.json"
            path.write_text(json.dumps({"schema_version": "qa-fix-01-v1", "relationships": []}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Incompatible evidence schema"):
                load_job_evidence(path, {})


if __name__ == "__main__":
    unittest.main()
