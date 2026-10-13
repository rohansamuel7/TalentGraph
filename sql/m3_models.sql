CREATE OR REPLACE TABLE dim_company AS
SELECT
    md5('company|' || coalesce(source_company_id, 'unknown')) AS company_key,
    source_company_id,
    min(company_name) AS company_name,
    count(*)::BIGINT AS posting_count
FROM read_parquet('{{INPUT_PARQUET}}')
GROUP BY source_company_id;

CREATE OR REPLACE TABLE dim_location AS
SELECT
    md5('location|' || coalesce(location, 'unknown')) AS location_key,
    coalesce(location, 'unknown') AS location_name,
    count(*)::BIGINT AS posting_count
FROM read_parquet('{{INPUT_PARQUET}}')
GROUP BY coalesce(location, 'unknown');

CREATE OR REPLACE TABLE fact_job_posting AS
SELECT
    p.job_key,
    p.source_job_id,
    c.company_key,
    l.location_key,
    p.title,
    p.company_name,
    p.location,
    p.work_type,
    p.experience_level,
    p.listed_at,
    p.original_listed_at,
    p.expires_at,
    p.closed_at,
    p.remote_allowed,
    p.min_salary,
    p.med_salary,
    p.max_salary,
    p.currency,
    p.pay_period,
    p.compensation_type,
    p.source_file,
    p.source_row_number,
    p.ingestion_run_id,
    p.retrieved_at_utc,
    p.raw_record_hash
FROM read_parquet('{{INPUT_PARQUET}}') p
JOIN dim_company c ON c.source_company_id IS NOT DISTINCT FROM p.source_company_id
JOIN dim_location l ON l.location_name IS NOT DISTINCT FROM coalesce(p.location, 'unknown');

CREATE OR REPLACE VIEW vw_job_counts_by_company_location_period AS
SELECT
    company_key,
    location_key,
    date_trunc('month', listed_at)::DATE AS posting_month,
    count(*)::BIGINT AS job_count
FROM fact_job_posting
GROUP BY company_key, location_key, date_trunc('month', listed_at)::DATE;

CREATE OR REPLACE VIEW vw_salary_analysis AS
SELECT
    job_key,
    company_key,
    location_key,
    currency,
    pay_period,
    min_salary,
    med_salary,
    max_salary,
    coalesce(med_salary, (min_salary + max_salary) / 2, min_salary, max_salary) AS representative_salary,
    listed_at
FROM fact_job_posting
WHERE coalesce(min_salary, med_salary, max_salary) IS NOT NULL
  AND coalesce(min_salary, med_salary, max_salary) >= 0
  AND (min_salary IS NULL OR max_salary IS NULL OR min_salary <= max_salary);
