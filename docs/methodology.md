# Methodology

## Fixed analytical scope

- Analysis as of: **March 2026**.
- Corporate performance: **Q1 2023–Q4 2025**, 12 complete quarters.
- Competitive website context: inherited **February 2026** snapshot.
- Competitive social context: inherited **March 2026** snapshot.

The continuation audit was performed on **October 14, 2026** using historical official documents published before the March 2026 analysis cutoff. The review date does not move the analysis date. Later operating results and current competitor values are excluded.

## Business questions and evidence

The case study examines whether audience growth coincided with deeper aggregate daily activity and larger paid-subscriber/revenue bases, then identifies operational questions for a growth team. It does not reconstruct Duolingo's internal funnel or assess campaign effectiveness.

The primary evidence is six company-reported metrics per quarter: average MAU, average DAU, period-end paid subscribers, quarterly GAAP revenue, total bookings and subscription bookings. Every raw corporate value must trace to official Investor Relations or SEC material through `source_id`. The historical competitor values provide limited context and have weaker provenance; they are not used to establish Duolingo's operating performance.

An inherited RACE/coursework narrative is motivation for the project, not independently established evidence. The original coursework and competitor captures are absent. Descriptive findings here depend on the inspected public data, not on unprovided prior summaries.

## Source verification

The October 2026 continuation audit independently matched **all 72 corporate metric cells** (12 quarters × six metrics) to official historical numerical disclosures. No raw corporate values needed replacement. See `source_manifest.csv` for document URLs and publication dates.

| Corporate periods | Numerical disclosure used | Precision retained |
|---|---|---|
| 2023-Q1, Q2, Q3, Q4 | Original official quarterly releases: `DUOL_2023_Q1_IR` through `DUOL_2023_Q4_IR` | User counts in millions; financial USD thousands divided by 1,000 |
| 2024-Q1, Q2, Q3 | Original official quarterly releases: `DUOL_2024_Q1_IR` through `DUOL_2024_Q3_IR` | User counts in millions; financial USD thousands divided by 1,000 |
| 2024-Q4 | Original Q4/FY2024 shareholder letter: `DUOL_2024_Q4_IR` | Disclosed one-decimal millions |
| 2025-Q1 | Original Q1 2025 shareholder letter: `DUOL_2025_Q1_IR` | Disclosed one-decimal millions |
| 2025-Q2 | Original Q2 2025 shareholder letter: `DUOL_2025_Q2_IR` | Disclosed one-decimal millions |
| 2025-Q3 | Original Q3 2025 shareholder letter: `DUOL_2025_Q3_IR` | Disclosed one-decimal millions |
| 2025-Q4 | Original Q4/FY2025 shareholder letter: `DUOL_2025_Q4_SEC` | Disclosed one-decimal millions |

The Q4 2025 DAU/MAU ratio is calculated as `52.7 / 133.1 = 39.594…%`, displayed as **39.6%**. The supplemental original [2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1562088/000162828026012494/duol-20251231.htm), published February 27, 2026, explicitly reports 39.6% and provides metric definitions. It adds no quarter or business metric to the dataset. Four announcement-only manifest links were corrected to the numerical shareholder letters.

The company explains that its published growth percentages can use underlying unrounded figures. This project transparently derives rates from the disclosed values stored in its CSVs, so minor differences from rounded official rates are expected and are not evidence of a data error.

## Data preparation and calculations

1. Preserve the three canonical raw CSVs and source manifest. The builder reads these existing inputs; it does not recreate or overwrite raw values.
2. Require the exact 12-quarter sequence, consistent fiscal metadata and actual quarter-end dates. Require positive core values, DAU no greater than MAU, and subscription bookings no greater than total bookings.
3. Calculate DAU/MAU, QoQ, YoY, four growth indexes (2023-Q1 = 100) and three YoY growth-rate gaps in Python for the processed quarterly CSV.
4. Preserve unavailable prior-period comparisons as missing values. QoQ is missing in 2023-Q1; YoY and growth gaps are missing in all four 2023 quarters. No observations before 2023-Q1 are fabricated or imported.
5. Reshape 13 selected metrics into the existing 156-row Tableau long CSV, retaining quarter keys, dates, numeric values and missing-value masks.
6. Copy the historical competitor snapshots into processed inputs without changing their values or months. Validate three unique web rows and nine unique brand/platform social rows.

