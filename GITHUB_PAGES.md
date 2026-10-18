# GitHub Pages publication

This folder is a buildless static portfolio website. Publish `main` → `/(root)` using GitHub Pages. The `.nojekyll` file preserves the packaged static files without a Jekyll build.

- Entry point: `index.html`
- Recommended repository name: `duolingo-growth-case-study`
- Tableau links: `docs/portfolio_links.json`
- Frozen source and per-file hashes: `PUBLICATION_SOURCE.json`

## Content provenance

The source is the most recently modified final archive: `Duolingo_Growth_Operations_Portfolio_Layout_Final.zip`, SHA-256 `ceb8310a6a3a9309bd34e0bb861a93cf06de39c1bded9bccff63847f5fa08eb6`.

All final case-study files, the original README, data, metric definitions, Tableau images and workbook are retained byte-for-byte (47 original files). Only two implementation/history files have public copies with local machine paths normalised; their original hashes and the normalisation scope are recorded in PUBLICATION_SOURCE.json. No analytical or case-study content changes. The new homepage reorganises frozen English case-study prose and adds section navigation, responsive CSS, download links and direct Tableau CTAs. No analysis, dataset, recommendation or caveat has been refreshed.

In particular, Page 2 uses the final complete local Tableau capture (SHA-256 `84564dfee55fc9ca26a2669193270883df3b1bc90006f2234459dade2892775d`). Do not replace it with the clipped Tableau Public image export.

Analysis remains as of March 2026. Website context remains February 2026; social context remains March 2026. Publication date does not update these dates.

## Maintenance

Edit only the homepage and `assets/` for presentation changes. Treat original deliverables and source files as frozen. All homepage paths are relative and support both a repository subpath and an account root site. No third-party script, font service, analytics or build dependency is required.

Official GitHub instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
