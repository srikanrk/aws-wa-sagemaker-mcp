# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""HTML report generator for Well-Architected validation results."""

import datetime
import html
import os


PILLAR_ORDER = [
    'Security',
    'Reliability',
    'Operational Excellence',
    'Performance Efficiency',
    'Cost Optimization',
    'Sustainability',
]

PILLAR_ICONS = {
    'Security': '🔒',
    'Reliability': '🛡️',
    'Operational Excellence': '⚙️',
    'Performance Efficiency': '⚡',
    'Cost Optimization': '💰',
    'Sustainability': '🌱',
}

PILLAR_COLORS = {
    'Security': '#e53935',
    'Reliability': '#8e24aa',
    'Operational Excellence': '#1e88e5',
    'Performance Efficiency': '#f9a825',
    'Cost Optimization': '#43a047',
    'Sustainability': '#00897b',
}


def generate_html_report(
    resource_name: str,
    resource_type: str,
    findings: list[dict],
    summary: dict,
    report_path: str | None = None,
    account_id: str | None = None,
    region: str | None = None,
) -> str:
    """Generate an HTML report for single-resource validation findings.

    Args:
        resource_name: Name of the validated resource
        resource_type: Type of the resource
        findings: List of finding dictionaries
        summary: Summary dict mapping pillar names to severity counts
        report_path: Optional path to write the report.
        account_id: AWS account ID
        region: AWS region name

    Returns:
        Absolute path to the generated HTML report file
    """
    return _build_report(
        title=f'{resource_type} — {resource_name}',
        resources=[f'{resource_type}/{resource_name}'],
        findings=findings,
        report_path=report_path,
        account_id=account_id,
        region=region,
    )


def generate_batch_html_report(
    resources_validated: list[str],
    findings: list[dict],
    summary: dict,
    report_path: str | None = None,
    account_id: str | None = None,
    region: str | None = None,
) -> str:
    """Generate an HTML report for batch validation findings.

    Args:
        resources_validated: List of validated resource names
        findings: List of all finding dictionaries
        summary: Aggregated summary dict
        report_path: Optional path to write the report.
        account_id: AWS account ID
        region: AWS region name

    Returns:
        Absolute path to the generated HTML report file
    """
    return _build_report(
        title=f'{len(resources_validated)} Resources',
        resources=resources_validated,
        findings=findings,
        report_path=report_path,
        account_id=account_id,
        region=region,
    )


def _build_report(
    title: str,
    resources: list[str],
    findings: list[dict],
    report_path: str | None = None,
    account_id: str | None = None,
    region: str | None = None,
) -> str:
    """Build the complete HTML report.

    Args:
        title: Report title
        resources: List of resource identifiers
        findings: List of finding dicts
        report_path: Output file path
        account_id: AWS account ID
        region: AWS region name

    Returns:
        Absolute path to the generated HTML file
    """
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%B %d, %Y at %H:%M UTC')
    total = len(findings)
    high = sum(1 for f in findings if f['severity'] == 'HIGH')
    med = sum(1 for f in findings if f['severity'] == 'MEDIUM')
    low = sum(1 for f in findings if f['severity'] == 'LOW')

    by_pillar: dict[str, list[dict]] = {}
    for f in findings:
        by_pillar.setdefault(f['pillar'], []).append(f)

    by_resource: dict[str, list[dict]] = {}
    for f in findings:
        by_resource.setdefault(f['resource'], []).append(f)

    parts = [
        _css(),
        _header(title, ts, len(resources), account_id, region),
        _score_ring(high, med, low, total),
        _severity_cards(high, med, low, total),
        _pillar_heatmap(by_pillar),
    ]

    if len(resources) > 1:
        parts.append(_resource_table(by_resource))

    for pillar in PILLAR_ORDER:
        if pillar in by_pillar:
            parts.append(_pillar_section(pillar, by_pillar[pillar]))

    parts.append(_footer(ts))

    content = '\n'.join(parts)

    if report_path is None:
        report_path = 'wa-report.html'

    with open(report_path, 'w', encoding='utf-8') as fh:
        fh.write(content)

    return os.path.abspath(report_path)


