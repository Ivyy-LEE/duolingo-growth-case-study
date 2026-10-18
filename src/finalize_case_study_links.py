"""Attach and verify native Tableau hyperlinks after case-study export.

Presentation text hyperlinks use Artifact Tool. This adds PDF URI annotations
after conversion and verifies that the exact Share URL survives the export.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

def attach_pdf(path: Path, url: str) -> None:
    from pypdf import PdfReader, PdfWriter
    from pypdf.annotations import Link

    reader = PdfReader(path)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    # Slide units are CSS pixels; PDF uses 72 points per inch, at 0.75 points/px.
    contracts = {
        0: (50.4, 28.8, 907.2, 48.0),
        2: (81.0, 21.0, 879.0, 496.0),
        3: (81.0, 21.0, 879.0, 496.0),
    }
    for page_index, rectangle in contracts.items():
        writer.add_annotation(page_index, Link(rect=rectangle, url=url))
    temporary = path.with_suffix(".linked.pdf")
    with temporary.open("wb") as stream:
        writer.write(stream)
    temporary.replace(path)
    check = PdfReader(path)
    assert len(check.pages) == 7
    for page_index in contracts:
        targets = [node.get_object().get("/A", {}).get("/URI") for node in check.pages[page_index].get("/Annots", [])]
        assert url in targets, (path, page_index, targets)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("format", choices=["pdf"])
    parser.add_argument("path", type=Path)
    parser.add_argument("--links", type=Path, required=True)
    args = parser.parse_args()
    url = json.loads(args.links.read_text())["tableau_public_url"]
    if not url.startswith("https://public.tableau.com/views/"):
        raise ValueError("Expected the approved Tableau Public view URL")
    attach_pdf(args.path, url)
    print(f"Verified exact Tableau Share URL in {args.format.upper()} click actions")


if __name__ == "__main__":
    main()
