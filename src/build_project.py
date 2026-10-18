"""Rebuild derived data, executed QA notebook and static dashboard prototypes.

Canonical raw CSVs, maintained SQL, source manifest, prose and presentation
exports are inputs. This script never rewrites those files. Run from any folder:
    python /path/to/duolingo_growth_ops/src/build_project.py
Use --check-only for read-only data/SQL reconciliation.
"""
from __future__ import annotations

import argparse
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import tempfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
METRICS = {'mau_m': 'mau', 'dau_m': 'dau',
           'paid_subscribers_m': 'paid_subscribers', 'revenue_usd_m': 'revenue'}
DERIVED = ['dau_mau_ratio'] + [f'{stem}_{suffix}' for stem in METRICS.values()
                              for suffix in ('qoq', 'yoy', 'index')] + [
    'dau_yoy_minus_mau_yoy', 'paid_subscribers_yoy_minus_mau_yoy',
    'revenue_yoy_minus_mau_yoy']
LONG_METRICS = {'MAU (M)': 'mau_m', 'DAU (M)': 'dau_m', 'DAU/MAU': 'dau_mau_ratio',
                'Paid Subscribers (M)': 'paid_subscribers_m',
                'Revenue (USD M)': 'revenue_usd_m',
                'MAU YoY': 'mau_yoy', 'DAU YoY': 'dau_yoy',
                'Paid Subscribers YoY': 'paid_subscribers_yoy', 'Revenue YoY': 'revenue_yoy',
                'MAU Index': 'mau_index', 'DAU Index': 'dau_index',
                'Paid Subscribers Index': 'paid_subscribers_index', 'Revenue Index': 'revenue_index'}


def load_inputs(root=ROOT):
    q = pd.read_csv(root / 'data/raw/quarterly_performance.csv', parse_dates=['period_end'])
    web = pd.read_csv(root / 'data/raw/competitor_web_snapshot.csv')
    social = pd.read_csv(root / 'data/raw/social_snapshot.csv')
    manifest = pd.read_csv(root / 'docs/source_manifest.csv')
    expected = pd.period_range('2023Q1', '2025Q4', freq='Q')
    q = q.sort_values('period_end').reset_index(drop=True)
    assert len(q) == 12 and q.quarter.tolist() == [f'{p.year}-Q{p.quarter}' for p in expected], 'Exact 12-quarter scope required'
    assert q.period_end.tolist() == list(expected.end_time.normalize()), 'Quarter-end dates must match'
    assert q.fiscal_year.tolist() == [p.year for p in expected]
    assert q.quarter_num.tolist() == [p.quarter for p in expected]
    assert not q.quarter.duplicated().any() and not q.period_end.duplicated().any()
    core = list(METRICS)
    assert q[core].notna().all().all() and np.isfinite(q[core]).all().all() and (q[core] > 0).all().all()
    assert (q.dau_m <= q.mau_m).all()
    for c in ['total_bookings_usd_m', 'subscription_bookings_usd_m']:
        assert np.isfinite(q[c].dropna()).all() and (q[c].dropna() > 0).all()
    assert (q.subscription_bookings_usd_m.dropna() <= q.total_bookings_usd_m).all()
    assert len(web) == 3 and set(web.brand) == {'Duolingo', 'Babbel', 'Busuu'}
    assert not web.brand.duplicated().any() and (web.snapshot_month == '2026-02').all()
    web_values = ['total_visits_m', 'bounce_rate_pct', 'pages_per_visit', 'avg_visit_duration_sec']
    assert web[web_values].notna().all().all() and np.isfinite(web[web_values]).all().all()
    assert (web[['total_visits_m', 'pages_per_visit', 'avg_visit_duration_sec']] > 0).all().all()
    assert web.bounce_rate_pct.between(0, 100).all()
    assert len(social) == 9 and not social.duplicated(['brand', 'platform']).any()
    assert set(zip(social.brand, social.platform)) == {(b, p) for b in web.brand for p in ['TikTok', 'YouTube', 'Instagram']}
    assert (social.snapshot_month == '2026-03').all() and (social.followers > 0).all()
    assert np.isfinite(social.followers).all()
    assert (social.followers % 1 == 0).all()
    assert manifest.source_id.notna().all() and not manifest.source_id.duplicated().any()
    for data in [q, web, social]:
        assert data.source_id.notna().all() and set(data.source_id) <= set(manifest.source_id)
    sources = manifest.set_index('source_id')
    for dataset, data, period_field in [('quarterly_performance', q, 'quarter'),
                                        ('competitor_web_snapshot', web, 'snapshot_month'),
                                        ('social_snapshot', social, 'snapshot_month')]:
        for _, row in data.iterrows():
            assert sources.loc[row.source_id, 'dataset'] == dataset
            assert sources.loc[row.source_id, 'period'] == row[period_field]
    return q, web, social


