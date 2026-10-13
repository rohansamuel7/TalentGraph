import unittest
from talentgraph.qa_fix_extraction import _extract_from_text, classify_taxonomy

class QAExtractionTests(unittest.TestCase):
    def test_positive_aliases_and_boundaries(self):
        text = "Required: Python, SQL Server, PySpark, and Git. JavaScript is unrelated. Go programming language is preferred."
        found = _extract_from_text("linkedin:test", text, "fixture.csv", 2)
        by_id = {x["competency_id"]: x for x in found}
        ids = set(by_id)
        self.assertNotIn("comp:java", ids)
        self.assertIn("comp:python", ids); self.assertIn("comp:sql_server", ids); self.assertIn("comp:pyspark", ids); self.assertIn("comp:git", ids); self.assertIn("comp:go", ids)
        self.assertNotIn("comp:sql", ids)
        self.assertEqual(by_id["comp:python"]["evidence_classification"], "required")
        self.assertEqual(by_id["comp:go"]["evidence_classification"], "preferred")

    def test_negative_and_incidental_mentions(self):
        text = "No experience with Docker is required. Our website mentions Spark. SQL is not required."
        found = {x["competency_id"]: x for x in _extract_from_text("linkedin:test", text, "fixture.csv", 2)}
        self.assertEqual(found["comp:docker"]["evidence_classification"], "negated")
        self.assertEqual(found["comp:sql"]["evidence_classification"], "negated")

    def test_requirement_and_preferred_phrases(self):
        text = "Proficiency in SQL. Must be computer literate in Excel. Effective working skills of Excel. Python scripting is preferred. Highly desirable: AWS. Experience with Git a plus."
        found = {x["competency_id"]: x for x in _extract_from_text("linkedin:test", text, "fixture.csv", 2)}
        self.assertEqual(found["comp:sql"]["evidence_classification"], "required")
        self.assertEqual(found["comp:excel"]["evidence_classification"], "required")
        self.assertEqual(found["comp:python"]["evidence_classification"], "preferred")
        self.assertEqual(found["comp:aws"]["evidence_classification"], "preferred")
        self.assertEqual(found["comp:git"]["evidence_classification"], "preferred")

    def test_ordinary_english_excel_is_not_a_competency(self):
        self.assertNotIn("comp:excel", {x["competency_id"] for x in _extract_from_text("linkedin:test", "Do you excel in a team environment?", "fixture.csv", 2)})

    def test_classification_is_explicit(self):
        rows = [("skill:python", "Python", "technical"), ("skill:source:sale", "Sales", "business")]
        result = classify_taxonomy(rows)
        self.assertEqual([r["semantic_type"] for r in result], ["technical_competency", "functional_skill"])

    def test_manual_precision_recall_fixture(self):
        cases = [
            ("Required Python and SQL.", {"comp:python", "comp:sql"}),
            ("Experience with PySpark and AWS is required.", {"comp:pyspark", "comp:aws"}),
            ("Docker is not required; no experience with Go is needed.", {"comp:docker"}),
            ("The website mentions Spark, but this role requires Excel.", {"comp:excel"}),
            ("JavaScript experience is required.", set()),
        ]
        true_positive = false_positive = false_negative = 0
        for text, expected in cases:
            actual = {r["competency_id"] for r in _extract_from_text("linkedin:fixture", text, "fixture.csv", 2)}
            true_positive += len(actual & expected); false_positive += len(actual - expected); false_negative += len(expected - actual)
        self.assertEqual((true_positive, false_positive, false_negative), (6, 0, 0))
        self.assertEqual(true_positive / (true_positive + false_positive), 1.0)
        self.assertEqual(true_positive / (true_positive + false_negative), 1.0)

if __name__ == "__main__": unittest.main()
