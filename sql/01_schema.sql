-- MySQL 8+ schema for Duolingo Growth & Marketing Operations Analytics
CREATE DATABASE IF NOT EXISTS duolingo_growth_ops;
USE duolingo_growth_ops;

CREATE TABLE IF NOT EXISTS quarterly_performance (
    quarter VARCHAR(7) PRIMARY KEY,
    fiscal_year INT NOT NULL,
    quarter_num TINYINT NOT NULL,
    period_end DATE NOT NULL,
    mau_m DECIMAL(10,3) NOT NULL,
    dau_m DECIMAL(10,3) NOT NULL,
    paid_subscribers_m DECIMAL(10,3) NOT NULL,
    revenue_usd_m DECIMAL(12,3) NOT NULL,
    total_bookings_usd_m DECIMAL(12,3) NULL,
    subscription_bookings_usd_m DECIMAL(12,3) NULL,
    source_id VARCHAR(64) NOT NULL,
    UNIQUE (fiscal_year, quarter_num),
    UNIQUE (period_end),
    CHECK (fiscal_year BETWEEN 2023 AND 2025),
    CHECK (quarter_num BETWEEN 1 AND 4),
    CHECK (mau_m > 0 AND dau_m > 0 AND dau_m <= mau_m),
    CHECK (paid_subscribers_m > 0 AND revenue_usd_m > 0),
    CHECK (total_bookings_usd_m > 0),
    CHECK (subscription_bookings_usd_m > 0 AND subscription_bookings_usd_m <= total_bookings_usd_m)
);

CREATE TABLE IF NOT EXISTS competitor_web_snapshot (
    brand VARCHAR(32) PRIMARY KEY,
    snapshot_month CHAR(7) NOT NULL,
    total_visits_m DECIMAL(10,3),
    bounce_rate_pct DECIMAL(6,2),
    pages_per_visit DECIMAL(8,2),
    avg_visit_duration_sec INT,
    source_id VARCHAR(64) NOT NULL,
    CHECK (snapshot_month = '2026-02'),
    CHECK (total_visits_m > 0),
    CHECK (bounce_rate_pct BETWEEN 0 AND 100),
    CHECK (pages_per_visit > 0 AND avg_visit_duration_sec > 0)
);

CREATE TABLE IF NOT EXISTS social_snapshot (
    brand VARCHAR(32) NOT NULL,
    platform VARCHAR(32) NOT NULL,
    followers BIGINT NOT NULL,
    snapshot_month CHAR(7) NOT NULL,
    source_id VARCHAR(64) NOT NULL,
    PRIMARY KEY (brand, platform),
    CHECK (snapshot_month = '2026-03'),
    CHECK (followers > 0)
);