def derive(q):
    proc = q.copy()
    proc['dau_mau_ratio'] = proc.dau_m / proc.mau_m
    for raw, stem in METRICS.items():
        proc[stem + '_qoq'] = proc[raw].pct_change(1, fill_method=None)
        proc[stem + '_yoy'] = proc[raw].pct_change(4, fill_method=None)
        proc[stem + '_index'] = proc[raw] / proc.iloc[0][raw] * 100
    for stem in ['dau', 'paid_subscribers', 'revenue']:
        proc[stem + '_yoy_minus_mau_yoy'] = proc[stem + '_yoy'] - proc.mau_yoy
    return proc


def compare_frames(actual, expected, keys, columns):
    """Compare by explicit keys, including missing-value masks and raw text/date fields."""
    assert not actual.duplicated(keys).any() and not expected.duplicated(keys).any()
    a = actual.set_index(keys).sort_index()
    b = expected.set_index(keys).sort_index()
    assert a.index.equals(b.index), f'Key mismatch: {keys}'
    diffs = {}
    for c in columns:
        assert c in a and c in b, f'Missing field: {c}'
        assert a[c].isna().equals(b[c].isna()), f'NULL-mask mismatch: {c}'
        mask = a[c].notna()
        if pd.api.types.is_numeric_dtype(b[c]):
            av = pd.to_numeric(a.loc[mask, c]).to_numpy(dtype=float)
            bv = b.loc[mask, c].to_numpy(dtype=float)
            np.testing.assert_allclose(av, bv, atol=1e-10, rtol=0, err_msg=c)
            diffs[c] = float(np.max(np.abs(av-bv))) if len(av) else 0.0
        elif pd.api.types.is_datetime64_any_dtype(b[c]):
            assert pd.to_datetime(a.loc[mask, c]).equals(b.loc[mask, c]), c
        else:
            assert a.loc[mask, c].astype(str).equals(b.loc[mask, c].astype(str)), c
    return diffs


def decimal_check(q, processed):
    """Independent Decimal formulas, separate from pandas pct_change/window SQL."""
    records = q.to_dict('records')
    expected = {}
    d = lambda v: Decimal(str(v))
    for i, r in enumerate(records):
        row = {'dau_mau_ratio': d(r['dau_m']) / d(r['mau_m'])}
        for raw, stem in METRICS.items():
            row[stem + '_index'] = d(r[raw]) / d(records[0][raw]) * 100
            for lag, suffix in [(1, 'qoq'), (4, 'yoy')]:
                row[stem + '_' + suffix] = d(r[raw]) / d(records[i-lag][raw])-1 if i >= lag else None
        for stem in ['dau', 'paid_subscribers', 'revenue']:
            if i >= 4:
                raw = next(c for c, s in METRICS.items() if s == stem)
                row[stem + '_yoy_minus_mau_yoy'] = (d(r[raw])/d(records[i-4][raw])-1) - (d(r['mau_m'])/d(records[i-4]['mau_m'])-1)
            else:
                row[stem + '_yoy_minus_mau_yoy'] = None
        expected[r['quarter']] = row
    assert not processed.quarter.duplicated().any()
    actual = processed.set_index('quarter')
    assert set(actual.index) == set(expected), 'Decimal quarter-key mismatch'
    diffs = {c: Decimal(0) for c in DERIVED}
    for quarter, values in expected.items():
        for field, value in values.items():
            observed = actual.loc[quarter, field]
            assert pd.isna(observed) == (value is None), f'Decimal NULL-mask mismatch: {quarter}/{field}'
            if value is not None:
                difference = abs(d(observed)-value)
                assert difference <= Decimal('1e-10'), f'Decimal value mismatch: {quarter}/{field}'
                diffs[field] = max(diffs[field], difference)
    return {field: float(value) for field, value in diffs.items()}


def adapt_sql(text):
    # SQLite provides an independent execution of these formulas; this adaptation
    # does not certify MySQL DECIMAL precision, coercion, DDL or constraints.
    text = re.sub(r'--[^\n]*', '', text)
    text = re.sub(r'^\s*(?:CREATE DATABASE|USE)\b[^;]*;', '', text, flags=re.M | re.I)
    return text.replace('CREATE OR REPLACE VIEW', 'CREATE VIEW').replace('AS DOUBLE', 'AS REAL')


def sql_check(q, web, social, processed, root=ROOT):
    with sqlite3.connect(':memory:') as conn:
        for f in ['01_schema.sql', '00_seed_data.sql', '03_growth_metrics.sql', '05_dashboard_views.sql']:
            conn.executescript(adapt_sql((root / 'sql' / f).read_text()))
        for table, frame, keys in [('quarterly_performance', q, ['quarter']), ('competitor_web_snapshot', web, ['brand']), ('social_snapshot', social, ['brand', 'platform'])]:
            seeded = pd.read_sql_query('SELECT * FROM ' + table, conn)
            compare_frames(seeded, frame, keys, [c for c in frame if c not in keys])
        sql = pd.read_sql_query('SELECT * FROM v_growth_metrics ORDER BY period_end', conn)
        compare_frames(sql, processed, ['quarter'], DERIVED[:13])
        dashboard = pd.read_sql_query('SELECT * FROM v_dashboard_quarterly ORDER BY period_end', conn)
        diffs = compare_frames(dashboard, processed, ['quarter'], DERIVED)
        compare_frames(dashboard, processed, ['quarter'], [c for c in dashboard if c != 'quarter'])
        validations = []
        for stmt in adapt_sql((root / 'sql/02_validation.sql').read_text()).split(';'):
            if stmt.strip():
                validations.append(conn.execute(stmt).fetchall())
        assert validations[0] == [(12, 12)] and all(v == [] for v in validations[1:]), validations
        comparisons = [conn.execute(stmt).fetchall() for stmt in adapt_sql((root / 'sql/04_period_comparison.sql').read_text()).split(';') if stmt.strip()]
        assert len(comparisons[0]) == 8 and comparisons[1][0] == ('2025-Q4', 133.1, 52.7, 39.6, 12.2, 282.9, 4.9, 14.1, 30.1, 28.4, 35.0)
    return diffs


