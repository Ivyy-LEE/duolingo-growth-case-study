"""Preserve the two frozen dashboard PDF pages after Chinese text regeneration."""
from pathlib import Path
from argparse import ArgumentParser
from pypdf import PdfReader,PdfWriter
p=ArgumentParser();p.add_argument('reference',type=Path);p.add_argument('candidate',type=Path);a=p.parse_args()
source=PdfReader(a.reference);updated=PdfReader(a.candidate)
assert len(source.pages)==len(updated.pages)==7
out=PdfWriter()
for i in range(7):out.add_page(source.pages[i] if i in (2,3) else updated.pages[i])
if updated.metadata:out.add_metadata({str(k):str(v) for k,v in updated.metadata.items() if v is not None})
tmp=a.candidate.with_suffix('.preserved.pdf')
with tmp.open('wb') as f:out.write(f)
tmp.replace(a.candidate)
print('Preserved the two frozen dashboard PDF pages and their annotations')
