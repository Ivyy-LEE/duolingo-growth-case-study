# Data Dictionary

Analysis as of **March 2026**. Corporate performance covers **Q1 2023–Q4 2025** only. Competitive observations are the inherited **February 2026 website** and **March 2026 social** snapshots. English and Chinese outputs use the same data.

## Corporate raw data: `data/raw/quarterly_performance.csv`

One row per quarter; 12 rows. `quarter` is the unique key. All six quantitative business fields come from official Duolingo IR/SEC disclosures. The source manifest provides the document for each row.

| Field | Definition | Stored unit / type | Timing and interpretation |
|---|---|---|---|
| `quarter` | Fiscal quarter label | Text, `YYYY-Qn` | Exact sequence 2023-Q1 through 2025-Q4 |
| `fiscal_year` | Fiscal year | Integer | 2023, 2024 or 2025 |
| `quarter_num` | Quarter number | Integer | 1–4; agrees with `quarter` |
| `period_end` | Calendar quarter end | ISO date | March 31, June 30, September 30 or December 31 |
| `mau_m` | Monthly active users | Millions of users | Average of monthly unique active-user counts over the quarter; not quarter-end users |
| `dau_m` | Daily active users | Millions of users | Average of daily unique active-user counts over the quarter; not quarter-end users |
| `paid_subscribers_m` | Active paid subscribers | Millions of paid user accounts | At period end; each unique account counts once, excluding free trials and non-paying family-plan members |
| `revenue_usd_m` | GAAP total revenue | USD millions | Revenue recognised during the quarter; not subscription revenue alone |
| `total_bookings_usd_m` | Total bookings | USD millions | Quarterly amounts from subscriptions, advertising networks, Duolingo English Test and in-app purchases, under company definitions |
| `subscription_bookings_usd_m` | Subscription bookings | USD millions | Quarterly amounts received from subscription purchases; distinct from revenue recognised over subscription terms |
| `source_id` | Primary disclosure trace key | Text | Joins to `docs/source_manifest.csv`; source IDs are preserved even where document URLs have been corrected |

MAU/DAU are company estimates from its internal analytics system, with potential methodology changes and no independent third-party validation. Other companies can define active users differently.

Financial values for **2023-Q1–2024-Q3** retain the source's USD-thousand precision after division by 1,000 (three decimals in USD millions). Values for **2024-Q4–2025-Q4** retain the shareholder letters' one-decimal-million precision. User counts retain one-decimal-million precision. The project does not invent additional precision. Growth calculated from these disclosed rounded inputs can differ slightly from company percentages calculated using underlying unrounded figures.

Dashboard cards generally display one decimal, while narrative growth figures use whole percentages. Full calculated precision remains in the CSVs. The notebook diagnostic table uses explicit Decimal half-up rounding to match the verified SQLite comparison display: for example, Q2 2025 paid-subscriber growth is 36.25%, displayed as 36.3%. Python's default half-even rounding can display 36.2% for the same value. Reconciliation compares the underlying values before display rounding. Native MySQL rounding has not been verified.

## Quarterly processed data: `data/processed/quarterly_dashboard.csv`

The file preserves all 11 raw fields above and adds the 16 fields below. Rows remain keyed by `quarter`. For formulas, `x[t]` is the current quarter; `x[t-1]` is the previous quarter; `x[t-4]` is the same quarter a year earlier; `x[0]` is 2023-Q1. Growth rates are stored as decimal fractions: `0.14` means 14%. A growth-rate difference of `0.16` means **16 percentage points**, not 16% relative growth.