def make_long(proc):
    rows = [(r.quarter, r.period_end.date().isoformat(), metric, r[field])
            for _, r in proc.iterrows() for metric, field in LONG_METRICS.items()]
    return pd.DataFrame(rows, columns=['quarter', 'period_end', 'metric', 'value'])


def check_processed(q, web, social, root=ROOT):
    expected = derive(q)
    proc = pd.read_csv(root / 'data/processed/quarterly_dashboard.csv', parse_dates=['period_end'])
    assert proc.columns.tolist() == expected.columns.tolist(), 'Processed schema must be preserved'
    compare_frames(proc, expected, ['quarter'], [c for c in expected if c != 'quarter'])
    for name, frame, keys in [('competitor_web_snapshot', web, ['brand']), ('social_snapshot', social, ['brand', 'platform'])]:
        compare_frames(pd.read_csv(root / f'data/processed/{name}.csv'), frame, keys, [c for c in frame if c not in keys])
    long = pd.read_csv(root / 'data/processed/tableau_quarterly_long.csv')
    assert len(long) == 156 and long.columns.tolist() == ['quarter', 'period_end', 'metric', 'value']
    compare_frames(long, make_long(expected), ['quarter', 'metric'], ['period_end', 'value'])
    return proc, decimal_check(q, proc), sql_check(q, web, social, proc, root)


