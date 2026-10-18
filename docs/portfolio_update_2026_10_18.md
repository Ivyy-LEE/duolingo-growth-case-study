# Portfolio update - October 18, 2026

The existing English and Chinese case studies now use the completed two-page Tableau dashboard. The update retains the original seven-slide structure and updates the corresponding HTML, PDF, PPTX, READMEs and resume entries for product, user, growth and general operations recruiting.

## Current presentation

- [English case study](../case_study/case_study_en.html)
- [Chinese case study](../case_study/case_study_cn.html)
- [Tableau Page 1](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P1_Growth_Monetisation_Overview?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- [Tableau Page 2](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P2_Growth_Diagnostics_Strategic_Context?:showVizHome=no)
- [Final packaged workbook](../dashboard/final/Duolingo_Growth_Marketing_Analytics.twbx)
- [Central link record](portfolio_links.json)

The final workbook is a copy of the newer downloaded workbook. The earlier root-level `工作簿 1.twbx` is retained unchanged in the working repository as a historical local version and is excluded from the final distribution. Earlier bilingual PNGs remain legacy prototypes in the working repository. The final distribution includes only the final published Tableau dashboard images.

## Scope and conclusions

Analysis remains as of March 2026. Corporate data covers Q1 2023-Q4 2025. Website and social snapshots retain February and March 2026 respectively.

The frozen findings remain unchanged: MAU +83%, DAU +160%, paid subscribers +154% and quarterly revenue +145% across the endpoint quarters. DAU/MAU rises from 28.0% to 39.6% (+11.6 percentage points). Q4 2025 rounded YoY growth remains 14%, 30%, 28% and 35% respectively.

Operational implications follow final Tableau Page 2: investigate sustained engagement, evaluate clearer premium value messaging and targeted trials, and assess configurable engagement settings with user-response monitoring. Measurement review and free-experience guardrails support proposed tests. These are proposals, with no claimed implementation, causal effect or measured business impact.

## Verification performed in this update

- Compared hashes of the three raw CSVs, four processed CSVs, six SQL files, source manifest, data dictionary and earlier workbook before and after editing. All 16 files remain byte-identical.
- Retrieved both final Tableau PNG exports without authentication and received HTTP 200 for the Page 1 public view on October 18, 2026. Both exports are 1599 x 926 pixels and include the Tableau footer. Interactive browser tab behaviour was not tested.
- Reused those public exports without retouching. Existing scrollbars and source-view truncation remain part of the original dashboards. The case-study text spells out the operational recommendations and limitations in full.
- Imported the existing PPTX files, edited their native text objects, and replaced only their dashboard illustrations. Both language decks retain seven slides. The narrative remains editable, while the Tableau views are embedded source images.
- Ran presentation package, geometry, font and import validation. Exported PDFs from the edited PPTX files and inspected all 14 rendered PDF pages.
- Checked HTML local links and image targets, seven-page PDF counts, frozen headline values and removal of obsolete current-status wording.

This update does not repeat or extend the October 14 source audit. Historical competitor captures remain unavailable. Native MySQL execution and PowerPoint-app behaviour remain unverified. Earlier audit reports retain their dated findings and now point here for current presentation status.

## Maintenance

Edit `portfolio_links.json` for Tableau links, then rebuild the case studies with `src/build_case_studies.mjs`. Final dashboard images live in `dashboard/final/`; both language versions use these same views. The analytical data and definitions remain frozen. The older static-dashboard generator is retained for historical prototype maintenance.

## Export revision

The revised outputs restore the exact approved priority headings and Tableau wording. PDF URI annotations and native PPTX text hyperlinks point to the exact owner-provided Share URL. The final PDFs, PPTXs and ZIP are reopened and checked after export; current results are in `FINAL_QA.md` and `docs/export_verification.json`.
