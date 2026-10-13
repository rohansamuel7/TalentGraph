SELECT 'fact_row_count' AS check_name, count(*)::BIGINT AS check_value,
       CASE WHEN count(*) = {{EXPECTED_ROWS}} THEN 'PASS' ELSE 'FAIL' END AS status
FROM fact_job_posting
UNION ALL
SELECT 'fact_unique_job_key', count(*) - count(DISTINCT job_key),
       CASE WHEN count(*) = count(DISTINCT job_key) THEN 'PASS' ELSE 'FAIL' END
FROM fact_job_posting
UNION ALL
SELECT 'orphan_company_keys', count(*),
       CASE WHEN count(*) = 0 THEN 'PASS' ELSE 'FAIL' END
FROM fact_job_posting f LEFT JOIN dim_company d USING (company_key)
WHERE d.company_key IS NULL
UNION ALL
SELECT 'orphan_location_keys', count(*),
       CASE WHEN count(*) = 0 THEN 'PASS' ELSE 'FAIL' END
FROM fact_job_posting f LEFT JOIN dim_location d USING (location_key)
WHERE d.location_key IS NULL
UNION ALL
SELECT 'invalid_timestamps', count(*),
       CASE WHEN count(*) = 0 THEN 'PASS' ELSE 'FAIL' END
FROM fact_job_posting
WHERE listed_at IS NULL OR listed_at < TIMESTAMP '2000-01-01' OR listed_at > TIMESTAMP '2100-01-01'
UNION ALL
SELECT 'invalid_salary_ranges', count(*),
       CASE WHEN count(*) = 0 THEN 'PASS' ELSE 'FAIL' END
FROM fact_job_posting
WHERE min_salary < 0 OR med_salary < 0 OR max_salary < 0 OR (min_salary > max_salary);
