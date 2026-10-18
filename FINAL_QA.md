# Final exported case-study verification

Updated October 18, 2026 for the revised English and Chinese outputs.

The existing seven-slide case studies were edited in place. Both PDF and PPTX versions use the final published Tableau Page 1 and Page 2 views. The approved operating priorities are restored verbatim in English, with faithful Chinese translations. All four case-study files provide clickable access to the exact owner-supplied Tableau Public Share URL.

## Exported files checked

- English PDF and PPTX: seven pages/slides each.
- Chinese PDF and PPTX: seven pages/slides each.
- Both READMEs and HTML case studies: exact Share URL and final image references.
- Final distribution ZIP: revised binaries and final dashboard assets.

## Verification scope

The final PDFs were rendered after export and all 14 pages were visually inspected. The PPTX package, geometry, font and import validators passed. Hyperlink relationships in the PPTXs and URI annotations in the PDFs are checked against the exact full Share URL, including its query parameters. Dashboard images are inspected inside the exported files and compared against the published Tableau exports. The ZIP is reopened to compare its members with the revised files.

Seventeen frozen source files remain byte-identical: raw and processed data, SQL, source manifest, data dictionary and both native workbooks. Headline values, dates, competitor caveats, missing-value treatment and non-causal interpretation are unchanged.

## Final Tableau Page 2

The page retains Q4 2025 growth-gap cards, Indexed Growth Comparison, Engagement Growth Gap, Monetisation Growth Gaps, separate Website Traffic and Social Audience contextual snapshots, and Operational Priorities.

The three priorities are **Protect engagement quality**, **Strengthen premium value communication**, and **Balance growth with user control**. These are operational proposals. Public aggregates do not reveal internal measurement coverage, and this portfolio claims no implemented business impact.

## Distribution and limitations

Only the final published dashboard images and current native workbook are included in the final distribution. Earlier static prototypes and the older local workbook remain in the working repository for history.

Competitor snapshots remain contextual and historically unverified. The analysis stays as of March 2026. Native MySQL execution and native PowerPoint-app behaviour remain outside the verified scope. Public image export retrieval and embedded link targets were checked; no claim is made that interactive browser tabs were exercised.

Detailed export results are recorded in [machine-readable verification](docs/export_verification.json). Earlier source-audit evidence remains in docs/qa_evidence.json.
