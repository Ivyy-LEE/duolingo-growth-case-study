# Tableau Workbook Maintenance Guide

The final two-page Tableau dashboard is published: [Page 1](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P1_Growth_Monetisation_Overview?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) / [Page 2](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P2_Growth_Diagnostics_Strategic_Context?:showVizHome=no). Both pages' unauthenticated public PNG exports were retrieved on October 18, 2026; interactive browser tabs were not tested. The repository includes the [final native workbook](../dashboard/final/Duolingo_Growth_Marketing_Analytics.twbx), with URLs and verification scope in [the central link record](portfolio_links.json).

This guide preserves the workbook's data and calculation rules for maintenance. Use `dashboard/final/tableau_page1.png` and `dashboard/final/tableau_page2.png` as the final visual references. Earlier bilingual PNGs are legacy static prototypes. See [delivery status](../TABLEAU_HANDOFF.md).

## Data sources and relationships

- `data/processed/quarterly_dashboard.csv`: one row per quarter, sorted by `period_end`. Use this wide table for the cards and charts.
- `data/processed/tableau_quarterly_long.csv`: optional long-format alternative with 13 measures. `metric` contains mixed units, so filter to compatible measures before plotting. Do not join it to the wide table and sum duplicated quarterly values.
- `data/processed/competitor_web_snapshot.csv`: February 2026 observations, one row per brand.
- `data/processed/social_snapshot.csv`: March 2026 observations, one row per brand/platform.

Keep the three datasets separate. No user-level join or time-series relationship exists between corporate data and competitor snapshots. Keep the snapshot-month labels visible. The supplied competitor figures are historically unverified, and original captures are absent.

## Formats and calculation rules

- Treat `period_end` as a date, `quarter` as its display label and `source_id` as a trace key.
- MAU, DAU and paid subscribers use millions. Revenue uses USD millions.
- `dau_mau_ratio`, all QoQ/YoY fields and all growth-gap fields are fractions. Display rates with one decimal percent. Multiply growth gaps by 100 and label them **percentage points (pp)**.
- QoQ is unavailable for Q1 2023. YoY and growth gaps are unavailable for all four quarters of 2023. Preserve NULL values without zero replacement or invented earlier observations.
- `*_index` fields use Q1 2023 = 100. Do not format indices as percentages.
- Ratios and rates should use the quarter's single value (for example ATTR or MIN), not a sum across quarters. Do not sum audience counts across quarters or platform follower counts.

## Page 1 - Growth & Monetisation Overview

1. Use a 1600 × 900 fixed canvas and retain the completed dashboard layout.
2. Filter the KPI cards to **Q4 2025**: MAU 133.1M, DAU 52.7M, DAU/MAU 39.6%, paid subscribers 12.2M and quarterly revenue $282.9M. Keep the quarter label visible.
3. Cards show YoY rates of 14.1%, 30.1%, 28.4% and 35.0%. DAU/MAU shows **+4.9 pp YoY**, a difference between the Q4 2025 and Q4 2024 ratios.
4. Retain the completed MAU/DAU trend lines, DAU/MAU line, separate paid/revenue lines and four-measure YoY comparison.
5. Include Q4 2025 on the endpoint ticks. Retain the measured findings and the official-source/definition footer.

## Page 2 - Growth Diagnostics & Strategic Context

1. Retain the **Q4 2025 growth-gap cards**: DAU versus MAU **16.1 pp**, paid subscribers versus MAU **14.4 pp**, revenue versus MAU **20.9 pp**. Gaps are descriptive, not causal measures.
2. Retain **Indexed Growth Comparison**, with the four index measures over all 12 quarters.
3. Retain **Engagement Growth Gap**, using `dau_yoy_minus_mau_yoy * 100`.
4. Retain **Monetisation Growth Gaps**, using `paid_subscribers_yoy_minus_mau_yoy * 100` and `revenue_yoy_minus_mau_yoy * 100`. These add diagnostic context to the Page 1 rate trends.
5. Keep **Website Traffic** (February 2026) and **Social Audience** (March 2026) as separate contextual snapshots. Preserve the inherited-source limitation. Browsing metrics do not establish conversion or retention, and followers overlap across platforms.
6. Retain **Operational Priorities** with the exact approved headings: **Protect engagement quality; Strengthen premium value communication; Balance growth with user control**（保护活跃质量；强化会员价值沟通；兼顾增长与用户自主控制）. Investigate sustained engagement, test premium value messaging/trial opportunities and monitor user response to configurable settings. Keep proposals distinct from observed findings; public aggregates do not establish better conversion or reveal internal measurement coverage.

## Presentation and link maintenance

Both English and Chinese case studies use the same completed English Tableau visuals. Translate the surrounding narrative only; preserve every filter, unit, calculation and source qualification. A separate Chinese Tableau replica is not required for the current portfolio.

For future workbook changes, reconcile card values and chart marks against the CSVs, verify NULL behavior and fixed periods, inspect both pages visually, then save the `.twb`/`.twbx` and refresh the final image assets. Keep the analysis cutoff at March 2026.

If future changes alter either Tableau Public URL, update `docs/portfolio_links.json`, verify both pages and regenerate the case studies to refresh their links and visuals. Record the verification date and scope; the current check covers public PNG exports, not interactive browser tabs.
