from __future__ import annotations
from pathlib import Path
from .io import REPO_ROOT, utc_now

def write_daily_report(snapshot: dict) -> Path:
    day = utc_now()[:10].replace("-", "")
    out = REPO_ROOT / "reports/ipo/spacex" / f"spacex_daily_{day}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    scores = snapshot.get("scores", {})
    lines = ["# SpaceX / SPCX Daily Super Desk Report", "", f"Generated: {utc_now()}", "", "## Market", "", f"- Symbol: {snapshot.get('symbol')}", f"- Price: {snapshot.get('price')}", f"- IPO price: {snapshot.get('ipo_price')}", f"- Gap vs IPO: {snapshot.get('gap_vs_ipo_pct')}", "", "## Scores", ""]
    for k, v in scores.items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Signals", ""] + [f"- {s}" for s in snapshot.get("signals", [])]
    lines += ["", "## Next actions", "", "- Validate TradingView real alert feed.", "- Validate Bot Vision SPCX profile.", "- Accumulate OHLCV for backtests.", "- Keep monitor-only."]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out

def write_ui(snapshot: dict) -> Path:
    ui = REPO_ROOT / "ui/spacex_desk/legacy_snapshot.html"
    ui.parent.mkdir(parents=True, exist_ok=True)
    scores = snapshot.get("scores", {})
    cards = "".join(f'<div class="card"><b>{k}</b><span>{v}</span></div>' for k, v in scores.items())
    signals = "".join(f"<li>{s}</li>" for s in snapshot.get("signals", []))
    html = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>SPCX Super Desk</title>
<style>
body{{font-family:Arial;margin:24px;background:#0b0d12;color:#e8eef7}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}}
.card{{background:#151a24;border:1px solid #2a3345;border-radius:10px;padding:14px}}
.card span{{display:block;font-size:28px;margin-top:8px}}
code{{color:#a8c7ff}}
</style></head>
<body>
<h1>SpaceX / SPCX Super Desk</h1>
<p>Monitor-only. Last update: <code>{snapshot.get('written_at','')}</code></p>
<h2>Market</h2>
<div class="grid"><div class="card"><b>Price</b><span>{snapshot.get('price')}</span></div><div class="card"><b>Gap IPO %</b><span>{snapshot.get('gap_vs_ipo_pct')}</span></div><div class="card"><b>RelVol</b><span>{snapshot.get('relative_volume_estimate')}</span></div></div>
<h2>Scores</h2><div class="grid">{cards}</div>
<h2>Signals</h2><ul>{signals}</ul>
</body></html>"""
    ui.write_text(html, encoding="utf-8")
    return ui
