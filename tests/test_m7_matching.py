import unittest
from pathlib import Path

from talentgraph.m7_matching import rank_candidates_for_job, rank_jobs_for_candidate, score_candidate_job


class M7MatchingTests(unittest.TestCase):
    def setUp(self):
        self.job = {"job_key": "linkedin:test", "title": "Test", "company_name": "Synthetic"}
        self.names = {"skill:a": "Alpha", "skill:b": "Beta", "skill:it": "Information Technology", "skill:python": "Python"}

    def test_full_partial_and_zero_overlap(self):
        full = score_candidate_job("c", {"skill:a", "skill:b"}, self.job, {"skill:a", "skill:b"}, self.names)
        partial = score_candidate_job("c", {"skill:a"}, self.job, {"skill:a", "skill:b"}, self.names)
        zero = score_candidate_job("c", set(), self.job, {"skill:a"}, self.names)
        self.assertEqual(full["skill_coverage"], 1.0); self.assertEqual(partial["skill_coverage"], 0.5); self.assertEqual(zero["skill_coverage"], 0.0)
        self.assertEqual(partial["missing_skills"], ["Beta"])

    def test_no_evidence_is_not_perfect(self):
        row = score_candidate_job("c", {"skill:a"}, self.job, set(), self.names)
        self.assertEqual(row["skill_coverage"], 0.0)
        self.assertEqual(row["evidence_status"], "insufficient_skill_evidence")

    def test_tie_top_k_reverse_and_broad_label(self):
        jobs = [{"job_key": "linkedin:a", "title": "A", "company_name": "X"}, {"job_key": "linkedin:b", "title": "B", "company_name": "Y"}]
        reference = {"job_skills": {"linkedin:a": {"skill:a"}, "linkedin:b": {"skill:b"}}, "skill_names": self.names}
        candidates = {"synthetic:candidate:000001": {"skill:it"}, "synthetic:candidate:000002": {"skill:python"}}
        ranked = rank_jobs_for_candidate("synthetic:candidate:000001", jobs, candidates, reference, 1)
        self.assertEqual(ranked[0]["job_key"], "linkedin:a")
        reverse = rank_candidates_for_job("linkedin:a", jobs, candidates, reference, 2)
        self.assertEqual([r["candidate_key"] for r in reverse], ["synthetic:candidate:000001", "synthetic:candidate:000002"])
        self.assertEqual(score_candidate_job("c", {"skill:it"}, self.job, {"skill:python"}, self.names)["skill_coverage"], 0.0)

    def test_real_data_integration_and_repeatability(self):
        from talentgraph.m7_matching import load_reference_data
        jobs, candidate_skills, reference = load_reference_data(Path("/home/developer/talentgraph_data/talentgraph.duckdb"), Path("data/processed/synthetic_candidates.json"))
        first = rank_jobs_for_candidate("synthetic:candidate:000001", jobs, candidate_skills, reference, 5)
        second = rank_jobs_for_candidate("synthetic:candidate:000001", jobs, candidate_skills, reference, 5)
        self.assertEqual(first, second); self.assertEqual(len(jobs), 1500); self.assertEqual(len(candidate_skills), 300)


if __name__ == "__main__": unittest.main()