Full formulas, units and field definitions are in `data_dictionary.md`. Rate differences are reported in **percentage points**; ratios and growth rates are reported in percent; indexes are index points. Period growth compares the two endpoint quarters, not annual totals.

## Independent reconciliation and SQL scope

The processed values are independently recalculated from raw CSV strings using Python's Decimal arithmetic, joined by `quarter`, and reconciled across **all 16 derived fields and their missing-value masks**. Floating-point exports are compared within a small numerical tolerance, not for literal decimal-string identity. Raw fields and the long-format key/date/value mapping are also checked.

The supplied SQL is intended for MySQL 8. It independently expresses the same quarterly formulas using `LAG`, `FIRST_VALUE` and analytical views. During this continuation, the actual schema, seed and view scripts are also executed against an in-memory **SQLite compatibility adaptation**, then their results are reconciled with the Python data. The adaptation removes MySQL database-selection statements, changes `CREATE OR REPLACE VIEW` to `CREATE VIEW`, and changes `CAST(... AS DOUBLE)` to a real-number cast. SQLite accepts the declared string/decimal types but does not reproduce MySQL's precision, coercion and constraint behavior.

Verification includes seeded raw values, all derived fields and NULL masks, SQL validation outputs, and the latest-quarter comparison. **Native MySQL execution is not verified.** This check demonstrates formula/result agreement through the disclosed adaptation; it does not certify MySQL deployment compatibility. See the executed notebook and final QA report for run evidence.

## Interpretation and operational use

- DAU/MAU is a ratio of separately averaged period counts and an aggregate engagement-intensity proxy; it is not cohort retention or an individual user's daily-use probability.
- Period-end paid subscribers and quarterly revenue do not constitute a measured free-to-paid funnel. Revenue growth combines multiple sources and timing effects; it cannot isolate subscription conversion, pricing, packaging, willingness to pay or commercial efficiency.
- Faster DAU/paid/revenue growth than MAU is an observed divergence. It suggests questions for operational review, not a proven causal mechanism.
- Proposed operational priorities require authorised internal evidence: review existing measurement, inspect cohort/renewal and conversion behavior where available, and evaluate possible actions against free-experience and learning guardrails. The portfolio's lack of access does not establish that Duolingo lacks instrumentation.
- As-of-cutoff management commentary can supply context when attributed to an official source. The [Q4/FY2025 shareholder letter](https://www.sec.gov/Archives/edgar/data/1562088/000162828026012246/q4fy25duolingo12-31x25shar.htm) describes prioritising teaching/user growth and reducing monetisation friction. This is a disclosed management direction, not a causal conclusion inferred from the quarterly metrics; forward forecasts are excluded from this case study.

## Competitive and delivery limitations

The inherited website/social observations remain point-in-time contextual snapshots. Original captures, exact observation dates and exact social account URLs are unavailable, so their historical provenance is explicitly **unverified**. The known months are preserved; unsupported exact dates are removed. Current provider pages cannot authenticate historical values and must not be used to replace the snapshots. The websites are not the apps; browsing metrics do not establish learning quality or conversion. Social audiences overlap, so followers are not summed across platforms. No market-share estimate or longitudinal competitor dataset is constructed.

The final presentation uses the completed and published two-page English Tableau dashboard and `dashboard/final/Duolingo_Growth_Marketing_Analytics.twbx`. Page 2 retains Q4 2025 growth-gap cards, Indexed Growth Comparison, Engagement Growth Gap, Monetisation Growth Gaps, separate Website Traffic and Social Audience contextual snapshots, and Operational Priorities. The approved priority headings are Protect engagement quality; Strengthen premium value communication; Balance growth with user control. Tableau Public URLs, including the exact supplied Share URL, are recorded in `docs/portfolio_links.json`. Both pages' public PNG exports were retrieved without authentication on October 18, 2026; interactive browser tabs were not tested. Final dashboard images are kept in `dashboard/final/`; earlier bilingual static images are legacy prototypes retained for reference. English and Chinese case-study deliverables share the same final visuals, observations, calculations, conclusions and analytical limits. Exported pages must be visually inspected after regeneration, as numerical reconciliation alone does not establish visual QA. This presentation update does not change the March 2026 analysis cutoff or the frozen data definitions.