def build_notebook(root=ROOT):
    scratch = Path(tempfile.gettempdir()) / 'duolingo-notebook-runtime'
    for name in ['JUPYTER_RUNTIME_DIR', 'JUPYTER_CONFIG_DIR', 'IPYTHONDIR']:
        folder = scratch / name.lower()
        folder.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault(name, str(folder))
    import nbformat as nbf
    from nbclient import NotebookClient
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell('# Duolingo Growth & Marketing Operations Analytics\n\nExecuted QA and business diagnostics. Analysis as of **March 2026**; corporate scope **Q1 2023–Q4 2025**, website **February 2026**, social **March 2026**. Canonical public data are preserved. DAU/MAU is a ratio of reported average counts, not cohort retention or average individual use.'),
        nbf.v4.new_code_cell("from pathlib import Path\nimport sys\nimport pandas as pd\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nassert (ROOT/'src/build_project.py').is_file()\nsys.path.insert(0, str(ROOT/'src'))\nimport build_project as build\nq, web, social = build.load_inputs(ROOT)\nprint(f'Validated exact scope: {len(q)} quarters, {len(web)} website rows, {len(social)} social rows.')\nq[['quarter','mau_m','dau_m','paid_subscribers_m','revenue_usd_m']]"),
        nbf.v4.new_markdown_cell('## Independent calculation and output reconciliation\n\nAll **16 derived fields** are checked by quarter key, including every missing-value mask. Pandas calculations are reconciled with separate Decimal arithmetic and independently executed SQL formulas. Raw values and all **156** long-format rows are also checked. Growth rates are fractions in CSVs; multiplying by 100 gives percent. Differences of growth rates multiplied by 100 give percentage points.'),
        nbf.v4.new_code_cell("processed, decimal_diffs, sql_diffs = build.check_processed(q, web, social, ROOT)\nassert len(decimal_diffs) == len(sql_diffs) == 16\nassert max(decimal_diffs.values()) < 1e-10\nassert max(sql_diffs.values()) < 1e-10\npd.DataFrame({'Decimal max absolute difference': decimal_diffs, 'SQL max absolute difference': sql_diffs})"),
        nbf.v4.new_markdown_cell('SQL execution uses an in-memory SQLite compatibility adaptation of the actual maintained MySQL scripts: database/use commands are omitted, view replacement becomes view creation, and DOUBLE casts become REAL. Seeds, every validation query, views, all 16 derived fields and latest KPI query pass assertions. **Native MySQL precision, coercion, DDL and server execution are not certified.** Competitor numbers remain inherited historical snapshots; original captures are unavailable, so their provenance is unverified.'),
        nbf.v4.new_code_cell("start, end = processed.iloc[0], processed.iloc[-1]\nsummary = pd.DataFrame([\n    ['MAU',start.mau_m,end.mau_m,'million users',(end.mau_m/start.mau_m-1)*100,'percent growth'],\n    ['DAU',start.dau_m,end.dau_m,'million users',(end.dau_m/start.dau_m-1)*100,'percent growth'],\n    ['Paid subscribers',start.paid_subscribers_m,end.paid_subscribers_m,'million accounts',(end.paid_subscribers_m/start.paid_subscribers_m-1)*100,'percent growth'],\n    ['Quarterly revenue',start.revenue_usd_m,end.revenue_usd_m,'USD millions',(end.revenue_usd_m/start.revenue_usd_m-1)*100,'percent growth'],\n    ['DAU/MAU',start.dau_mau_ratio*100,end.dau_mau_ratio*100,'percent',(end.dau_mau_ratio-start.dau_mau_ratio)*100,'percentage-point increase']\n], columns=['Metric','Q1 2023','Q4 2025','Level unit','Change','Change unit'])\nsummary.round(3)"),
        nbf.v4.new_markdown_cell('## Growth diagnostics and operational interpretation\n\nDaily activity, paid accounts and revenue expanded faster than MAU across the fixed window. At Q4 2025 their YoY growth gaps versus MAU are **16.1, 14.4 and 20.9 pp**. These descriptive divergences support reviews of engagement and monetisation; they do not establish conversion, pricing effectiveness, retention or commercial efficiency. An authorised internal next step would audit existing measurement and investigate drivers with free-experience guardrails.'),
        nbf.v4.new_code_cell("fields = ['quarter','mau_yoy','dau_yoy','paid_subscribers_yoy','revenue_yoy','dau_yoy_minus_mau_yoy','paid_subscribers_yoy_minus_mau_yoy','revenue_yoy_minus_mau_yoy']\ndiagnostics = processed.loc[processed.mau_yoy.notna(), fields].copy()\ndiagnostics.iloc[:,1:] = diagnostics.iloc[:,1:]*100\ndiagnostics.columns = ['Quarter','MAU YoY (%)','DAU YoY (%)','Paid YoY (%)','Revenue YoY (%)','DAU minus MAU (pp)','Paid minus MAU (pp)','Revenue minus MAU (pp)']\nassert diagnostics.iloc[-1,1:].astype(float).round(1).tolist() == [14.1,30.1,28.4,35.0,16.1,14.4,20.9]\n# Use explicit half-up display rounding so 36.25% displays as 36.3%, consistent with SQL.\nfrom decimal import Decimal, ROUND_HALF_UP\nfor column in diagnostics.columns[1:]:\n    diagnostics[column] = diagnostics[column].map(lambda value: float(Decimal(str(value)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)))\ndiagnostics"),
    ]
    nb.metadata['kernelspec'] = {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
    # Pin the kernel process to the Python used for this build, avoiding a user's
    # unrelated global kernel and without installing a global kernelspec.
    client = NotebookClient(nb, timeout=120, kernel_name='python3')
    manager = client.create_kernel_manager()
    manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
    executed = client.execute(cwd=str(root / 'notebooks'))
    assert all(c.execution_count is not None and not any(o.output_type == 'error' for o in c.get('outputs', [])) for c in executed.cells if c.cell_type == 'code')
    nbf.write(executed, root / 'notebooks/duolingo_growth_analysis.ipynb')


def configure_plotting(cn_font_path=None):
    os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'duolingo-matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    candidates = ([cn_font_path] if cn_font_path else []) + [
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        'C:/Windows/Fonts/msyh.ttc']
    font = None
    for path in candidates:
        if path and Path(path).is_file():
            fm.fontManager.addfont(path)
            font = fm.FontProperties(fname=path).get_name()
            break
    if font is None:
        for name in ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS']:
            try:
                fm.findfont(name, fallback_to_default=False)
                font = name
                break
            except ValueError:
                continue
    if font is None:
        raise RuntimeError('A CJK font is required; supply --cn-font-path to a local font file.')
    plt.rcParams['axes.unicode_minus'] = False
    return plt, font


COLORS = {'green': '#2FB344', 'navy': '#172B4D', 'text': '#263238', 'muted': '#68737D',
          'grid': '#E7ECEF', 'bg': '#F7F9FA', 'white': '#FFFFFF', 'blue': '#3B82F6',
          'teal': '#14B8A6', 'orange': '#F59E0B', 'purple': '#8B5CF6'}


