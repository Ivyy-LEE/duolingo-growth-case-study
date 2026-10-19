#!/usr/bin/env python3
"""Build the Chinese homepage from shared copy and the approved English page.

The curated English page in en/index.html is the stable, approved template.
It supplies existing published Tableau/resource URLs and dashboard dimensions;
Chinese prose comes only from copy_zh_cn.json. No dashboard asset is rewritten.
Run from any directory: python3 src/build_public_pages.py
"""

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]


class ApprovedPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        elif tag == "img":
            self.images.append(attrs)


def e(value):
    return escape(str(value), quote=True)


def local_root(href):
    """Reverse the English route's one-level asset prefix for the root page."""
    return href[3:] if href.startswith("../") else href


def render():
    copy = json.loads((ROOT / "src" / "copy_zh_cn.json").read_text())
    labels, cta = copy["labels"], copy["cta"]
    template = ApprovedPage()
    template.feed((ROOT / "en" / "index.html").read_text())
    tableau = next(url for url in template.links if "public.tableau.com" in url and "/P1_" in url)
    tableau2 = next(url for url in template.links if "public.tableau.com" in url and "/P2_" in url)
    repository = next(url for url in template.links if "github.com/" in url)
    chinese_pdf = local_root(next(url for url in template.links if url.endswith("_CN.pdf")))
    english_pdf = local_root(next(url for url in template.links if url.endswith("_EN.pdf")))
    images = [image for image in template.images if "dashboard/final/" in image["src"]]
    if len(images) != 2:
        raise ValueError("The approved English page must contain exactly two final dashboard images")

    def external(href, text, css=""):
        class_attr = f' class="{e(css)}"' if css else ""
        return f'<a{class_attr} href="{e(href)}" target="_blank" rel="noopener noreferrer">{e(text)}</a>'

    def heading(number, title):
        return f'<div class="section-heading"><span class="section-number">{number:02d}</span><h2>{e(title)}</h2></div>'

    def items(values, tag="ul", css=""):
        class_attr = f' class="{e(css)}"' if css else ""
        return f'<{tag}{class_attr}>' + "".join(f'<li>{e(value)}</li>' for value in values) + f'</{tag}>'

    language_switch = (
        f'<nav class="language-switch" aria-label="{e(labels["languageNavigation"])}">'
        f'<span lang="zh-Hans" aria-current="page">{e(labels["languageChinese"])}</span>'
        '<span class="language-divider" aria-hidden="true">|</span>'
        f'<a href="en/" lang="en" hreflang="en">{e(labels["languageEnglish"])}</a></nav>'
    )
    scope = "".join(
        f'<div><dt>{e(labels[key])}</dt><dd>{e(labels[key + "Value"])}</dd></div>'
        for key in ("corporatePerformance", "analysisAsOf", "competitiveContext")
    )
    nav = "".join(f'<a href="#{e(anchor)}">{e(text)}</a>' for anchor, text in copy["nav"].items())
    dashboard_figures = []
    for number, (image, link) in enumerate(zip(images, (tableau, tableau2)), 1):
        image_path = local_root(image["src"])
        dashboard_figures.append(
            '<figure class="dashboard">'
            f'<a href="{e(image_path)}"><img width="{e(image["width"])}" height="{e(image["height"])}" '
            f'loading="lazy" src="{e(image_path)}" alt="{e(labels[f"dashboardPage{number}Alt"])}"></a>'
            f'<figcaption>{e(labels[f"dashboardPage{number}Caption"])}<span class="figure-actions">'
            + external(link, cta[f"tableauPage{number}"])
            + f'<a href="{e(image_path)}" target="_blank" rel="noopener">{e(cta["fullSizeImage"])}</a>'
            '</span></figcaption></figure>'
        )
    operations = "".join(f'<h3>{e(title)}</h3><p>{e(body)}</p>' for title, body in copy["recs"])

    return f'''<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(copy["title"])} | {e(labels["portfolio"])}</title>
<meta name="description" content="{e(copy["cover"])}">
<meta name="theme-color" content="#226b38">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="stylesheet" href="assets/style.css">
<link rel="alternate" hreflang="zh-Hans" href="./">
<link rel="alternate" hreflang="en" href="en/">
</head>
<body>
<a class="skip" href="#main">{e(cta["skip"])}</a>
<header class="topbar"><div class="topbar-inner"><a class="brand" href="#overview">{e(labels["brand"])} <span>/ {e(labels["brandSuffix"])}</span></a><div class="topbar-tools">{language_switch}{external(tableau, cta["tableauShort"], "top-cta")}</div></div></header>
<main id="main">
<div class="hero page-width" id="overview">
<p class="eyebrow">{e(labels["portfolio"])}</p>
<h1>{e(copy["title"])}</h1>
<p class="sub">{e(copy["roleLine"])}</p>
<p class="lead">{e(copy["cover"])}</p>
<div class="actions">{external(tableau, cta["tableau"], "button primary")}<a class="button secondary" href="{e(chinese_pdf)}">{e(cta["chinesePdf"])}</a></div>
<dl class="scope">{scope}</dl>
<p class="role">{e(copy["role"])}</p>
</div>
<nav class="section-nav page-width" aria-label="{e(labels["sectionNavigation"])}">{nav}</nav>
<div class="page-width content">
<section id="question">{heading(1, labels["businessQuestions"])}<p>{e(copy["context"])}</p>{items(copy["qs"], "ol")}</section>
<section id="dashboards">{heading(2, labels["dashboards"])}<p class="small">{e(labels["dashboardNote"])}</p>{"".join(dashboard_figures)}</section>
<section id="findings">{heading(3, labels["findings"])}{items(copy["findings"], "ol", "findings")}</section>
<section id="operations">{heading(4, labels["operations"])}<p class="small">{e(copy["operationsIntro"])}</p>{operations}</section>
<section id="method">{heading(5, labels["method"])}{items(copy["scope"])}<p class="small">{e(copy["rounding"])}</p><details class="method-details"><summary>{e(labels["calculationDetails"])}</summary>{items(copy["methods"])}<p>{e(copy["tech"])}</p><p>{e(copy["definitions"])}</p></details></section>
<section id="limits">{heading(6, labels["limits"])}{items(copy["limits"])}<p class="small">{e(copy["competitorCaveat"])}</p><p class="small">{e(copy["companyDefinition"])}</p></section>
<section id="resources" class="resources"><h2>{e(labels["resources"])}</h2><div class="actions">{external(tableau, cta["tableau"], "button primary")}</div><nav aria-label="{e(labels["resourceNavigation"])}"><a href="{e(chinese_pdf)}" lang="zh-Hans">{e(cta["chinesePdf"])}</a><a href="{e(english_pdf)}" lang="en">{e(cta["englishPdf"])}</a>{external(repository, cta["repository"])}</nav></section>
</div>
</main>
<footer class="page-width"><p>{e(copy["footer"])}</p><p>{e(labels["independentPortfolio"])}</p><a href="#overview">{e(cta["backToTop"])}</a></footer>
</body></html>
'''


if __name__ == "__main__":
    target = ROOT / "index.html"
    homepage = render()
    target.write_text(homepage)
    # Keep the previously shared standalone Chinese HTML on the same curated copy.
    # Rebase every site-relative resource to retain this older public URL.
    def legacy_link(match):
        attribute, value = match.groups()
        if value.startswith(("#", "http:", "https:", "//", "mailto:", "tel:", "data:")):
            return match.group(0)
        return f'{attribute}="../{value}"'

    legacy = re.sub(r'(href|src)="([^"]+)"', legacy_link, homepage)
    legacy = legacy.replace('href=".././"', 'href="../"')
    chinese_label = e(json.loads((ROOT / "src" / "copy_zh_cn.json").read_text())["labels"]["languageChinese"])
    legacy = legacy.replace(
        f'<span lang="zh-Hans" aria-current="page">{chinese_label}</span>',
        f'<a href="../" lang="zh-Hans" hreflang="zh-Hans" aria-current="page">{chinese_label}</a>',
    )
    (ROOT / "case_study" / "case_study_cn.html").write_text(legacy)
    print(f"Built {target.relative_to(ROOT)} from src/copy_zh_cn.json and en/index.html")
    print("Built case_study/case_study_cn.html from the same curated Chinese page")