| Derived field | Formula | Stored unit | Missing values |
|---|---|---|---|
| `dau_mau_ratio` | `dau_m / mau_m` | Decimal ratio; display as percent | None in this dataset |
| `mau_qoq` | `mau_m[t] / mau_m[t-1] - 1` | Decimal growth rate | Blank in 2023-Q1 |
| `mau_yoy` | `mau_m[t] / mau_m[t-4] - 1` | Decimal growth rate | Blank in all four 2023 quarters |
| `mau_index` | `mau_m[t] / mau_m[0] * 100` | Index points, 2023-Q1 = 100 | None |
| `dau_qoq` | `dau_m[t] / dau_m[t-1] - 1` | Decimal growth rate | Blank in 2023-Q1 |
| `dau_yoy` | `dau_m[t] / dau_m[t-4] - 1` | Decimal growth rate | Blank in all four 2023 quarters |
| `dau_index` | `dau_m[t] / dau_m[0] * 100` | Index points, 2023-Q1 = 100 | None |
| `paid_subscribers_qoq` | `paid_subscribers_m[t] / paid_subscribers_m[t-1] - 1` | Decimal growth rate | Blank in 2023-Q1 |
| `paid_subscribers_yoy` | `paid_subscribers_m[t] / paid_subscribers_m[t-4] - 1` | Decimal growth rate | Blank in all four 2023 quarters |
| `paid_subscribers_index` | `paid_subscribers_m[t] / paid_subscribers_m[0] * 100` | Index points, 2023-Q1 = 100 | None |
| `revenue_qoq` | `revenue_usd_m[t] / revenue_usd_m[t-1] - 1` | Decimal growth rate | Blank in 2023-Q1 |
| `revenue_yoy` | `revenue_usd_m[t] / revenue_usd_m[t-4] - 1` | Decimal growth rate | Blank in all four 2023 quarters |
| `revenue_index` | `revenue_usd_m[t] / revenue_usd_m[0] * 100` | Index points, 2023-Q1 = 100 | None |
| `dau_yoy_minus_mau_yoy` | `dau_yoy - mau_yoy` | Decimal rate difference; multiply by 100 for pp | Blank in all four 2023 quarters |
| `paid_subscribers_yoy_minus_mau_yoy` | `paid_subscribers_yoy - mau_yoy` | Decimal rate difference; multiply by 100 for pp | Blank in all four 2023 quarters |
| `revenue_yoy_minus_mau_yoy` | `revenue_yoy - mau_yoy` | Decimal rate difference; multiply by 100 for pp | Blank in all four 2023 quarters |

CSV blanks represent unavailable comparisons, corresponding to pandas missing values and SQL `NULL`; they must not be filled with zero. Prior periods outside the analysis window are deliberately not imported. SQL division uses `NULLIF` to return `NULL` for a zero denominator; current denominators are all positive.

`dau_mau_ratio` is the **ratio of separately averaged quarterly DAU and MAU counts**. It is an aggregate engagement-intensity proxy. It is not cohort retention, a user's probability of daily activity, or the average of individual daily DAU/MAU ratios. Paid accounts are period-end counts while MAU is a period average; this project does not call their ratio a measured free-to-paid conversion rate. Growth gaps identify divergences for investigation, not causal effects or evidence of pricing efficiency.

## Tableau long data: `data/processed/tableau_quarterly_long.csv`

156 rows: 12 quarters × 13 selected metrics. The unique key is (`quarter`, `metric`). No new observations or calculations are introduced by reshaping.

| Field | Definition | Stored type |
|---|---|---|
| `quarter` | Quarter label from quarterly data | Text |
| `period_end` | Matching quarter-end date | ISO date |
| `metric` | One of the 13 labels below | Text |
| `value` | Value from the mapped quarterly field | Numeric; unit depends on `metric`; preserves blanks |

| `metric` label | Quarterly field | Unit / display |
|---|---|---|
| `MAU (M)` | `mau_m` | Millions of users |
| `DAU (M)` | `dau_m` | Millions of users |
| `DAU/MAU` | `dau_mau_ratio` | Decimal ratio; percent |
| `Paid Subscribers (M)` | `paid_subscribers_m` | Millions of paid accounts |
| `Revenue (USD M)` | `revenue_usd_m` | USD millions |
| `MAU YoY` | `mau_yoy` | Decimal growth rate; percent |
| `DAU YoY` | `dau_yoy` | Decimal growth rate; percent |
| `Paid Subscribers YoY` | `paid_subscribers_yoy` | Decimal growth rate; percent |
| `Revenue YoY` | `revenue_yoy` | Decimal growth rate; percent |
| `MAU Index` | `mau_index` | Index points |
| `DAU Index` | `dau_index` | Index points |
| `Paid Subscribers Index` | `paid_subscribers_index` | Index points |
| `Revenue Index` | `revenue_index` | Index points |

