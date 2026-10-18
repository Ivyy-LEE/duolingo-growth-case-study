USE duolingo_growth_ops;

-- Tableau-ready quarterly view.
CREATE OR REPLACE VIEW v_dashboard_quarterly AS
SELECT
    quarter,
    fiscal_year,
    quarter_num,
    period_end,
    source_id,
    mau_m,
    dau_m,
    dau_mau_ratio,
    paid_subscribers_m,
    revenue_usd_m,
    mau_qoq,
    dau_qoq,
    paid_subscribers_qoq,
    revenue_qoq,
    mau_yoy,
    dau_yoy,
    paid_subscribers_yoy,
    revenue_yoy,
    mau_index,
    dau_index,
    paid_subscribers_index,
    revenue_index,
    dau_yoy - mau_yoy AS dau_yoy_minus_mau_yoy,
    paid_subscribers_yoy - mau_yoy AS paid_subscribers_yoy_minus_mau_yoy,
    revenue_yoy - mau_yoy AS revenue_yoy_minus_mau_yoy
FROM v_growth_metrics;

-- Competitive snapshots remain point-in-time context, not longitudinal trends.
CREATE OR REPLACE VIEW v_dashboard_web_competition AS
SELECT * FROM competitor_web_snapshot;

CREATE OR REPLACE VIEW v_dashboard_social_competition AS
SELECT * FROM social_snapshot;