def _css() -> str:
    """Generate the HTML head with dark theme CSS."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SageMaker Well-Architected Operational Review</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#232733;--surface3:#2c3040;
  --border:#333849;--text:#e4e7ef;--text2:#9ca3b8;--text3:#6b7280;
  --high:#ef4444;--high-bg:rgba(239,68,68,.12);
  --med:#f59e0b;--med-bg:rgba(245,158,11,.12);
  --low:#3b82f6;--low-bg:rgba(59,130,246,.12);
  --pass:#22c55e;--pass-bg:rgba(34,197,94,.12);
  --accent:#818cf8;--accent-bg:rgba(129,140,248,.08);
  --radius:12px;--radius-sm:8px;
}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',sans-serif;
  background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh;
}
.container{max-width:1280px;margin:0 auto;padding:32px 24px}
.header{
  background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#3730a3 100%);
  border-radius:var(--radius);padding:40px;margin-bottom:28px;
  position:relative;overflow:hidden;
}
.header::before{
  content:'';position:absolute;top:-50%;right:-20%;width:400px;height:400px;
  background:radial-gradient(circle,rgba(129,140,248,.15) 0%,transparent 70%);
}
.header h1{font-size:28px;font-weight:700;letter-spacing:-.5px;margin-bottom:8px;position:relative;color:#fff}
.header .meta{color:rgba(255,255,255,.7);font-size:14px;position:relative;display:flex;flex-wrap:wrap;gap:6px}
.header .meta span{
  display:inline-block;background:rgba(255,255,255,.1);padding:3px 12px;
  border-radius:20px;font-size:12px;
}
.score-section{display:flex;align-items:center;gap:32px;margin-bottom:28px;
  background:var(--surface);border-radius:var(--radius);padding:32px;border:1px solid var(--border)}
.ring-container{position:relative;width:140px;height:140px;flex-shrink:0}
.ring-container svg{transform:rotate(-90deg)}
.ring-label{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center}
.ring-label .number{font-size:36px;font-weight:800;line-height:1}
.ring-label .sub{font-size:12px;color:var(--text2);margin-top:2px}
.sev-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px}
.sev-card{
  background:var(--surface);border-radius:var(--radius);padding:20px 24px;
  border:1px solid var(--border);position:relative;overflow:hidden;
}
.sev-card::after{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.sev-card.high::after{background:var(--high)}
.sev-card.med::after{background:var(--med)}
.sev-card.low::after{background:var(--low)}
.sev-card.total::after{background:var(--accent)}
.sev-card .val{font-size:32px;font-weight:800;line-height:1.2}
.sev-card .lbl{font-size:12px;color:var(--text2);text-transform:uppercase;letter-spacing:1px;margin-top:4px}
.sev-card.high .val{color:var(--high)}
.sev-card.med .val{color:var(--med)}
.sev-card.low .val{color:var(--low)}
.sev-card.total .val{color:var(--accent)}
.heatmap{background:var(--surface);border-radius:var(--radius);padding:28px;border:1px solid var(--border);margin-bottom:28px}
.heatmap h2{font-size:18px;font-weight:600;margin-bottom:20px}
.heatmap-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}
.hm-cell{background:var(--surface2);border-radius:var(--radius-sm);padding:16px;text-align:center;border:1px solid var(--border);transition:transform .15s,box-shadow .15s}
.hm-cell:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.3)}
.hm-cell .icon{font-size:28px;margin-bottom:8px}
.hm-cell .name{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px;line-height:1.3}
.hm-cell .counts{display:flex;justify-content:center;gap:6px}
.hm-cell .dot{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;font-size:12px;font-weight:700}
.dot.h{background:var(--high-bg);color:var(--high)}
.dot.m{background:var(--med-bg);color:var(--med)}
.dot.l{background:var(--low-bg);color:var(--low)}
.dot.zero{opacity:.3}
.res-table{background:var(--surface);border-radius:var(--radius);border:1px solid var(--border);margin-bottom:28px;overflow:hidden}
.res-table h2{font-size:18px;font-weight:600;padding:20px 24px;border-bottom:1px solid var(--border)}
.res-table table{width:100%;border-collapse:collapse}
.res-table th{text-align:left;padding:10px 24px;font-size:11px;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;background:var(--surface2);border-bottom:1px solid var(--border)}
.res-table td{padding:12px 24px;border-bottom:1px solid var(--border);font-size:14px}
.res-table tr:last-child td{border-bottom:none}
.res-table tr:hover td{background:var(--surface2)}
.res-name{font-family:'SF Mono',SFMono-Regular,Consolas,monospace;font-size:13px}
.pillar{background:var(--surface);border-radius:var(--radius);border:1px solid var(--border);margin-bottom:20px;overflow:hidden}
.pillar-head{padding:20px 24px;display:flex;align-items:center;gap:14px;border-bottom:1px solid var(--border)}
.pillar-head:hover{background:var(--surface2)}
.pillar-head .pill-icon{font-size:24px}
.pillar-head .pill-name{font-size:16px;font-weight:600;flex:1}
.pillar-head .pill-count{font-size:13px;color:var(--text2);background:var(--surface3);padding:4px 12px;border-radius:20px}
.pillar-head .pill-bar{width:120px;height:6px;background:var(--surface3);border-radius:3px;overflow:hidden;display:flex}
.pillar-head .pill-bar span{height:100%}
.pillar table{width:100%;border-collapse:collapse}
.pillar th{text-align:left;padding:10px 24px;font-size:11px;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;background:var(--surface2);border-bottom:1px solid var(--border)}
.pillar td{padding:14px 24px;border-bottom:1px solid var(--border);font-size:14px;vertical-align:top}
.pillar tr:last-child td{border-bottom:none}
.pillar tr:hover td{background:rgba(255,255,255,.02)}
.badge{display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:700;letter-spacing:.5px}
.badge-HIGH{background:var(--high-bg);color:var(--high)}
.badge-MEDIUM{background:var(--med-bg);color:var(--med)}
.badge-LOW{background:var(--low-bg);color:var(--low)}
.check-id{font-family:'SF Mono',SFMono-Regular,Consolas,monospace;font-size:12px;color:var(--accent);background:var(--accent-bg);padding:2px 8px;border-radius:4px}
.detail{color:var(--text);line-height:1.5}
.rec{margin-top:6px;font-size:13px;color:var(--text2);padding-left:16px;border-left:2px solid var(--border)}
.resource-tag{font-size:12px;color:var(--text3);font-family:'SF Mono',SFMono-Regular,Consolas,monospace}
.footer{text-align:center;padding:24px;color:var(--text3);font-size:12px;border-top:1px solid var(--border);margin-top:12px}
@media(max-width:900px){
  .heatmap-grid{grid-template-columns:repeat(3,1fr)}
  .sev-cards{grid-template-columns:repeat(2,1fr)}
  .score-section{flex-direction:column;text-align:center}
}
@media(max-width:600px){
  .heatmap-grid{grid-template-columns:repeat(2,1fr)}
  .sev-cards{grid-template-columns:1fr 1fr}
  .container{padding:16px}
}
</style>
</head>
<body>
<div class="container">"""


