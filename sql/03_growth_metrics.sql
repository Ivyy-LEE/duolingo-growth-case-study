USE duolingo_growth_ops;

-- Build growth KPIs once so Tableau can consume a clean analytical view.
CREATE OR REPLACE VIEW v_growth_metrics AS
WITH base AS (
    SELECT
        quarter,
        fiscal_year,
        quarter_num,
        period_end,
        mau_m,
        dau_m,
        paid_subscribers_m,
        revenue_usd_m,
        total_bookings_usd_m,
        subscription_bookings_usd_m,
        source_id,
        CAST(dau_m AS DOUBLE) / NULLIF(mau_m, 0) AS dau_mau_ratio,
        LAG(mau_m, 1) OVER (ORDER BY period_end) AS prev_q_mau,
        LAG(dau_m, 1) OVER (ORDER BY period_end) AS prev_q_dau,
        LAG(paid_subscribers_m, 1) OVER (ORDER BY period_end) AS prev_q_paid,
        LAG(revenue_usd_m, 1) OVER (ORDER BY period_end) AS prev_q_revenue,
        LAG(mau_m, 4) OVER (ORDER BY period_end) AS prev_y_mau,
        LAG(dau_m, 4) OVER (ORDER BY period_end) AS prev_y_dau,
        LAG(paid_subscribers_m, 4) OVER (ORDER BY period_end) AS prev_y_paid,
        LAG(revenue_usd_m, 4) OVER (ORDER BY period_end) AS prev_y_revenue,
        FIRST_VALUE(mau_m) OVER (ORDER BY period_end) AS base_mau,
        FIRST_VALUE(dau_m) OVER (ORDER BY period_end) AS base_dau,
        FIRST_VALUE(paid_subscribers_m) OVER (ORDER BY period_end) AS base_paid,
        FIRST_VALUE(revenue_usd_m) OVER (ORDER BY period_end) AS base_revenue
    FROM quarterly_performance
)
SELECT
    *,
    CAST(mau_m AS DOUBLE) / NULLIF(prev_q_mau,0) - 1 AS mau_qoq,
    CAST(dau_m AS DOUBLE) / NULLIF(prev_q_dau,0) - 1 AS dau_qoq,
    CAST(paid_subscribers_m AS DOUBLE) / NULLIF(prev_q_paid,0) - 1 AS paid_subscribers_qoq,
    CAST(revenue_usd_m AS DOUBLE) / NULLIF(prev_q_revenue,0) - 1 AS revenue_qoq,
    CAST(mau_m AS DOUBLE) / NULLIF(prev_y_mau,0) - 1 AS mau_yoy,
    CAST(dau_m AS DOUBLE) / NULLIF(prev_y_dau,0) - 1 AS dau_yoy,
    CAST(paid_subscribers_m AS DOUBLE) / NULLIF(prev_y_paid,0) - 1 AS paid_subscribers_yoy,
    CAST(revenue_usd_m AS DOUBLE) / NULLIF(prev_y_revenue,0) - 1 AS revenue_yoy,
    CAST(mau_m AS DOUBLE) / NULLIF(base_mau,0) * 100 AS mau_index,
    CAST(dau_m AS DOUBLE) / NULLIF(base_dau,0) * 100 AS dau_index,
    CAST(paid_subscribers_m AS DOUBLE) / NULLIF(base_paid,0) * 100 AS paid_subscribers_index,
    CAST(revenue_usd_m AS DOUBLE) / NULLIF(base_revenue,0) * 100 AS revenue_index
FROM base;
