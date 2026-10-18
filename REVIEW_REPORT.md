> Historical audit record from October 14, 2026. Dashboard delivery status has since changed. See the [October 18 portfolio update](docs/portfolio_update_2026_10_18.md) for current case-study and Tableau status. The original verification results below remain historical evidence.

# Independent Review Report

Review date: 14 October 2026. Analysis remains **as of March 2026**, with corporate data restricted to **2023-Q1–2025-Q4**. Website/social observations remain the supplied February/March 2026 historical snapshots.

## Continuation state, verified before new edits

The interrupted review/polish task was **partially completed**. The original folder contained 40 files. The review report and five SQL scripts were newer than the original build; the builder, notebook, source manifest, documentation, dashboards and case-study exports were still original. `FINAL_QA.md`, `CHANGELOG.md` and `TABLEAU_HANDOFF.md` were absent. No Git repository or AGENTS.md was present. File timestamps and hashes were recorded before edits, and every underlying input/output family was inspected directly.

The pre-edit status was: **A)** original deliverables and SQL repairs existed; **B)** notebook/build/documentation/visual repairs and completion records remained; **C)** stale review references, destructive builder behavior, announcement-only source links, unsupported Tableau claims and absent competitor captures needed attention; **D)** corporate numbers/calculations passed while content/visual QA failed; **E)** preserve good data/SQL, complete only remaining repairs and verify regenerated outputs. The audit did not rely on README or prior-review claims as proof. See `docs/qa_inventory.json` for original file fingerprints and final comparisons.

## Initial audit, recorded before fixes

The audit covered every original file: both READMEs, all raw/processed CSVs, six SQL scripts, the executed notebook, builder, documentation and resume copy, four dashboard PNGs and four screenshot copies, both HTML case studies, both seven-slide PPTX files and both seven-page PDFs. Original PDF pages were rendered and visually inspected. No AGENTS.md or actual Tableau workbook was present. This folder is not a Git repository.

| ID | Severity | Finding and evidence | Required correction |
|---|---|---|---|
| H01 | HIGH | Case-study context presents inherited RACE findings as established evidence; original coursework report is absent. | Describe coursework as motivation, distinguish hypotheses from findings verified here. |
| H02 | HIGH | READMEs, Page 2 and slide 6 infer pricing/packaging upside from subscriber/revenue growth exceeding MAU. Aggregate growth cannot establish willingness to pay, efficiency or tactic effectiveness. | Preserve monetisation priority as measured investigation with free-experience guardrails. |
| H03 | HIGH | Conversion recommendations imply Duolingo lacks instrumentation. Only the portfolio's lack of access is established. | Audit existing measurement with authorised internal data before proposing missing events or experiments. |
| H04 | HIGH | Resume headers and slide 7 list Tableau despite no .twb/.twbx. | Resolved: the native two-page workbook is complete and published, and the current case studies embed its final Public exports. |
| H05 | HIGH | Builder hardcodes /mnt/data and a Linux CJK font, omits required dependencies, overwrites raw sources and does not regenerate PDFs. | Make build location-independent, preserve canonical inputs, use portable fonts and reproducible export steps. |
| M01 | MEDIUM | Four manifest URLs point to announcements without numerical tables; Q4 2025 ratio note cites the wrong document. | Link verified original shareholder letters and supplemental 2025 10-K. |
| M02 | MEDIUM | SQL 'missing-quarter' check detects duplicates only. Replacing 2023-Q2 with 2026-Q1 still passes its checks. | Validate the exact expected quarter sequence, metadata, dates and bounds. |
| M03 | MEDIUM | Notebook compares 7/16 derived columns by row position, lacks assertions and never executes SQL despite cross-check wording. | Reconcile all fields by key, assert missing-value masks and execute SQL with disclosed engine limitations. |
| M04 | MEDIUM | SQL and CSV diagnostic aliases differ. | Standardise names and document units and NULL behavior. |
| M05 | MEDIUM | Page 2 repeats Page 1 monetisation YoY lines and cumulative headline totals. | Use percentage-point growth gaps and operational interpretation to add analytical value. |
| M06 | MEDIUM | Dashboard sources, latest-card period and ratio limitations are insufficiently visible. End-quarter labels are missing on several axes. | Add compact source/definition footer, explicit Q4 2025 labels and readable final-quarter ticks. |
| M07 | MEDIUM | Page 2 narrative wraps outside its panels; CN line breaks split English metric names; slide dashboard embeds crop the bottom content. | Bound text, improve bilingual wrapping, fit full dashboard content within existing slide/page structure. |
| M08 | MEDIUM | Busuu pages/visit becomes an engagement-quality inference; competitor rows claim exact dates without original captures. | Keep historical numbers, state browsing metrics do not establish conversion/retention, mark historical provenance as unverified. |
| M09 | MEDIUM | Dictionary omits processed fields, competitor units, ratio-of-averages caveat and rounding differences. | Define all datasets, calculations and measurement timing. |
| M10 | MEDIUM | CN resume optional copy claims strategic shift/commercial efficiency, stronger than EN and available evidence. | Align quantified findings and avoid implied corporate strategy or efficiency conclusions. |
| L01 | LOW | EN competitor question says March only; CN navigation and portfolio labels differ. Notebook summary has mixed change units. | Align periods/navigation and distinguish percent growth from percentage-point changes. |

