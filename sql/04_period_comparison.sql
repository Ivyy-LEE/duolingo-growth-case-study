USE duolingo_growth_ops;

-- Diagnose whether engagement and monetisation are growing faster than audience scale.
SELECT
    quarter,
    ROUND(mau_yoy * 100, 1) AS mau_yoy_pct,
    ROUND(dau_yoy * 100, 1) AS dau_yoy_pct,
    ROUND(paid_subscribers_yoy * 100, 1) AS paid_subscribers_yoy_pct,
    ROUND(revenue_yoy * 100, 1) AS revenue_yoy_pct,
    ROUND((dau_yoy - mau_yoy) * 100, 1) AS engagement_growth_gap_pp,
    ROUND((paid_subscribers_yoy - mau_yoy) * 100, 1) AS paid_growth_gap_pp,
    ROUND((revenue_yoy - mau_yoy) * 100, 1) AS revenue_growth_gap_pp
FROM v_growth_metrics
WHERE mau_yoy IS NOT NULL
ORDER BY period_end;

-- Latest-quarter KPI card values.
SELECT
    quarter,
    mau_m,
    dau_m,
    ROUND(dau_mau_ratio * 100, 1) AS dau_mau_pct,
    paid_subscribers_m,
    revenue_usd_m,
    ROUND((dau_mau_ratio - LAG(dau_mau_ratio, 4) OVER (ORDER BY period_end)) * 100, 1) AS dau_mau_yoy_change_pp,
    ROUND(mau_yoy * 100, 1) AS mau_yoy_pct,
    ROUND(dau_yoy * 100, 1) AS dau_yoy_pct,
    ROUND(paid_subscribers_yoy * 100, 1) AS paid_yoy_pct,
    ROUND(revenue_yoy * 100, 1) AS revenue_yoy_pct
FROM v_growth_metrics
ORDER BY period_end DESC
LIMIT 1;
