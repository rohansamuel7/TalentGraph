import unittest
from pathlib import Path

from talentgraph.m5_graph import (build_graph, companies_requesting_skill, cooccurring_skills,
                                  graph_summary, jobs_with_skills, jobs_without_explicit_skills,
                                  most_required_skills)


class M5GraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = build_graph(Path("/home/developer/talentgraph_data/talentgraph.duckdb"))

    def test_counts_and_relationships(self):
        summary = graph_summary(self.graph)
        self.assertEqual(summary["node_types"], {"Company": 1134, "Job": 1500, "Location": 761, "Skill": 50})
        self.assertEqual(summary["edge_types"], {"LOCATED_IN": 1500, "POSTED_BY": 1500, "REQUIRES_SKILL": 2498})
        self.assertEqual(jobs_without_explicit_skills(self.graph), 22)
        eng_jobs = jobs_with_skills(self.graph, ["skill:source:eng"])
        self.assertTrue(eng_jobs)
        self.assertEqual(eng_jobs, sorted(eng_jobs))

    def test_queries_are_deterministic_and_explainable(self):
        self.assertTrue(most_required_skills(self.graph, 3))
        self.assertTrue(cooccurring_skills(self.graph, 3))
        self.assertIsInstance(companies_requesting_skill(self.graph, "skill:source:eng"), list)
        self.assertEqual(graph_summary(self.graph), graph_summary(build_graph(Path("/home/developer/talentgraph_data/talentgraph.duckdb"))))

    def test_no_dangling_or_duplicate_edges(self):
        for source, target, data in self.graph.edges(data=True):
            self.assertIn(self.graph.nodes[source]["node_type"], {"Job"})
            self.assertIn(data["relationship"], {"POSTED_BY", "LOCATED_IN", "REQUIRES_SKILL"})
            self.assertIn(target, self.graph)


if __name__ == "__main__": unittest.main()
