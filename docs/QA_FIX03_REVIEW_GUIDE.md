# QA-FIX-03 Human Review Guide

Review `data/processed/qa_fix03_human_review.csv` one candidate competency at a time. Do not treat the existing extraction decision as ground truth. Enter exactly one `confirmed_label` from:

- `required` — explicitly required competency
- `preferred` — explicitly preferred or optional competency
- `incidental` — mentioned without evidence that the role seeks it
- `negated` — explicitly not required, prohibited, or disclaimed
- `ambiguous` — insufficient context to decide

Use `reviewer_rationale` for a short explanation. Do not paste full descriptions, URLs, names, contact details, or other personal information into the worksheet.
