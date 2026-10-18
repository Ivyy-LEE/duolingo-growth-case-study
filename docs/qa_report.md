> Historical audit record from October 14, 2026. Dashboard delivery status has since changed. See the [October 18 portfolio update](portfolio_update_2026_10_18.md) for current case-study and Tableau status. The original verification results below remain historical evidence.

# QA Report

Verified October 14, 2026. Analysis remains as of March 2026.

- PASS - 72 corporate metric values match official historical IR/SEC disclosures.
- PASS - exact 12-quarter sequence (Q1 2023-Q4 2025), metadata, dates, uniqueness and bounds.
- PASS - all 16 derived fields, 192 cells/32 NULLs and 156 long rows independently reconcile.
- PASS - actual maintained SQL formulas executed through disclosed SQLite adaptation; native MySQL untested.
- PASS - notebook genuinely executed, four real code-cell outputs and no errors.
- PASS - original raw/processed CSV and SQL bytes/mtimes preserved.
- PASS - four bilingual dashboards and all 14 final PDF pages visually inspected; PNG copies/embeds match.
- PASS - bilingual data, conclusions, proposals, links and evidence limits align.
- UNVERIFIED - inherited competitor historical provenance, with original captures absent.
- COMPLETE - native Tableau workbook and publication. Current bilingual case studies use final Public exports and clickable Share URL links; see ../FINAL_QA.md.

Full results and limits: [Final QA](../FINAL_QA.md). Machine evidence: [qa_evidence.json](qa_evidence.json). Initial/final fingerprints: [qa_inventory.json](qa_inventory.json).
