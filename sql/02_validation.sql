USE duolingo_growth_ops;

-- Query 1: manual summary must be 12 rows and 12 distinct quarters.
SELECT COUNT(*) AS quarter_count, COUNT(DISTINCT quarter) AS distinct_quarter_count
FROM quarterly_performance;

-- Query 2: exact expected periods absent from the input; expected result: no rows.
WITH expected AS (
    SELECT '2023-Q1' AS quarter, 2023 AS fiscal_year, 1 AS quarter_num, '2023-03-31' AS period_end
    UNION ALL
    SELECT '2023-Q2', 2023, 2, '2023-06-30'
    UNION ALL
    SELECT '2023-Q3', 2023, 3, '2023-09-30'
    UNION ALL
    SELECT '2023-Q4', 2023, 4, '2023-12-31'
    UNION ALL
    SELECT '2024-Q1', 2024, 1, '2024-03-31'
    UNION ALL
    SELECT '2024-Q2', 2024, 2, '2024-06-30'
    UNION ALL
    SELECT '2024-Q3', 2024, 3, '2024-09-30'
    UNION ALL
    SELECT '2024-Q4', 2024, 4, '2024-12-31'
    UNION ALL
    SELECT '2025-Q1', 2025, 1, '2025-03-31'
    UNION ALL
    SELECT '2025-Q2', 2025, 2, '2025-06-30'
    UNION ALL
    SELECT '2025-Q3', 2025, 3, '2025-09-30'
    UNION ALL
    SELECT '2025-Q4', 2025, 4, '2025-12-31'
)
SELECT expected.quarter AS missing_quarter
FROM expected LEFT JOIN quarterly_performance actual ON actual.quarter = expected.quarter
WHERE actual.quarter IS NULL;

-- Query 3: out-of-scope labels or inconsistent fiscal metadata/dates; no rows.
WITH expected AS (
    SELECT '2023-Q1' AS quarter, 2023 AS fiscal_year, 1 AS quarter_num, '2023-03-31' AS period_end
    UNION ALL
    SELECT '2023-Q2', 2023, 2, '2023-06-30'
    UNION ALL
    SELECT '2023-Q3', 2023, 3, '2023-09-30'
    UNION ALL
    SELECT '2023-Q4', 2023, 4, '2023-12-31'
    UNION ALL
    SELECT '2024-Q1', 2024, 1, '2024-03-31'
    UNION ALL
    SELECT '2024-Q2', 2024, 2, '2024-06-30'
    UNION ALL
    SELECT '2024-Q3', 2024, 3, '2024-09-30'
    UNION ALL
    SELECT '2024-Q4', 2024, 4, '2024-12-31'
    UNION ALL
    SELECT '2025-Q1', 2025, 1, '2025-03-31'
    UNION ALL
    SELECT '2025-Q2', 2025, 2, '2025-06-30'
    UNION ALL
    SELECT '2025-Q3', 2025, 3, '2025-09-30'
    UNION ALL
    SELECT '2025-Q4', 2025, 4, '2025-12-31'
)
SELECT actual.*
FROM quarterly_performance actual LEFT JOIN expected ON actual.quarter = expected.quarter
WHERE expected.quarter IS NULL
   OR actual.fiscal_year <> expected.fiscal_year
   OR actual.quarter_num <> expected.quarter_num
   OR actual.period_end <> expected.period_end;

-- Query 4: duplicate fiscal quarter combinations; expected result: no rows.
SELECT fiscal_year, quarter_num, COUNT(*) AS row_count
FROM quarterly_performance
GROUP BY fiscal_year, quarter_num
HAVING COUNT(*) <> 1;

-- Query 5: core metric constraints, including NULLs; expected result: no rows.
SELECT * FROM quarterly_performance
WHERE mau_m IS NULL OR dau_m IS NULL OR paid_subscribers_m IS NULL OR revenue_usd_m IS NULL
   OR mau_m <= 0 OR dau_m <= 0 OR dau_m > mau_m
   OR paid_subscribers_m <= 0 OR revenue_usd_m <= 0
   OR total_bookings_usd_m <= 0 OR subscription_bookings_usd_m <= 0
   OR subscription_bookings_usd_m > total_bookings_usd_m
   OR CAST(dau_m AS DOUBLE) / NULLIF(mau_m, 0) NOT BETWEEN 0 AND 1;
