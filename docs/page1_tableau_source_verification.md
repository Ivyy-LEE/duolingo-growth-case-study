# English Page 1 — CSV source verification

Verified October 14, 2026 against `data/processed/quarterly_dashboard.csv`, the data dictionary and methodology. This is **source-only verification**; it does not certify a Tableau worksheet, dashboard, workbook or publication. Analysis remains as of March 2026.

## Structure and field types

- Exactly 12 rows and 12 unique quarters, ordered from `2023-Q1` through `2025-Q4` without omissions.
- `period_end`: Date, actual quarter ends from `2023-03-31` through `2025-12-31`.
- `quarter`: String; use it for the quarter label and preserve chronological ordering.
- `mau_m`, `dau_m`, `paid_subscribers_m`, `revenue_usd_m`: decimal numeric measures, already stored in millions. Do not divide them by a million again.
- `dau_mau_ratio`, `mau_yoy`, `dau_yoy`, `paid_subscribers_yoy`, `revenue_yoy`: numeric fractions; display with one decimal percent.
- A quarter contains one observation, so MIN or ATTR can preserve its value. Never total audience counts or rates across quarters.

## Q4 2025 KPI cards and annotations

Only the five KPI worksheets should filter `quarter` to `2025-Q4`.

| Card | Exact CSV field | Q4 2025 source value | Card display | YoY field or calculation | Annotation |
|---|---|---:|---:|---|---:|
| MAU | `mau_m` | 133.1 | 133.1M | `mau_yoy` = 0.14053127677806332 | +14.1% |
| DAU | `dau_m` | 52.7 | 52.7M | `dau_yoy` = 0.3012345679012347 | +30.1% |
| DAU/MAU | `dau_mau_ratio` | 0.3959429000751315 | 39.6% | (Q4 2025 ratio − Q4 2024 ratio) × 100 = 4.889919827564565 | +4.9 pp |
| Paid Subscribers | `paid_subscribers_m` | 12.2 | 12.2M | `paid_subscribers_yoy` = 0.28421052631578947 | +28.4% |
| Quarterly Revenue | `revenue_usd_m` | 282.9 | $282.9M | `revenue_yoy` = 0.3497137404580153 | +35.0% |

The DAU/MAU comparison uses the Q4 2024 ratio `0.34704370179948585` (34.7%). There is no DAU/MAU YoY-change field in the CSV. `dau_yoy_minus_mau_yoy` is a different diagnostic: the gap between DAU and MAU growth rates, equal to 16.1 pp in Q4 2025. It must not be used for the +4.9 pp card annotation.

## Trend endpoints

All trend worksheets must retain the full 12-quarter source domain. Each of the five level/ratio series contains 12 non-NULL observations.

| Chart / series | Field | First quarter | Exact first value | Last quarter | Exact last value | Display units |
|---|---|---|---:|---|---:|---|
| MAU & DAU / MAU | `mau_m` | 2023-Q1 | 72.6 | 2025-Q4 | 133.1 | Millions of users |
| MAU & DAU / DAU | `dau_m` | 2023-Q1 | 20.3 | 2025-Q4 | 52.7 | Millions of users |
| DAU/MAU | `dau_mau_ratio` | 2023-Q1 | 0.2796143250688706 | 2025-Q4 | 0.3959429000751315 | 28.0% → 39.6% |
| Paid Subscribers | `paid_subscribers_m` | 2023-Q1 | 4.8 | 2025-Q4 | 12.2 | Millions of paid accounts |
| Quarterly Revenue | `revenue_usd_m` | 2023-Q1 | 115.661 | 2025-Q4 | 282.9 | USD millions; one-decimal display 115.7 → 282.9 |

## Four-measure YoY comparison endpoints

Each series has four NULLs in 2023 and eight available values from 2024-Q1 through 2025-Q4. Retain all 12 quarter labels/domain; leave 2023 comparisons unavailable. No 2023 zero-valued growth marks should appear.

| Series | Exact CSV field | First non-NULL quarter | Exact first fraction | First display | Q4 2025 fraction | Last display |
|---|---|---|---:|---:|---:|---:|
| MAU YoY | `mau_yoy` | 2024-Q1 | 0.34435261707988984 | 34.4% | 0.14053127677806332 | 14.1% |
| DAU YoY | `dau_yoy` | 2024-Q1 | 0.5467980295566501 | 54.7% | 0.3012345679012347 | 30.1% |
| Paid Subscribers YoY | `paid_subscribers_yoy` | 2024-Q1 | 0.5416666666666667 | 54.2% | 0.28421052631578947 | 28.4% |
| Revenue YoY | `revenue_yoy` | 2024-Q1 | 0.44865598602813384 | 44.9% | 0.3497137404580153 | 35.0% |

## NULLs and definition checks

- The complete processed file contains 32 unavailable derived cells: four QoQ fields × one NULL in 2023-Q1, four YoY fields × four NULLs in 2023, and three growth-gap fields × four NULLs in 2023.
- Do not replace blanks with zero or use a Tableau `ZN` calculation to fabricate unavailable comparisons.
- MAU and DAU are separately averaged quarterly activity counts; paid subscribers are period-end counts; revenue is quarterly GAAP total revenue.
- DAU/MAU is an aggregate engagement-intensity proxy, not cohort retention or an individual daily-activity probability.
- Percentage change annotations use fractions formatted as percent; the ratio change annotation uses percentage points.

## Remaining Tableau acceptance checks

In the native workbook, verify the five displayed KPIs, the five annotations, every first/last endpoint above, all 12 quarter labels and the eight non-NULL marks per YoY series. Confirm that the Q4 2025 filter applies only to the KPI-card worksheets. Confirm the approved fixed 1600 × 900 layout and English findings/footer visually. These GUI checks remain unverified by this document.