def _header(
    title: str, ts: str, resource_count: int, account_id: str | None, region: str | None
) -> str:
    """Generate the HTML header section."""
    account_badge = f'<span>🏢 Account: {html.escape(account_id)}</span>' if account_id else ''
    region_badge = f'<span>🌍 Region: {html.escape(region)}</span>' if region else ''
    return f"""<div class="header">
  <h1>SageMaker Well-Architected Report</h1>
  <p class="meta">
    {account_badge}
    {region_badge}
    <span>📦 {resource_count} resource{'s' if resource_count != 1 else ''} scanned</span>
    <span>🕐 {ts}</span>
  </p>
</div>"""


def _score_ring(high: int, med: int, low: int, total: int) -> str:
    """Generate the SVG donut chart section."""
    if total == 0:
        return ''
    r = 58
    circ = 2 * 3.14159 * r
    h_pct = high / total if total else 0
    m_pct = med / total if total else 0
    l_pct = low / total if total else 0
    h_len = circ * h_pct
    m_len = circ * m_pct
    l_len = circ * l_pct
    h_off = 0
    m_off = h_len
    l_off = h_len + m_len

    if high == 0 and med == 0:
        grade, grade_color = 'Excellent', 'var(--pass)'
    elif high == 0 and med <= 3:
        grade, grade_color = 'Good', 'var(--low)'
    elif high <= 2:
        grade, grade_color = 'Fair', 'var(--med)'
    else:
        grade, grade_color = 'Needs Work', 'var(--high)'

    return f"""<div class="score-section">
  <div class="ring-container">
    <svg width="140" height="140" viewBox="0 0 140 140">
      <circle cx="70" cy="70" r="{r}" fill="none" stroke="var(--surface3)" stroke-width="12"/>
      <circle cx="70" cy="70" r="{r}" fill="none" stroke="var(--low)" stroke-width="12"
        stroke-dasharray="{l_len:.1f} {circ:.1f}" stroke-dashoffset="-{l_off:.1f}" stroke-linecap="round"/>
      <circle cx="70" cy="70" r="{r}" fill="none" stroke="var(--med)" stroke-width="12"
        stroke-dasharray="{m_len:.1f} {circ:.1f}" stroke-dashoffset="-{m_off:.1f}" stroke-linecap="round"/>
      <circle cx="70" cy="70" r="{r}" fill="none" stroke="var(--high)" stroke-width="12"
        stroke-dasharray="{h_len:.1f} {circ:.1f}" stroke-dashoffset="-{h_off:.1f}" stroke-linecap="round"/>
    </svg>
    <div class="ring-label">
      <div class="number">{total}</div>
      <div class="sub">findings</div>
    </div>
  </div>
  <div>
    <div style="font-size:14px;color:var(--text2);margin-bottom:4px">Overall Health</div>
    <div style="font-size:28px;font-weight:800;color:{grade_color};margin-bottom:8px">{grade}</div>
    <div style="font-size:13px;color:var(--text3);line-height:1.6">
      {high} critical issue{'s' if high != 1 else ''} requiring immediate attention<br>
      {med} improvement{'s' if med != 1 else ''} recommended<br>
      {low} informational suggestion{'s' if low != 1 else ''}
    </div>
  </div>
</div>"""