def build_dashboards(proc, web, social, root=ROOT, cn_font_path=None):
    plt, cn_font = configure_plotting(cn_font_path)
    from matplotlib.patches import FancyBboxPatch, Rectangle
    from matplotlib.font_manager import FontProperties
    from PIL import Image
    audit = []

    def box(ax, x, y, w, h):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.006,rounding_size=0.012',
                                   transform=ax.transAxes, facecolor='white', edgecolor=COLORS['grid'], linewidth=.8))

    def text(ax, x, y, value, size=9, color='text', bold=False, font='DejaVu Sans', **kwargs):
        return ax.text(x, y, value, transform=ax.transAxes, fontsize=size, color=COLORS[color],
                       fontname=font, fontweight='bold' if bold else 'normal', **kwargs)

    def bounded(ax, x, y, w, h, value, size, font, color='text', bold=False):
        # Token-aware wrapping uses actual glyph widths. Latin words/metric
        # abbreviations stay whole; CJK characters wrap without splitting DAU/MAU.
        renderer = ax.figure.canvas.get_renderer()
        fp = FontProperties(family=font, size=size, weight='bold' if bold else 'normal')
        max_width = w * ax.bbox.width
        tokens = re.findall(r'[+\-]?[A-Za-z0-9]+(?:[/.,+\-][A-Za-z0-9]+)*%?|\s+|[^A-Za-z0-9\s]', value)
        lines, line = [], ''
        for token in tokens:
            candidate = line + token
            width = renderer.get_text_width_height_descent(candidate.rstrip(), fp, False)[0]
            if line and width > max_width:
                lines.append(line.rstrip())
                line = token.lstrip()
            else:
                line = candidate
        if line.strip():
            lines.append(line.rstrip())
        artist = text(ax, x, y, '\n'.join(lines), size, color, bold, font, va='top', linespacing=1.28)
        ax.figure.canvas.draw()
        bbox = artist.get_window_extent(ax.figure.canvas.get_renderer())
        allowed = h * ax.bbox.height
        assert bbox.width <= max_width+2 and bbox.height <= allowed+2, f'Text exceeds panel: {value}'
        audit.append({'text': value, 'lines': len(lines), 'width_px': round(bbox.width, 1), 'height_px': round(bbox.height, 1)})
        return artist

    def axis(fig, rect, title, font):
        ax = fig.add_axes(rect)
        ax.set_facecolor('white')
        for s in ax.spines.values():
            s.set_visible(False)
        ax.grid(axis='y', color=COLORS['grid'], linewidth=.8, zorder=0)
        ax.tick_params(colors=COLORS['muted'], labelsize=8, length=0)
        ax.set_title(title, loc='left', fontsize=10.5, color=COLORS['navy'], fontweight='bold', fontname=font, pad=9)
        return ax

    def ticks(ax, frame, full=False):
        positions = list(range(len(frame))) if full else ([0, 3, 6, 9, 11] if len(frame) == 12 else list(range(len(frame))))
        ax.set_xticks(positions)
        ax.set_xticklabels(frame.quarter.iloc[positions], rotation=35 if full else 0, ha='right' if full else 'center')
        ax.margins(x=.035)

    def finish(fig, path, font, footer):
        ax0 = fig.axes[0]
        text(ax0, .035, .017, footer, 7.1, 'muted', font=font, va='center')
        for ax in fig.axes[1:]:
            for label in ax.get_xticklabels()+ax.get_yticklabels():
                label.set_fontname(font)
        fig.savefig(path, dpi=180, facecolor=fig.get_facecolor())
        plt.close(fig)
        with Image.open(path) as image:
            assert image.size == (2880, 1620)

    latest, first, prior = proc.iloc[-1], proc.iloc[0], proc.iloc[-5]
    x = np.arange(len(proc))
    yoy = proc.loc[proc.mau_yoy.notna()].reset_index(drop=True)
    xx = np.arange(len(yoy))
    for lang in ['en', 'cn']:
        en = lang == 'en'
        font = 'DejaVu Sans' if en else cn_font
        names = [('mau', 'MAU', 'blue'), ('dau', 'DAU', 'green'), ('paid_subscribers', 'Paid accounts' if en else '付费账户', 'purple'), ('revenue', 'Revenue' if en else '收入', 'orange')]
        footer = ('Sources: official Duolingo IR/SEC; ratio of reported averages. DAU/MAU is not retention; growth is descriptive.' if en else '来源：Duolingo IR / SEC 官方披露。DAU/MAU 为披露平均人数之比，不等同留存；增长关系为描述性分析。')
        fig = plt.figure(figsize=(16, 9), dpi=180, facecolor=COLORS['bg'])
        canvas = fig.add_axes([0, 0, 1, 1]); canvas.axis('off'); fig.canvas.draw()
        text(canvas, .035, .965, 'Growth & Monetisation Overview' if en else '增长与商业化概览', 23, 'navy', True, font, va='top')
        text(canvas, .035, .919, 'Q1 2023 – Q4 2025 | Analysis as of March 2026 | Cards: Q4 2025' if en else '2023 Q1–2025 Q4｜分析时点：2026年3月｜卡片数据：2025 Q4', 9.5, 'muted', font=font, va='top')
        text(canvas, .965, .95, 'DUOLINGO', 10, 'green', True, font, ha='right')
        cards = [('MAU' if en else '月活用户（MAU）', f'{latest.mau_m:.1f}M', f'+{latest.mau_yoy*100:.1f}%'),
                 ('DAU' if en else '日活用户（DAU）', f'{latest.dau_m:.1f}M', f'+{latest.dau_yoy*100:.1f}%'),
                 ('DAU / MAU', f'{latest.dau_mau_ratio*100:.1f}%', f'+{(latest.dau_mau_ratio-prior.dau_mau_ratio)*100:.1f} pp'),
                 ('Paid accounts' if en else '付费订阅账户', f'{latest.paid_subscribers_m:.1f}M', f'+{latest.paid_subscribers_yoy*100:.1f}%'),
                 ('Quarterly revenue' if en else '季度收入', f'${latest.revenue_usd_m:.1f}M', f'+{latest.revenue_yoy*100:.1f}%')]
        for i, (title, value, growth) in enumerate(cards):
            cx = .035 + i * .189
            box(canvas, cx, .782, .174, .104)
            text(canvas, cx+.009, .862, title, 9, 'muted', font=font, va='center')
            text(canvas, cx+.009, .824, value, 20, 'navy', True, font, va='center')
            text(canvas, cx+.009, .794, growth+(' YoY' if en else ' 同比'), 8.3, 'green', font=font)
        ax = axis(fig, [.045, .515, .43, .207], 'User Growth Trend' if en else '用户增长趋势', font)
        ax.plot(x, proc.mau_m, color=COLORS['blue'], lw=2, marker='o', ms=3, label='MAU')
        ax.plot(x, proc.dau_m, color=COLORS['green'], lw=2, marker='o', ms=3, label='DAU')
        ticks(ax, proc); ax.set_ylabel('Million users' if en else '百万用户', fontsize=8, color=COLORS['muted'], fontname=font)
        ax.legend(frameon=False, ncol=2, loc='upper left', prop={'family':font, 'size':8})
        ax = axis(fig, [.53, .515, .42, .207], 'Engagement Intensity (DAU / MAU)' if en else '用户活跃强度（DAU / MAU）', font)
        ax.plot(x, proc.dau_mau_ratio*100, color=COLORS['teal'], lw=2.2, marker='o', ms=3)
        ax.set_ylim(25, 42); ticks(ax, proc); ax.set_ylabel('%', fontsize=8, color=COLORS['muted'])
        ax.annotate(f'{latest.dau_mau_ratio*100:.1f}%', (11, latest.dau_mau_ratio*100), (9.2, 40.8), color=COLORS['teal'], fontsize=9, fontname=font, arrowprops={'arrowstyle':'-', 'color':COLORS['teal']})
        for rect, field, title, color, unit in [([.045,.277,.205,.158], 'paid_subscribers_m', 'Paid accounts' if en else '付费订阅账户', 'purple', 'M'), ([.285,.277,.205,.158], 'revenue_usd_m', 'Quarterly revenue' if en else '季度收入', 'orange', 'USD M')]:
            ax = axis(fig, rect, title, font)
            ax.plot(x, proc[field], color=COLORS[color], lw=2, marker='o', ms=2.5); ticks(ax, proc)
            ax.set_ylabel(unit, fontsize=8, color=COLORS['muted'], fontname=font)
        ax = axis(fig, [.53,.277,.42,.158], 'YoY Growth Comparison' if en else '同比增长对比', font)
        for stem, label, color in names:
            ax.plot(xx, yoy[stem+'_yoy']*100, color=COLORS[color], lw=1.7, marker='o', ms=2.5, label=label)
        ticks(ax, yoy, True); ax.set_ylabel('%', fontsize=8, color=COLORS['muted'])
        ax.legend(frameon=False, ncol=4, loc='upper right', prop={'family':font, 'size':7})
        box(canvas, .035, .052, .93, .151)
        text(canvas, .055, .179, 'Key Growth Insights' if en else '关键增长洞察', 11, 'navy', True, font)
        insights = (['DAU grew 160% versus MAU 83% from Q1 2023 to Q4 2025. DAU/MAU increased from 28.0% to 39.6% (+11.6 pp).', 'Paid accounts grew 154% and quarterly revenue 145% over the same period, both ahead of audience growth.', 'Q4 2025 MAU grew 14% YoY; DAU, paid accounts and revenue grew 30%, 28% and 35%. These are aggregate observations.'] if en else ['2023 Q1 至 2025 Q4，DAU 增长160%，MAU 增长83%；DAU/MAU 从28.0%升至39.6%（+11.6个百分点）。', '同期付费订阅账户增长154%，季度收入增长145%，均高于用户规模增速。', '2025 Q4，MAU 同比增长14%；DAU、付费账户与收入增长30%、28%和35%。这些是汇总数据观察。'])
        for i, value in enumerate(insights):
            cx = .055 + i*.304
            text(canvas, cx, .145, f'0{i+1}', 9, 'green', True, font)
            bounded(canvas, cx+.024, .148, .265, .083, value, 8.3, font)
        path = root / ('dashboard/english/dashboard_page1_growth_monetisation.png' if en else 'dashboard/chinese/dashboard_page1_growth_monetisation_cn.png')
        finish(fig, path, font, footer)

        fig = plt.figure(figsize=(16, 9), dpi=180, facecolor=COLORS['bg'])
        canvas = fig.add_axes([0,0,1,1]); canvas.axis('off'); fig.canvas.draw()
        text(canvas, .035, .965, 'Growth Diagnostics & Strategic Context' if en else '增长质量诊断与战略背景', 23, 'navy', True, font, va='top')
        text(canvas, .035, .919, 'Corporate: Q1 2023–Q4 2025 | Website: February 2026 | Social: March 2026' if en else '公司趋势：2023 Q1–2025 Q4｜网站：2026年2月｜社媒：2026年3月', 9.5, 'muted', font=font, va='top')
        text(canvas, .965, .95, 'DUOLINGO', 10, 'green', True, font, ha='right')
        ax = axis(fig, [.045,.577,.56,.266], 'Indexed Growth (Q1 2023 = 100)' if en else '指数化增长（2023 Q1 = 100）', font)
        for stem, label, color in names:
            ax.plot(x, proc[stem+'_index'], color=COLORS[color], lw=2, marker='o', ms=2.8, label=label)
        ticks(ax, proc); ax.set_ylabel('Index' if en else '指数', fontsize=8, color=COLORS['muted'], fontname=font)
        ax.legend(frameon=False, ncol=4, loc='upper left', prop={'family':font, 'size':8})
        box(canvas, .64,.565,.325,.288)
        text(canvas, .66,.818, 'Q4 2025 growth gaps' if en else '2025 Q4 增长差', 11, 'navy', True, font)
        text(canvas, .66,.785, 'YoY growth minus MAU YoY growth' if en else '各指标同比增速减去 MAU 同比增速', 8.1, 'muted', font=font)
        for i, (stem, label, color) in enumerate(names[1:]):
            yy = .737-i*.045
            text(canvas, .66, yy, label, 9, 'muted', font=font)
            text(canvas, .935, yy, f'+{latest[stem+"_yoy_minus_mau_yoy"]*100:.1f} pp', 11, color, True, font, ha='right')
        bounded(canvas, .66,.608,.285,.045, 'Divergences identify questions to investigate; they do not establish conversion or pricing effects.' if en else '增速差可帮助提出调查问题，但不能证明转化或定价效果。', 8, font)
        ax = axis(fig, [.045,.321,.29,.177], 'Engagement Growth Gap' if en else '活跃增长差', font)
        ax.bar(xx, yoy.dau_yoy_minus_mau_yoy*100, color=COLORS['teal'], width=.65, zorder=3)
        ax.axhline(0, color=COLORS['muted'], lw=.7); ticks(ax, yoy, True)
        ax.set_ylabel('DAU YoY − MAU YoY (pp)' if en else 'DAU同比 − MAU同比（百分点）', fontsize=7.8, color=COLORS['muted'], fontname=font)
        ax = axis(fig, [.385,.321,.275,.177], 'Monetisation Growth Gaps' if en else '商业化增长差', font)
        ax.bar(xx-.18, yoy.paid_subscribers_yoy_minus_mau_yoy*100, width=.34, color=COLORS['purple'], label='Paid − MAU' if en else '付费 − MAU', zorder=3)
        ax.bar(xx+.18, yoy.revenue_yoy_minus_mau_yoy*100, width=.34, color=COLORS['orange'], label='Revenue − MAU' if en else '收入 − MAU', zorder=3)
        ax.axhline(0, color=COLORS['muted'], lw=.7); ticks(ax, yoy, True)
        ax.set_ylabel('YoY gap (pp)' if en else '同比增速差（百分点）', fontsize=8, color=COLORS['muted'], fontname=font)
        ax.legend(frameon=False, ncol=2, loc='upper left', prop={'family':font, 'size':7})
        box(canvas, .697,.273,.268,.25)
        text(canvas, .711,.494, 'Competitive Digital Snapshot' if en else '数字竞争表现快照', 10.3, 'navy', True, font)
        text(canvas, .711,.467, 'Website visits: Feb 2026' if en else '网站访问量：2026年2月', 7.8, 'muted', font=font)
        for i, r in web.iterrows():
            yy=.432-i*.031
            text(canvas, .711, yy, r.brand, 7.7, font=font)
            canvas.add_patch(Rectangle((.777,yy-.004), .125*r.total_visits_m/web.total_visits_m.max(), .01, transform=canvas.transAxes, facecolor=COLORS['green'] if r.brand=='Duolingo' else '#BEC9D2', edgecolor='none'))
            text(canvas, .946, yy, f'{r.total_visits_m:.1f}M', 7.7, 'muted', font=font, ha='right')
        duolingo = social.set_index(['brand','platform']).followers
        social_text = (f'Duolingo social (Mar): TikTok {duolingo["Duolingo","TikTok"]/1e6:.1f}M; YouTube {duolingo["Duolingo","YouTube"]/1e6:.2f}M; Instagram {duolingo["Duolingo","Instagram"]/1e6:.1f}M. Leads both peers on each platform.' if en else 'Duolingo社媒（3月）：TikTok 17.0M，YouTube 6.61M，Instagram 4.8M；各平台均领先两家竞品。')
        bounded(canvas,.711,.338,.235,.058,social_text,7.3,font)
        bounded(canvas,.711,.285,.235,.027,'Historical captures unavailable; snapshot provenance unverified.' if en else '原始历史截图缺失；快照来源尚未核验。',6.8,font,'muted')
        box(canvas,.035,.056,.93,.17)
        text(canvas,.055,.198,'Operational Priorities' if en else '运营重点',11,'navy',True,font)
        priorities = ([('Monitor engagement','Review DAU/MAU alongside authorised cohort and re-engagement measures; aggregate intensity cannot show retention.'),('Investigate monetisation drivers','Review paid/revenue divergences with internal plan and journey data. Evaluate premium value with free-experience guardrails.'),('Audit existing measurement','Use authorised internal data to assess premium exposure, trials and paid conversion before selecting experiments.')] if en else [('监控活跃表现','结合获授权的用户群及召回指标审视 DAU/MAU；汇总活跃强度不能反映留存。'),('调查商业化驱动因素','用内部套餐和用户路径数据审视付费及收入增速差；评估会员价值并守住免费体验。'),('审视现有测量体系','使用获授权的内部数据检查会员曝光、试用及付费转化，再选择实验。')])
        for i,(head,body) in enumerate(priorities):
            cx=.055+i*.304
            text(canvas,cx,.162,f'0{i+1}',9,'green',True,font)
            bounded(canvas,cx+.024,.166,.265,.035,head,9,font,'navy',True)
            bounded(canvas,cx+.024,.131,.265,.066,body,7.9,font)
        footer2 = ('Sources: Duolingo IR/SEC; inherited Feb/Mar 2026 competitor snapshots (unverified). pp = percentage points; context, not market share.' if en else '来源：Duolingo IR / SEC；继承的2026年2–3月竞品快照（未核验）。pp = 百分点；竞品数据仅作背景，不代表市场份额。')
        path = root / ('dashboard/english/dashboard_page2_growth_diagnostics.png' if en else 'dashboard/chinese/dashboard_page2_growth_diagnostics_cn.png')
        finish(fig,path,font,footer2)
    copies = [('english/dashboard_page1_growth_monetisation.png','EN_Page1_Growth_Monetisation.png'), ('english/dashboard_page2_growth_diagnostics.png','EN_Page2_Growth_Diagnostics.png'), ('chinese/dashboard_page1_growth_monetisation_cn.png','CN_Page1_Growth_Monetisation.png'), ('chinese/dashboard_page2_growth_diagnostics_cn.png','CN_Page2_Growth_Diagnostics.png')]
    for source,destination in copies:
        shutil.copyfile(root/'dashboard'/source,root/'dashboard/screenshots'/destination)
        assert (root/'dashboard'/source).read_bytes() == (root/'dashboard/screenshots'/destination).read_bytes()
    return audit