The value column mixes units, so charts must filter/group by metric and apply the matching format. Summing values across metric labels is meaningless. QoQ, bookings and growth gaps remain available in the quarterly CSV; they are not included in this existing 13-metric long file.

## Website snapshot: `data/raw/competitor_web_snapshot.csv`

The processed file of the same name preserves the raw snapshot. Three rows, keyed by (`brand`, `snapshot_month`). Historical provenance is **unverified**: original coursework/provider captures and exact observation dates are absent from this folder. Values are retained as supplied contextual observations, not independently authenticated historical facts.

| Field | Definition | Stored unit / type |
|---|---|---|
| `brand` | Duolingo, Babbel or Busuu | Text |
| `snapshot_month` | Inherited website observation month | Text, `2026-02` |
| `total_visits_m` | Estimated monthly website visits | Millions of visits; not unique people or app MAU |
| `bounce_rate_pct` | Provider's estimated bounce rate | Percent on a 0–100 scale; `31.71` means 31.71% |
| `pages_per_visit` | Estimated pages per website visit | Pages per visit |
| `avg_visit_duration_sec` | Estimated average website visit duration | Seconds |
| `source_id` | Shared historical source trace key | Text, `COMP_WEB_2026_02` |

These estimates describe the three websites at one point in time. Different product/site flows can affect browsing metrics. More pages per visit or longer duration does not establish better learning, app engagement, conversion or retention. The three-brand visits total is not a market denominator; no market-share or longitudinal competitor claim is supported. The manifest's Similarweb link identifies a provider page, not evidence of an archived February capture.

## Social snapshot: `data/raw/social_snapshot.csv`

The processed file of the same name preserves the raw snapshot. Nine rows, keyed by (`brand`, `platform`, `snapshot_month`). Historical provenance is **unverified**: original account captures, exact account URLs and observation dates are absent.

| Field | Definition | Stored unit / type |
|---|---|---|
| `brand` | Duolingo, Babbel or Busuu | Text |
| `platform` | TikTok, YouTube or Instagram | Text |
| `followers` | Inherited platform audience count; YouTube subscribers are stored under the common field name | Count of platform follows/subscriptions, integer |
| `snapshot_month` | Inherited social observation month | Text, `2026-03` |
| `source_id` | Shared historical source trace key | Text, `COMP_SOCIAL_2026_03` |

Audiences overlap across platforms and can include inactive accounts; **do not sum followers across platforms**. Follower counts do not measure unique reach, engagement, app acquisition, paid conversion or campaign performance. No synthetic social time series is generated.

## Source manifest: `docs/source_manifest.csv`

| Field | Definition |
|---|---|
| `source_id` | Unique document/provenance key; referenced by raw data where applicable |
| `dataset` | Dataset supported by the source |
| `period` | Corporate quarter or inherited snapshot month; not necessarily publication date |
| `source_name` | Descriptive document or snapshot name |
| `source_type` | Official IR/SEC source or explicitly unverified inherited snapshot |
| `publication_date` | Known official publication date in ISO format; blank for historical competitor sources with unestablished dates |
| `original_url` | Verified official document link or explicitly limited provider reference; blank when the exact source URL is unknown |
| `metrics_covered` | Supported metric names or supplemental definitions |
| `access_context` | How the source is used and any verification limitations |
| `notes` | Units, precision, derivation and provenance caveats |

`DUOL_2025_10K_SEC` is supplemental definition/ratio evidence published on February 27, 2026. It adds no raw-data quarter and does not replace the Q4 2025 shareholder-letter source key.
