import unittest
from pathlib import Path

from talentgraph.api_data import load_dataset
from talentgraph.network_projection import build_projection


class NetworkProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).parents[1]
        cls.data = load_dataset(
            Path("/home/developer/talentgraph_data/talentgraph.duckdb"),
            root / "data/processed/synthetic_candidates.json",
            root / "data/processed/job_competency_evidence_qa_fix04.json",
        )
        cls.projection = build_projection(cls.data, "synthetic:candidate:000001")

    def test_nodes_and_edges_are_source_backed(self):
        node_ids = {node["id"] for node in self.projection["nodes"]}
        self.assertTrue(self.projection["nodes"])
        self.assertTrue(all(edge["source"] in node_ids and edge["target"] in node_ids for edge in self.projection["edges"]))

    def test_requirement_edge_classes_are_distinct(self):
        kinds = {edge["kind"] for edge in self.projection["edges"]}
        self.assertTrue(kinds <= {"has_skill", "requires_skill", "prefers_skill"})
        self.assertFalse(any(edge["kind"] == "requires_skill" and edge["kind"] == "prefers_skill" for edge in self.projection["edges"]))

    def test_projection_is_bounded_and_deterministic(self):
        again = build_projection(self.data, "synthetic:candidate:000001")
        self.assertEqual(self.projection, again)
        self.assertLessEqual(len(self.projection["nodes"]), 1 + 4 + 24)


if __name__ == "__main__":
    unittest.main()
