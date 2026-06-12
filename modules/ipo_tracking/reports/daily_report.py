from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from modules.ipo_tracking.config import load_config, resolve_paths
from modules.ipo_tracking.storage.jsonl_store import read_latest_jsonl


def render_report(snapshot: dict) -> str:
    asset = snapshot.get("asset", {})
    tech = snapshot.get("technical", {})
    scores = snapshot.get("scores", {})
    alerts = snapshot.get("alerts", [])
    sec = snapshot.get("sec", {})
    news = snapshot.get("news", {})
    produced = snapshot.get("produced_at", "")
    lines = [
        f"# SpaceX / {asset.get('symbol', 'SPCX')} Daily Super Desk Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Snapshot: {produced}",
        "",
        "## Market",
        "",
        f"- Price: {tech.get('price')}",
        f"- IPO gap %: {tech.get('ipo_gap_pct')}",
        f"- Previous close gap %: {tech.get('prev_gap_pct')}",
        f"- Relative volume: {tech.get('relative_volume')}",
        f"- Bars count: {tech.get('bars_count')}",
        "",
        "## Smart Money",
        "",
        f"- Bullish FVG: {snapshot.get('smart_money', {}).get('fvg_bullish')}",
        f"- Bearish FVG: {snapshot.get('smart_money', {}).get('fvg_bearish')}",
        f"- BOS candidate: {snapshot.get('smart_money', {}).get('bos_candidate')}",
        f"- Liquidity sweep candidate: {snapshot.get('smart_money', {}).get('liquidity_sweep_candidate')}",
        "",
        "## Scores",
        "",
    ]
    for k, v in scores.items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Alerts", ""])
    if alerts:
        for a in alerts:
            lines.append(f"- {a.get('event')} / {a.get('severity')} / {a}")
    else:
        lines.append("- none")
    lines.extend(["", "## SEC", "", f"- OK: {sec.get('ok')}", f"- Recent filings: {len(sec.get('recent_filings') or [])}"])
    lines.extend(["", "## News", "", f"- OK: {news.get('ok')}", f"- Articles: {news.get('count')}"])
    lines.extend(["", "## Monitor-only", "", "No orders. No execution. Manual decision support only.", ""])
    return "\n".join(lines)


def write_daily_report(config_path: str | None = None) -> Path:
    config = load_config(config_path)
    paths = resolve_paths(config)
    snapshot = read_latest_jsonl(paths.raw_jsonl)
    if snapshot is None and paths.latest_snapshot.exists():
        import json
        snapshot = json.loads(paths.latest_snapshot.read_text(encoding="utf-8"))
    if snapshot is None:
        snapshot = {"asset": {"symbol": "SPCX"}, "scores": {}, "alerts": [], "note": "no snapshot available"}
    paths.report_dir.mkdir(parents=True, exist_ok=True)
    out = paths.report_dir / f"spacex_daily_{datetime.now(timezone.utc).strftime('%Y%m%d')}.md"
    out.write_text(render_report(snapshot), encoding="utf-8")
    return out
