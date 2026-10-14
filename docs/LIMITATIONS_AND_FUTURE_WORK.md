# Limitations and future work

TalentGraph is a local, evidence-based demonstration. Its outputs describe available text and modeled relationships, not people or hiring outcomes.

## Current limitations

- **Bounded source:** the system uses 1,500 LinkedIn postings selected deterministically from one local archive. The sample is repeatable for that archive but not statistically representative. The exact published version of the user-provided archive is not independently established from its contents.
- **Fictional candidates:** all 300 candidate profiles are synthetic role templates. Their overlap scores demonstrate the data model; they say nothing about real applicants.
- **Sparse technical evidence:** current mutually exclusive job groups are 80 with required technical evidence, 7 preferred-only, 44 non-required-only, and 1,369 without eligible technical evidence. Missing evidence is not proof of missing skills.
- **Heuristic extraction:** regular expressions and nearby context classify observed terms as required, preferred, mentioned, negated, or ambiguous. Job descriptions can omit, abbreviate, or ambiguously describe requirements; the controlled vocabulary is incomplete.
- **Limited review:** a small selected human review identified disagreements, but cannot establish general precision or recall for all postings.
- **Comparison scope:** observed required-skill overlap is not suitability, hiring probability, competency proficiency, or a fair ranking of real people. One observed requirement is explicitly limited evidence; none produces an unavailable numeric overlap.
- **Legacy category meaning:** M4 source skills include broad occupational and functional categories. They are retained for lineage and the M5 graph, but are not treated as verified technical requirements by current matching or API graph projection.
- **Source-row traceability:** M2's Spark processing index and archive CSV row enumeration are different schemes. Direct one-to-one row-number provenance has not been verified across all artifacts, although job IDs, source names, and description hashes are retained.
- **Local operation:** the API depends on a fixed local production database path and ignored JSON artifacts. There is no scheduled production orchestration, automated monitoring, deployment package, or independent clean-machine reproduction test.
- **Browser verification:** code and build checks are recorded, but some visual and interactive behaviors still require manual browser inspection.

## Practical next steps

1. **Strengthen source traceability.** Carry the archive's logical record number through the sample and Spark stages, then test that it resolves to the same job ID and description hash. Do not relabel existing indices without verification.
2. **Broaden reviewed evidence.** Review more diverse descriptions and disagreement cases; measure class-specific error rates before changing extractor rules.
3. **Expand data responsibly.** Obtain and version new source data under its terms, verify physical schemas and licensing, and compare quality across refreshes. Revisit sampling strategy before making population claims.
4. **Improve quality reporting.** Add explicit checks for source-to-curated record lineage, artifact compatibility, unexpected nulls, and coverage drift with clear failure thresholds.
5. **Make processing operational.** Build on the existing deterministic and rerun checks with validated incremental inputs, then add a bounded Airflow schedule, retries, run logs, and alerts only after local recovery paths are tested.
6. **Test the full user path.** Add browser checks for route navigation, themes, graph expansion, and charts, plus larger-data performance measurements and a documented deployment configuration.

The current pipeline and checks are described in [Data pipeline](DATA_PIPELINE.md); package and runtime versions are in [Technology stack](TECH_STACK.md).
