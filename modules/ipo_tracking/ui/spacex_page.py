from __future__ import annotations

import html
import json
from pathlib import Path

from modules.ipo_tracking.config import load_config, resolve_paths


def render_static_page(config_path: str | None = None) -> str:
    paths = resolve_paths(load_config(config_path))
    snapshot = {}
    if paths.latest_snapshot.exists():
        snapshot = json.loads(paths.latest_snapshot.read_text(encoding="utf-8"))
    scores = snapshot.get("scores", {})
    tech = snapshot.get("technical", {})
    alerts = snapshot.get("alerts", [])
    def esc(v):
        return html.escape(str(v))
    alert_items = "".join(f"<li>{esc(a)}</li>" for a in alerts) or "<li>none</li>"
    return f"""<!doctype html>
<html><head><meta charset='utf-8'><title>SpaceX Super Desk</title>
<style>body{{font-family:system-ui;margin:24px;background:#0b0f14;color:#e7edf5}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}}.card{{border:1px solid #263241;border-radius:10px;padding:16px;background:#121821}}code{{color:#9bd}}</style>
</head><body>
<h1>SpaceX / SPCX Super Desk</h1>
<p><b>Mode:</b> monitor-only. Manual decision support only.</p>
<div class='grid'>
<div class='card'><h2>Market</h2><p>Price: {esc(tech.get('price'))}</p><p>IPO gap %: {esc(tech.get('ipo_gap_pct'))}</p><p>Rel vol: {esc(tech.get('relative_volume'))}</p></div>
<div class='card'><h2>Scores</h2><p>Trade ready: {esc(scores.get('trade_ready_score'))}</p><p>Accumulation: {esc(scores.get('accumulation_score'))}</p><p>Setup: {esc(scores.get('selected_setup'))}</p></div>
<div class='card'><h2>Alerts</h2><ul>{alert_items}</ul></div>
<div class='card'><h2>Files</h2><p><code>{esc(paths.latest_snapshot)}</code></p><p><code>{esc(paths.data_center_view)}</code></p></div>
</div>
</body></html>"""


def write_static_page(output: Path | None = None, config_path: str | None = None) -> Path:
    out = output or Path("ui/spacex_desk/index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_static_page(config_path), encoding="utf-8")
    return out
