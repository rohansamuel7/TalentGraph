# Engineering Standards

## Python
Use modules with single responsibilities, type hints on public interfaces, docstrings for non-obvious behavior, deterministic ordering, and explicit configuration. Keep functions testable and avoid hidden global state.

## SQL and data
Use explicit columns and keys, documented grain, readable CTEs, parameterized values, and DuckDB-compatible SQL. Validate nullability, uniqueness, referential integrity, row counts, and unexpected categories.

## Testing
Use Pytest with small fixtures and synthetic data. Test happy paths, malformed inputs, empty inputs, duplicate inputs, thresholds, and reruns. Separate unit, integration, and smoke checks.

## Logging and errors
Use structured, actionable logs with record counts and run identifiers; never log secrets or raw sensitive values. Fail fast on broken contracts, classify recoverable bad records, and preserve error samples for diagnosis.

## Performance
Bound memory, select only required columns, partition only when useful, limit Spark local threads, avoid expensive graph layouts, and measure before optimizing.

## Security
Use environment variables for secrets, keep local databases and data ignored, sanitize demo data, and review `git diff --cached` before commits.