def protected_hashes(root):
    paths = list((root/'data/raw').glob('*.csv')) + list((root/'sql').glob('*.sql')) + list((root/'docs').glob('*')) + list(root.glob('*.md')) + list((root/'case_study').glob('*'))
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only',action='store_true',help='Read-only verification of existing processed data and actual SQL')
    parser.add_argument('--only',choices=['all','dashboards','notebook'],default='all',help='Rebuild one output family when the other is already verified')
    parser.add_argument('--cn-font-path',help='Local font file supporting Chinese glyphs')
    parser.add_argument('--qa-json',type=Path,help='Optional machine-readable build evidence (use a temporary path)')
    args=parser.parse_args()
    before=protected_hashes(ROOT)
    if args.qa_json:
        assert args.qa_json.suffix == '.json' and str(args.qa_json.resolve()) not in before, 'QA output must not replace a protected input'
    q,web,social=load_inputs()
    text_audit=[]
    regenerated=[]
    if not args.check_only:
        proc=derive(q)
        # Validate logic first; retain already-correct processed files verbatim.
        decimal_check(q,proc);sql_check(q,web,social,proc)
        outputs=[('quarterly_dashboard',proc,['quarter']),
                 ('competitor_web_snapshot',web,['brand']),
                 ('social_snapshot',social,['brand','platform']),
                 ('tableau_quarterly_long',make_long(proc),['quarter','metric'])]
        for name,expected,keys in outputs:
            path=ROOT/f'data/processed/{name}.csv'
            try:
                actual=pd.read_csv(path,parse_dates=['period_end'] if name=='quarterly_dashboard' else None)
                assert actual.columns.tolist()==expected.columns.tolist()
                compare_frames(actual,expected,keys,[c for c in expected if c not in keys])
            except (FileNotFoundError,pd.errors.EmptyDataError,pd.errors.ParserError,AssertionError,ValueError,KeyError):
                expected.to_csv(path,index=False)
                regenerated.append(name)
    proc,decimal_diffs,sql_diffs=check_processed(q,web,social)
    if not args.check_only:
        if args.only in ['all','notebook']:
            build_notebook()
        if args.only in ['all','dashboards']:
            text_audit=build_dashboards(proc,web,social,cn_font_path=args.cn_font_path)
    assert protected_hashes(ROOT)==before, 'A protected input changed during the build'
    evidence={'status':'PASS','corporate_quarters':12,'website_rows':3,'social_rows':9,'derived_fields':16,'long_rows':156,'decimal_max_absolute_difference':max(decimal_diffs.values()),'sql_max_absolute_difference':max(sql_diffs.values()),'sql_engine':sqlite3.sqlite_version,'native_mysql_tested':False,'protected_inputs_unchanged':True,'processed_outputs_regenerated':regenerated,'bounded_dashboard_text_blocks':len(text_audit),'python':sys.executable,'mode':'check-only' if args.check_only else 'build','output_family':args.only,'notebook_executed':not args.check_only and args.only in ['all','notebook']}
    if args.qa_json:
        args.qa_json.write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence,indent=2))


if __name__=='__main__':
    main()
