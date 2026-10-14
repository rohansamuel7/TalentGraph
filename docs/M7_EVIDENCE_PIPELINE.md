# M7 Evidence Pipeline

## Root cause of the previous 101-job result

M7 previously loaded `data/processed/job_competency_evidence.json`, whose schema was `qa-fix-01-v1`. It contained 403 requirement-context relationships across 270 jobs and no preserved QA-FIX-04 five-class output. After canonical-key and technical-category filtering, M7 saw 167 eligible relationships across 101 jobs and treated all of them as required.

This was stale lineage, not evidence that only 101 descriptions contained technical terms. The QA-FIX-04 extractor had already produced 582 classified mentions across 372 jobs, but only a diagnostic copy existed and M7 had no stable API for it.

## Canonical rebuild

`data/processed/job_competency_evidence_qa_fix04.json` is generated directly from the unchanged QA-FIX-04 extractor and the same 1,500 accepted descriptions. It is schema `m7-evidence-v2`, extraction version `qa-fix-04-v1`, contains 582 deterministically ordered relationships, and retains required, preferred, mentioned, negated, and ambiguous classes.

Each relationship includes the canonical `skill:*` competency ID, original `comp:*` extractor ID, classification, evidence text, source file and row, exact source-description SHA-256, extraction rule, and extraction version. The M7 loader validates schema, extraction version, and required provenance fields; it fails clearly on stale or incompatible artifacts.

## Coverage comparison

| Inventory | Previous M7 artifact | Canonical QA-FIX-04 artifact |
|---|---:|---:|
| Relationships before eligibility filtering | 403 | 582 |
| Eligible technical relationships | 167 | 233 |
| Jobs with required technical competencies | 101 | 80 |
| Preferred-only technical jobs | Not available | 7 |
| Jobs with non-required mentions but no required evidence | Not available | 44 |
| Jobs with no eligible detected technical evidence | Not available | 1,369 |

The canonical categories are mutually exclusive: 80 required, 7 preferred-only, 44 mentioned/negated/ambiguous without required or preferred evidence, and 1,369 with no eligible technical evidence. The last group includes descriptions with no dictionary match and matches outside the controlled taxonomy; it does not mean the descriptions contain no skills.

The required-job count falls from 101 to 80 because the old artifact promoted every legacy `requirement_context` relationship to required. QA-FIX-04 reclassified some of those mentions as preferred, mentioned, negated, or ambiguous, and canonical taxonomy filtering excludes unsupported competency IDs. This is a semantic correction, not an attempt to inflate coverage.

## Human review comparison

The QA-FIX-07 set remains separate from the production artifact. Across the 25 reviewed records, the canonical predictions preserve the same 13 comparable human/model disagreements documented in QA-FIX-07; the five no-dictionary records remain review cases rather than inferred negatives. No human label was promoted into the extraction artifact or global rule set. The 17-record comparable evaluation remains too small and selected to establish production accuracy.

## Determinism and limitations

The canonical artifact rebuild is byte-stable under the fixed input archive, sample, extractor version, and deterministic ordering. Current M7 evidence is complete for the latest extractor output, but the controlled taxonomy does not cover every competency suggested in QA-FIX-07 (for example SaaS, SharePoint, WMIS, and Foundation software). Those remain coverage gaps rather than automatically added skills.
