# QA-FIX-07 Extraction Quality Evaluation

- Records: 25
- Comparable prediction records: 17
- Unresolved records: 5

Final label counts: ambiguous=5, incidental=1, preferred=4, required=15.

## Java resolution

The raw human label `required/preferred` is preserved. It is resolved to `preferred` because the full description says: `two or more development languages such as Java or Python`; Java is an example/alternative, not individually mandatory.

## Confusion matrix

Rows are finalized human labels; columns are QA-FIX-04 predictions.

| Actual \ Predicted | required | preferred | incidental | negated | ambiguous |
|---|---:|---:|---:|---:|---:|

| required | 11 | 0 | 0 | 0 | 2 |
| preferred | 1 | 1 | 0 | 0 | 1 |
| incidental | 0 | 1 | 0 | 0 | 0 |
| negated | 0 | 0 | 0 | 0 | 0 |
| ambiguous | 0 | 0 | 0 | 0 | 0 |

## Supported metrics

Metrics use only the 17 records with a five-class prediction. Five no-dictionary-term cases have `no_candidate_term`, and three explicit mentions have `mentioned`; both are outside the five-class comparison and are reported as detection/classification gaps.

| Class | Support | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| required | 13 | 0.917 | 0.846 | 0.880 |
| preferred | 3 | 0.500 | 0.333 | 0.400 |
| incidental | 1 | 0.000 | 0.000 | 0.000 |
| ambiguous | 0 | 0.000 | 0.000 | 0.000 |

## No-dictionary-term review

The five descriptions do not establish absence of skills. Coverage suggestions are evidence-backed prompts only:

- **linkedin:3884806695** — possible coverage: basic math; problem-solving. Exact source quotation: `You will need to possess basic math and solid problem-solving skills`
- **linkedin:3884856205** — possible coverage: SaaS; sales-funnel optimization; go-to-market strategy. Exact source quotation: `Your mission: to optimize our sales funnel, create powerful go-to-market strategies`
- **linkedin:3884875543** — possible coverage: SaaS platform. Exact source quotation: `What We Do: J. Galt Finance Suite offers a SaaS platform and consultative services`
- **linkedin:3887480827** — possible coverage: Foundation software. Exact source quotation: `Foundation software experience preferred, but not required.`
- **linkedin:3887575585** — possible coverage: SharePoint; Work Management Information System; data entry; report generation. Exact source quotation: `The Administrative Assistant - Maintenance role provides administrative support and clerical assistance, timekeeping, data entry, report generation services, and SharePoint site overview`

## Interpretation

The set is selected and only 25 records; these metrics do not establish production-wide accuracy. Disagreements involving explicit dictionary terms are extractor classification/detection issues. The five no-term records are taxonomy coverage gaps or non-technical competency cases, not confirmed extractor false negatives. Human labels remain reviewed judgments, not general ground truth.
