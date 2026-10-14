import hashlib
import unittest
from pathlib import Path

from fastapi import HTTPException

from talentgraph import api
from talentgraph.api_data import technical_skill_frequency


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = None

    def test_health_and_overview(self):
        body = api.overview()
        self.assertEqual(body["sampled_jobs"], 1500)
        self.assertEqual(body["synthetic_candidates"], 300)
        self.assertEqual(api.health()["status"], "ok")

    def test_skill_frequency_counts_distinct_jobs_and_eligible_classes(self):
        jobs = [{"job_key": "one"}, {"job_key": "two"}, {"job_key": "three"}]
        reference = {"skill_names": {"sql": "SQL", "py": "Python"}, "job_evidence": {
            "one": {"required": {"sql": {}}, "preferred": {"sql": {}, "py": {}}, "non_scoring": {}},
            "two": {"required": {"sql": {}}, "preferred": {}, "non_scoring": {}},
            "three": {"required": {}, "preferred": {}, "non_scoring": {"py": {}}},
        }}
        self.assertEqual(technical_skill_frequency(jobs, reference), [
            {"competency_id": "sql", "competency_name": "SQL", "job_count": 2},
            {"competency_id": "py", "competency_name": "Python", "job_count": 1},
        ])
        live = api.skill_frequency()["items"]
        self.assertTrue(live)
        self.assertTrue(all(item["job_count"] > 0 for item in live))
        self.assertIn("/api/insights/skill-frequency", {route.path for route in api.app.routes})

    def test_job_search_pagination_and_invalid_filter(self):
        response = api.jobs(limit=3, offset=2)
        self.assertEqual(len(response["items"]), 3)
        with self.assertRaises(HTTPException):
            api.jobs(evidence_status="bad")

    def test_job_detail_preserves_evidence_provenance(self):
        job_id = api.jobs(evidence_status="required", limit=1)["items"][0].job_id
        body = api.job_detail(job_id)
        self.assertTrue(body["required"])
        evidence = body["required"][0].model_dump()
        self.assertIn("source_description_sha256", evidence)
        self.assertIn("source_location", evidence)

    def test_candidate_search_and_missing_records(self):
        response = api.candidates(role_family="data_engineering", limit=2)
        self.assertTrue(all(item.synthetic for item in response["items"]))
        with self.assertRaises(HTTPException):
            api.candidate_detail("missing")

    def test_matches_require_one_subject_and_preserve_insufficient_null(self):
        with self.assertRaises(HTTPException):
            api.matches()
        response = api.matches(candidate_id="synthetic:candidate:000001", limit=50)
        for item in response["items"]:
            if item.evidence_status == "insufficient_evidence":
                self.assertIsNone(item.required_skill_overlap)

    def test_graph_edges_are_typed_and_source_backed(self):
        body = api.neighborhood("synthetic:candidate:000001")
        body = body.model_dump()
        nodes = {node["id"] for node in body["nodes"]}
        self.assertTrue(all(edge["source"] in nodes and edge["target"] in nodes for edge in body["edges"]))
        self.assertTrue({edge["relationship"] for edge in body["edges"]} <= {"HAS_SKILL", "REQUIRES_SKILL", "PREFERS_SKILL"})
        one_hop = api.neighborhood("synthetic:candidate:000001", hops=1).model_dump()
        self.assertFalse(any(node["type"] == "job" for node in one_hop["nodes"]))

    def test_job_graph_and_invalid_root(self):
        job_id = api.jobs(limit=1)["items"][0].job_id
        self.assertEqual(api.neighborhood(job_id).root, job_id)
        with self.assertRaises(HTTPException):
            api.neighborhood("missing")

    def test_database_file_hash_unchanged(self):
        path = Path("/home/developer/talentgraph_data/talentgraph.duckdb")
        before = hashlib.sha256(path.read_bytes()).digest()
        api.overview()
        self.assertEqual(hashlib.sha256(path.read_bytes()).digest(), before)


if __name__ == "__main__":
    unittest.main()
