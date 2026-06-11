"""
telegram_signal_query.py — queryable interface for telegram screener signals.

Reads from data_center views (fast, cached) or re-parses raw collector data.
Supports filtering by channel, pair, direction, completeness, mode, priority.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_DC_TG = _PROJECT_ROOT / "data" / "data_center" / "views" / "telegram_signals"
_SIGNALS_DIR = _PROJECT_ROOT / "data" / "telegram_screener" / "signals"

# ── Consolidated channel type taxonomy ──
CHANNEL_TYPE_LABELS = {
    "xau_signal":       {"fr": "Or (XAU/USD)",       "icon": "🥇"},
    "trade_signal":     {"fr": "Trade Signal",       "icon": "📊"},
    "whale_trade":      {"fr": "Flux Baleine",        "icon": "🐋"},
    "whale_alert":      {"fr": "Alerte Baleine",      "icon": "🚨"},
    "onchain_data":     {"fr": "On-Chain",            "icon": "⛓️"},
    "forex_signal":     {"fr": "Forex",               "icon": "💱"},
    "tp_hits":          {"fr": "TP Hits (ignoré)",   "icon": "✅"},
    "education":        {"fr": "Éducation (ignoré)",  "icon": "📚"},
    "marketing":        {"fr": "Marketing (ignoré)",  "icon": "📢"},
    "trade_setup":      {"fr": "Trade Setup",         "icon": "🔧"},
    "unknown":          {"fr": "Inconnu",             "icon": "❓"},
}

PRIORITY_LABELS = {
    "P0": {"fr": "Actif — backtesté",      "color": "green"},
    "P1": {"fr": "Actif — promu",          "color": "blue"},
    "P2": {"fr": "Surveillance / Contexte","color": "yellow"},
    "P3": {"fr": "Rejeté",                 "color": "red"},
}


def _read_cached_signals() -> list[dict]:
    """Read signals from filesystem cache (fast)."""
    if not _SIGNALS_DIR.exists():
        return []
    signals = []
    for f in sorted(_SIGNALS_DIR.glob("signal_*.json")):
        try:
            signals.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            continue
    return signals


def _read_dc_signals() -> list[dict]:
    """Read signals from data_center history (newest)."""
    hist_dir = _DC_TG / "history"
    if not hist_dir.exists():
        return _read_cached_signals()
    signals = []
    for f in sorted(hist_dir.glob("*.json")):
        try:
            signals.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            continue
    return signals


def query_signals(
    channel: Optional[str] = None,
    pair: Optional[str] = None,
    direction: Optional[str] = None,
    complete_only: bool = False,
    mode: Optional[str] = None,
    priority: Optional[str] = None,
    channel_type: Optional[str] = None,
    limit: Optional[int] = None,
    source: str = "cache",
) -> list[dict]:
    """Query signals with filters. Source: 'cache' (fast) or 'dc' (data_center)."""
    if source == "dc":
        signals = _read_dc_signals()
    else:
        signals = _read_cached_signals()

    results = []
    for s in signals:
        if channel and s.get("channel") != channel:
            continue
        if pair and pair.upper() not in s.get("pair", "").upper():
            continue
        if direction and s.get("direction", "").upper() != direction.upper():
            continue
        if complete_only:
            if not (s.get("entry_price") and s.get("sl") and s.get("tp")):
                continue
        if mode and s.get("channel_priority") != mode:
            # mode maps to priority field in signal
            pass  # mode filtering done at channel level
        if priority and s.get("channel_priority") != priority:
            continue
        if channel_type and s.get("channel_type") != channel_type:
            continue
        results.append(s)

    if limit:
        return results[:limit]
    return results


def list_channels(channel_type: Optional[str] = None, mode: Optional[str] = None) -> list[dict]:
    """List active channels with their types, modes, and signal counts."""
    from modules.analysis_bundles.app.telegram_screener_bridge import _CHANNEL_PRIORITY

    signals = _read_cached_signals()
    # Count signals per channel
    ch_counts: dict[str, dict] = {}
    for s in signals:
        ch = s.get("channel", "unknown")
        if ch not in ch_counts:
            ch_counts[ch] = {"total": 0, "complete": 0, "pairs": set()}
        ch_counts[ch]["total"] += 1
        if s.get("entry_price") and s.get("sl") and s.get("tp"):
            ch_counts[ch]["complete"] += 1
        if s.get("pair"):
            ch_counts[ch]["pairs"].add(s["pair"])

    channels = []
    for alias, info in sorted(_CHANNEL_PRIORITY.items()):
        if channel_type and info.get("type") != channel_type:
            continue
        if mode and info.get("mode") != mode:
            continue
        cnt = ch_counts.get(alias, {"total": 0, "complete": 0, "pairs": set()})
        channels.append({
            "alias": alias,
            "priority": info.get("priority", "P2"),
            "mode": info.get("mode", "REJECTED"),
            "type": info.get("type", "unknown"),
            "output": info.get("output", "skip"),
            "note": info.get("note", ""),
            "signals_total": cnt["total"],
            "signals_complete": cnt["complete"],
            "pairs": sorted(cnt["pairs"]),
            "type_label": CHANNEL_TYPE_LABELS.get(info.get("type", ""), {}).get("fr", info.get("type", "")),
            "priority_label": PRIORITY_LABELS.get(info.get("priority", ""), {}).get("fr", ""),
        })
    return channels


def signal_summary() -> dict:
    """Produce a summary of all signals for dashboard display."""
    signals = _read_cached_signals()
    now = datetime.now(timezone.utc).isoformat()

    total = len(signals)
    complete = sum(1 for s in signals if s.get("entry_price") and s.get("sl") and s.get("tp"))
    longs = sum(1 for s in signals if s.get("direction") == "LONG")
    shorts = sum(1 for s in signals if s.get("direction") == "SHORT")

    # By pair
    by_pair: dict[str, int] = {}
    for s in signals:
        p = s.get("pair", "?")
        by_pair[p] = by_pair.get(p, 0) + 1

    # By channel type
    by_type: dict[str, dict] = {}
    for s in signals:
        ct = s.get("channel_type", "unknown")
        if ct not in by_type:
            by_type[ct] = {"total": 0, "complete": 0, "label": CHANNEL_TYPE_LABELS.get(ct, {}).get("fr", ct)}
        by_type[ct]["total"] += 1
        if s.get("entry_price") and s.get("sl") and s.get("tp"):
            by_type[ct]["complete"] += 1

    # By channel
    by_channel: dict[str, dict] = {}
    for s in signals:
        ch = s.get("channel", "unknown")
        if ch not in by_channel:
            by_channel[ch] = {"total": 0, "complete": 0, "priority": s.get("channel_priority", "P2")}
        by_channel[ch]["total"] += 1
        if s.get("entry_price") and s.get("sl") and s.get("tp"):
            by_channel[ch]["complete"] += 1

    active_channels = len({s.get("channel") for s in signals})

    return {
        "contract": "telegram_signal_summary.v1",
        "produced_at": now,
        "totals": {
            "signals": total,
            "complete": complete,
            "incomplete": total - complete,
            "longs": longs,
            "shorts": shorts,
            "active_channels": active_channels,
        },
        "by_pair": dict(sorted(by_pair.items(), key=lambda x: -x[1])[:20]),
        "by_type": by_type,
        "by_channel": dict(sorted(by_channel.items(), key=lambda x: -x[1]["total"])[:30]),
        "channels": list_channels(),
    }


def format_table(rows: list[dict], columns: list[str], max_widths: dict[str, int] | None = None) -> str:
    """Format a list of dicts as aligned text table."""
    if not rows:
        return "(aucun résultat)"
    widths = dict(max_widths or {})
    for col in columns:
        widths[col] = max(widths.get(col, 0), len(col), max((len(str(r.get(col, ""))) for r in rows), default=0))
    header = "  ".join(col.ljust(widths[col]) for col in columns)
    sep = "  ".join("-" * widths[col] for col in columns)
    lines = [header, sep]
    for r in rows:
        lines.append("  ".join(str(r.get(col, "")).ljust(widths[col]) for col in columns))
    return "\n".join(lines)
