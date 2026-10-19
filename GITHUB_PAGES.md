# GitHub Pages publication

This folder is a buildless static portfolio website. Publish `main` → `/(root)` using GitHub Pages. The `.nojekyll` file preserves the packaged static files without a Jekyll build.

- Chinese entry point: `index.html`
- English route: `en/index.html`
- Shared Chinese copy: `src/copy_zh_cn.json`
- Recommended repository name: `duolingo-growth-case-study`
- Tableau links: `docs/portfolio_links.json`
- Frozen source and per-file hashes: `PUBLICATION_SOURCE.json`

## Content provenance

The source is the most recently modified final archive: `Duolingo_Growth_Operations_Portfolio_Layout_Final.zip`, SHA-256 `ceb8310a6a3a9309bd34e0bb861a93cf06de39c1bded9bccff63847f5fa08eb6`.

The original archive hashes are retained as historical source references in PUBLICATION_SOURCE.json. Data, metric definitions, SQL/Python analysis, final Tableau images/workbook and the approved English PDF/PPTX/standalone HTML remain unchanged. Curated Chinese wording comes from one shared source and is regenerated into the Chinese homepage, case-study PDF/PPTX/HTML and README. The approved English homepage is retained at /en/. No analysis, dataset, recommendation or caveat has been changed. Implementation/history copies use portable or repository-relative paths.

In particular, Page 2 uses the final complete local Tableau capture (SHA-256 `84564dfee55fc9ca26a2669193270883df3b1bc90006f2234459dade2892775d`). Do not replace it with the clipped Tableau Public image export.

Analysis remains as of March 2026. Website context remains February 2026; social context remains March 2026. Publication date does not update these dates.

## Maintenance

For Chinese wording, edit `src/copy_zh_cn.json`, then run the Chinese-only `src/build_case_studies.mjs` with the documented runtime environment. It regenerates the Chinese PDF/PPTX, Chinese web pages and Chinese README. `src/build_public_pages.py` handles a web-only refresh. Keep the approved English deliverables, data, calculations and final Tableau assets unchanged. Visually inspect all seven Chinese PDF pages after regenerating. All homepage paths are relative and support both a repository subpath and an account root site. No third-party script, font service, analytics or build dependency is required.

Official GitHub instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
