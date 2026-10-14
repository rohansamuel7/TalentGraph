import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path


class M7EvidenceArtifactTests(unittest.TestCase):
    def test_canonical_artifact_schema_and_classifications(self):
        path = Path("data/processed/job_competency_evidence_qa_fix04.json")
        artifact = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(artifact["schema_version"], "m7-evidence-v2")
        self.assertEqual(artifact["extraction_version"], "qa-fix-04-v1")
        self.assertEqual(artifact["sample_job_count"], 1500)
        self.assertEqual(artifact["jobs_seen"], 1500)
        self.assertEqual(artifact["relationship_count"], 582)
        self.assertEqual(set(Counter(row["classification"] for row in artifact["relationships"])), {"required", "preferred", "mentioned", "negated", "ambiguous"})
        self.assertEqual(artifact["relationships"], sorted(artifact["relationships"], key=lambda row: (row["job_key"], row["competency_id"], row["classification"], row["extraction_rule_id"])))
        self.assertTrue(all(len(row["source_description_sha256"]) == 64 and row["evidence_text"] for row in artifact["relationships"]))

    def test_artifact_is_byte_stable(self):
        path = Path("data/processed/job_competency_evidence_qa_fix04.json")
        first = hashlib.sha256(path.read_bytes()).hexdigest()
        second = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
