# M7 Refined Matching

M7 now matches synthetic candidate competencies only against eligible technical evidence from the processed extraction artifact. The M4 job-skill bridge remains preserved for provenance and graph use, but broad source categories, industry labels, operations labels, and non-technical edges are excluded from matching.

## Evidence rules

- `required` and legacy `requirement_context` evidence form the primary required set.
- `preferred` evidence is tracked separately and never counted in required overlap.
- `mentioned`, `negated`, and `ambiguous` evidence are excluded.
- Duplicate job/competency evidence is collapsed by canonical skill key while retaining source, rule, and extraction version metadata.
- No eligible required evidence means `insufficient_evidence` and a null numeric overlap.
- One observed required competency is `limited_evidence`, even at `1/1` overlap.
- Two or more observed required competencies are `sufficient_for_limited_comparison`; this is a comparison heuristic, not confidence or suitability.

The current stable artifact is the versioned QA-FIX-04 canonical artifact. Preferred-only evidence is reported separately; M7 does not infer labels from the human review sample.

## Current evidence inventory

Across 1,500 jobs: 80 have eligible required technical evidence, 7 have preferred-only evidence, and the remainder are separated into non-required mentions or no eligible evidence. This is an extraction-artifact inventory, not a claim that the remaining descriptions contain no skills.

## Output and ranking

Each result includes candidate/job IDs, evidence status, required counts, matched and missing required competencies, separate preferred counts, evidence source, extraction version, nullable required overlap, and a plain-language explanation. The percentage measures matched extracted required competencies divided by observed extracted required competencies; it does not measure hiring probability, overall suitability, or completeness of the job description.

Ranking prioritizes sufficient evidence, then limited evidence, then insufficient evidence. Within those groups it uses required overlap, observed required count, preferred matches, and stable job ID. Candidate-to-job and job-to-candidate ranking use the same ordering.

Examples from the deterministic synthetic artifact:

- Strong observed overlap: `linkedin:3885805688` has 5 observed required competencies; candidate `synthetic:candidate:000001` matches 2 (`Python`, `SQL`) and is `sufficient_for_limited_comparison`.
- One-skill limited evidence: `linkedin:3884249830` has 1 observed requirement and candidate `synthetic:candidate:000001` matches `1/1`; status remains `limited_evidence`.
- Insufficient evidence: `linkedin:141969940` has no eligible extracted required competency and receives no numeric overlap.

## Limitations

The controlled taxonomy does not cover every competency suggested in QA-FIX-07. The selected QA-FIX-07 review set is not a ranking-accuracy benchmark, and M7 does not infer unobserved requirements.
