# Tableau Delivery & Maintenance

**Status (October 18, 2026):** The final two-page Tableau dashboard is published: [Page 1](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P1_Growth_Monetisation_Overview?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) / [Page 2](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P2_Growth_Diagnostics_Strategic_Context?:showVizHome=no). Both pages' public PNG exports were retrieved without authentication on this date. Interactive browser tabs were not tested. The [final native workbook](dashboard/final/Duolingo_Growth_Marketing_Analytics.twbx) is included, and [docs/portfolio_links.json](docs/portfolio_links.json) is the central link record.

**状态（2026 年 10 月 18 日）：** 最终两页 Tableau Dashboard 已发布：[Page 1](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P1_Growth_Monetisation_Overview?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) / [Page 2](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P2_Growth_Diagnostics_Strategic_Context?:showVizHome=no)。当日已在未登录状态下取得两页的公开 PNG 导出；本次未测试浏览器中的交互标签页。仓库包含[最终原生工作簿](dashboard/final/Duolingo_Growth_Marketing_Analytics.twbx)，链接统一维护于 [docs/portfolio_links.json](docs/portfolio_links.json)。

## Fixed scope

Analysis remains as of **March 2026**. Corporate data covers **Q1 2023-Q4 2025** only. Website and social snapshots remain **February 2026** and **March 2026**, respectively. Competitor data provides single-period context, with original historical captures unavailable. The delivery update does not change the analysis cutoff, data definitions or conclusions.

## Final presentation assets

- Final native workbook: `dashboard/final/Duolingo_Growth_Marketing_Analytics.twbx`. The earlier `工作簿 1.twbx` is retained as an original file.
- Final English Tableau images: `dashboard/final/tableau_page1.png` and `dashboard/final/tableau_page2.png`. Both language case studies use these same final visuals.
- Tableau Public links: `tableau_public_url` (Page 1) and `tableau_public_page2_url` (Page 2) in `docs/portfolio_links.json`. Verification metadata records the public-image-export check and its scope.
- Earlier bilingual PNGs in `dashboard/english/`, `dashboard/chinese/` and `dashboard/screenshots/` are **legacy static prototypes**, retained for reference. They are not the final Tableau visuals.
- [Maintenance guide](docs/tableau_build_guide.md), [data dictionary](docs/data_dictionary.md) and [source manifest](docs/source_manifest.csv).

## Final dashboard structure and priorities

- **Page 1 — Growth & Monetisation Overview:** Q4 2025 KPI cards, audience and engagement trends, monetisation trends and YoY growth comparison.
- **Page 2 — Growth Diagnostics & Strategic Context:** Q4 2025 growth-gap cards; Indexed Growth Comparison; Engagement Growth Gap; Monetisation Growth Gaps; separate Website Traffic (February 2026) and Social Audience (March 2026) contextual snapshots; Operational Priorities.
- The approved priority headings are **Protect engagement quality; Strengthen premium value communication; Balance growth with user control**（保护活跃质量；强化会员价值沟通；兼顾增长与用户自主控制）. Their supporting actions remain proposals for investigation, monitoring and testing. Public aggregates do not reveal the company’s internal measurement coverage.

## Data behind the workbook

- Wide quarterly CSV: 12 rows and 16 derived fields; optional long CSV: 156 rows / 13 measures.
- Website context: three rows. Social context: nine platform-specific rows. These remain separate sources.
- The previously validated CSV values and formulas remain unchanged.

## Future update checks

1. Preserve the fixed analysis dates, units, missing values and Q4 2025 card period.
2. Reconcile any edited cards and chart marks with the processed CSVs. Do not sum ratios, quarterly user counts or overlapping social audiences.
3. Inspect titles, labels, endpoints, tooltips and footers at normal viewing size; retain the source, ratio and competitor qualifications.
4. Keep the two final dashboard images aligned with the workbook when updating presentation assets. Translation may change narrative text, not calculations or findings.
5. If a workbook update changes the Tableau Public URLs, update the central link record, check both pages and regenerate the HTML, PDF and PPTX case studies so their links and visuals match.

Historical audit files describe their earlier verification scope. They are retained as records and do not supersede this delivery status.