No CRITICAL issue was found. No raw value or derived formula error was found. No major business conclusion needs removal or a scope change.

## Independent data evidence

- All **72 raw corporate metric cells** (six metrics × twelve quarters) match original official IR/SEC disclosures published by February 2026. Financial precision changes from disclosed dollar-thousands to one-decimal millions. No raw values need replacement.
- All **16 derived fields** match independent Decimal calculations, including NULL masks. Final direct Decimal reconciliation differs by at most **5.10e-14**; SQL/CSV floating-point reconciliation differs by at most **2.84e-14**, both below the 1e-10 tolerance.
- SQL formulas executed through a SQLite compatibility adaptation reconcile with Python. This does not constitute native MySQL testing.
- Competitor inputs match all supplied historical values: three web rows and nine platform-specific social rows. No current replacements, follower totals or fabricated series.
- Q4 2025: 133.1M MAU, 52.7M DAU, 12.2M paid accounts, $282.9M revenue; derived DAU/MAU 39.6%; YoY 14.1%, 30.1%, 28.4%, 35.0%. Growth gaps: 16.1/14.4/20.9 pp for DAU/paid/revenue versus MAU.

## Business and visual judgement

The central growth story is supported: daily activity, paid subscribers and revenue expanded faster than MAU across the fixed window. DAU/MAU measures aggregate engagement intensity, not cohort retention. Revenue growth does not isolate subscription conversion or pricing effects. Page 1 should show observed growth; Page 2 should identify diagnostic divergences and propose operational reviews, rather than repeat trends.

The original navy/green visual language and two-page/seven-slide structure are appropriate and will be preserved. Necessary polishing concerns sources, text fit, chart redundancy, endpoint labels and dashboard fitting in slide exports.

## Final disposition

The remaining public-data review and polish work is **complete**, with regenerated and inspected deliverables. The three raw CSVs, four already-correct processed CSVs and all six maintained SQL scripts retain their original bytes and modification times. No analysis period or quantitative source value changed.

All H01-H05, M01-M10 and L01 corrections are addressed through guarded operational language, explicit provenance/tool status, corrected source links, complete definitions, a safe builder, genuinely executed notebook, and bounded bilingual visuals. Page 2 now adds growth-gap diagnostics; dashboard endpoints/card dates/source footers are visible; full PNGs fit within both seven-slide decks. All four dashboards and all 14 final PDF pages were inspected. PDFs were regenerated from the actual final PPTXs. Final package/layout checks report no findings or warnings.

See [final QA](FINAL_QA.md), [change log](CHANGELOG.md), [machine-readable evidence](docs/qa_evidence.json) and [Tableau handoff](TABLEAU_HANDOFF.md). Corporate data, calculations, bilingual content and rendered deliverables pass within the declared evidence scope. Competitor historical provenance remains explicitly unverified because original captures are absent. Native MySQL and PowerPoint-app behaviour were outside that historical audit. Current Tableau publication and case-study exports are covered by FINAL_QA.md. These limitations are disclosed consistently rather than replaced with fabricated evidence.