def _severity_cards(high: int, med: int, low: int, total: int) -> str:
    """Generate severity summary cards."""
    return f"""<div class="sev-cards">
  <div class="sev-card total"><div class="val">{total}</div><div class="lbl">Total Findings</div></div>
  <div class="sev-card high"><div class="val">{high}</div><div class="lbl">High Severity</div></div>
  <div class="sev-card med"><div class="val">{med}</div><div class="lbl">Medium Severity</div></div>
  <div class="sev-card low"><div class="val">{low}</div><div class="lbl">Low Severity</div></div>
</div>"""


def _pillar_heatmap(by_pillar: dict[str, list[dict]]) -> str:
    """Generate pillar heatmap grid."""
    cells = []
    for pillar in PILLAR_ORDER:
        findings = by_pillar.get(pillar, [])
        icon = PILLAR_ICONS.get(pillar, '📋')
        h = sum(1 for f in findings if f['severity'] == 'HIGH')
        m = sum(1 for f in findings if f['severity'] == 'MEDIUM')
        lo = sum(1 for f in findings if f['severity'] == 'LOW')
        h_cls = 'zero' if h == 0 else ''
        m_cls = 'zero' if m == 0 else ''
        l_cls = 'zero' if lo == 0 else ''
        cells.append(f"""<div class="hm-cell">
      <div class="icon">{icon}</div>
      <div class="name">{html.escape(pillar)}</div>
      <div class="counts">
        <span class="dot h {h_cls}">{h}</span>
        <span class="dot m {m_cls}">{m}</span>
        <span class="dot l {l_cls}">{lo}</span>
      </div>
    </div>""")
    return f"""<div class="heatmap">
  <h2>Findings by Pillar</h2>
  <div style="display:flex;gap:12px;margin-bottom:16px;font-size:12px;color:var(--text3)">
    <span><span class="dot h" style="width:16px;height:16px;font-size:9px;vertical-align:middle">H</span> High</span>
    <span><span class="dot m" style="width:16px;height:16px;font-size:9px;vertical-align:middle">M</span> Medium</span>
    <span><span class="dot l" style="width:16px;height:16px;font-size:9px;vertical-align:middle">L</span> Low</span>
  </div>
  <div class="heatmap-grid">{''.join(cells)}</div>
</div>"""


def _resource_table(by_resource: dict[str, list[dict]]) -> str:
    """Generate the findings-by-resource table."""
    rows = []
    sorted_res = sorted(
        by_resource.items(),
        key=lambda x: sum(1 for f in x[1] if f['severity'] == 'HIGH'),
        reverse=True,
    )
    for res_name, findings in sorted_res:
        h = sum(1 for f in findings if f['severity'] == 'HIGH')
        m = sum(1 for f in findings if f['severity'] == 'MEDIUM')
        lo = sum(1 for f in findings if f['severity'] == 'LOW')
        total = len(findings)
        bar_w = min(total * 4, 120)
        h_w = int(bar_w * h / total) if total else 0
        m_w = int(bar_w * m / total) if total else 0
        l_w = bar_w - h_w - m_w
        rows.append(f"""<tr>
      <td><span class="res-name">{html.escape(res_name)}</span></td>
      <td>{total}</td>
      <td style="color:var(--high);font-weight:600">{h}</td>
      <td style="color:var(--med);font-weight:600">{m}</td>
      <td style="color:var(--low);font-weight:600">{lo}</td>
      <td>
        <div style="display:flex;height:8px;border-radius:4px;overflow:hidden;width:{bar_w}px;background:var(--surface3)">
          <div style="width:{h_w}px;background:var(--high)"></div>
          <div style="width:{m_w}px;background:var(--med)"></div>
          <div style="width:{l_w}px;background:var(--low)"></div>
        </div>
      </td>
    </tr>""")
    return f"""<div class="res-table">
  <h2>Findings by Resource</h2>
  <table>
    <thead><tr><th>Resource</th><th>Total</th><th>High</th><th>Medium</th><th>Low</th><th>Distribution</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</div>"""


def _pillar_section(pillar: str, findings: list[dict]) -> str:
    """Generate a pillar findings section with table."""
    icon = PILLAR_ICONS.get(pillar, '📋')
    color = PILLAR_COLORS.get(pillar, '#888')
    total = len(findings)
    h = sum(1 for f in findings if f['severity'] == 'HIGH')
    m = sum(1 for f in findings if f['severity'] == 'MEDIUM')
    lo = sum(1 for f in findings if f['severity'] == 'LOW')
    bar_total = max(total, 1)
    h_pct = h / bar_total * 100
    m_pct = m / bar_total * 100
    l_pct = lo / bar_total * 100

    sev_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    sorted_findings = sorted(findings, key=lambda f: sev_order.get(f['severity'], 3))

    rows = []
    for f in sorted_findings:
        sev = f['severity']
        rows.append(f"""<tr>
      <td><span class="badge badge-{sev}">{sev}</span></td>
      <td><span class="check-id">{html.escape(f.get('check', ''))}</span></td>
      <td><span class="resource-tag">{html.escape(f.get('resource', ''))}</span></td>
      <td>
        <div class="detail">{html.escape(f.get('detail', ''))}</div>
        <div class="rec">💡 {html.escape(f.get('recommendation', ''))}</div>
      </td>
    </tr>""")

    return f"""<div class="pillar">
  <div class="pillar-head" style="border-left:4px solid {color}">
    <span class="pill-icon">{icon}</span>
    <span class="pill-name">{html.escape(pillar)}</span>
    <span class="pill-count">{total} finding{'s' if total != 1 else ''}</span>
    <div class="pill-bar">
      <span style="width:{h_pct:.0f}%;background:var(--high)"></span>
      <span style="width:{m_pct:.0f}%;background:var(--med)"></span>
      <span style="width:{l_pct:.0f}%;background:var(--low)"></span>
    </div>
  </div>
  <table>
    <thead><tr><th style="width:90px">Severity</th><th style="width:180px">Check</th><th style="width:180px">Resource</th><th>Detail &amp; Recommendation</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</div>"""


def _footer(ts: str) -> str:
    """Generate the HTML footer."""
    return f"""</div>
<div class="footer">
  Generated by Amazon SageMaker Well-Architected MCP Server &middot; {ts}
</div>
</body>
</html>"""
