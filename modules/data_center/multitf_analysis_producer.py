"""
multitf_analysis_producer.py — aggregate multi-TF analysis input per symbol.

Reads from existing DC views:
  - market_metrics        → price, vwap, change_24h
  - vision_analysis       → trend, signals, freshness
  - signal_event.v1       → CDP events

Produces:
  multitf_analysis_input.v1 — per-symbol aggregated analysis input
  Writes to: data/data_center/views/multitf_analysis_input.v1/by_symbol/{SYM}.json
             data/data_center/views/multitf_analysis_input.v1/latest.json

Usage:
    python -m modules.data_center.multitf_analysis_producer

Invariants:
  - Read-only consumer of existing views
  - No execution, no broker, no order
  - Monitor-only
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp") as fh:
        json.dump(payload, fh, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def _load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _extract_trend_from_summary(summary: str) -> str:
    low = summary.lower()
    if any(w in low for w in ["baissier", "baissi", "bearish", "bear", "baisse "]):
        return "bearish"
    if any(w in low for w in ["haussier", "bullish", "bull", "hauss "]):
        return "bullish"
    if any(w in low for w in ["range", "neutre", "neutral", "consolidation", "lateral"]):
        return "neutral"
    return ""


_ASSET_CLASS_MAP = {
    "BTC": "crypto_perp", "ETH": "crypto_perp", "SOL": "crypto_perp",
    "XAUUSD": "forex_cfd", "DXY": "index", "VIX": "index",
    "SPY": "stock", "SPCX": "ipo", "NVDA": "stock", "PLTR": "stock",
    "AVGO": "stock", "RKLB": "stock", "ASTS": "stock", "LUNR": "stock",
}

_SYMBOLS = ["BTC", "ETH", "SOL", "XAUUSD", "SPCX"]


def produce_multitf_analysis_input() -> dict:
    """Aggregate existing DC views into multitf_analysis_input.v1 per symbol."""
    now = datetime.now(timezone.utc).isoformat()
    produced = 0
    symbols_written = []

    # Load shared sources once (array format from signal_event_writer.py)
    signal_events = _load_json(_VIEWS_DIR / "signal_event.v1" / "latest.json")
    signal_by_symbol: dict[str, list] = {}
    # Map TradingView symbols to canonical symbols
    _SYM_NORM = {"BTCUSDT.P": "BTC", "ETHUSDT.P": "ETH", "SOLUSDT.P": "SOL",
                 "OANDA:XAUUSD": "XAUUSD", "SPCX": "SPCX", "XAUUSD": "XAUUSD",
                 "BTCUSDT": "BTC", "ETHUSDT": "ETH", "SOLUSDT": "SOL"}
    if isinstance(signal_events, list):
        for evt in signal_events:
            raw_sym = evt.get("symbol", "")
            sym = _SYM_NORM.get(raw_sym, raw_sym)
            if sym:
                signal_by_symbol.setdefault(sym, []).append(evt)
    elif isinstance(signal_events, dict):
        sig_dir = _VIEWS_DIR / "signal_event.v1" / "by_symbol"
        for sym in _SYMBOLS:
            sig_file = sig_dir / sym / "latest.json"
            sig_data = _load_json(sig_file)
            if isinstance(sig_data, list):
                signal_by_symbol[sym] = sig_data
            elif isinstance(sig_data, dict):
                signal_by_symbol[sym] = sig_data.get("events", [])

    for sym in _SYMBOLS:
        entry = _build_symbol_entry(sym, now, signal_by_symbol.get(sym, []))
        if entry is None:
            continue

        out_path = _VIEWS_DIR / "multitf_analysis_input.v1" / "by_symbol" / f"{sym}.json"
        _atomic_write(out_path, entry)
        symbols_written.append(sym)
        produced += 1

    # Global latest
    global_payload = {
        "input_class": "multitf_analysis_input.v1",
        "provider_id": "data_center_aggregator",
        "produced_at": now,
        "symbols": symbols_written,
        "total_symbols": produced,
    }
    _atomic_write(_VIEWS_DIR / "multitf_analysis_input.v1" / "latest.json", global_payload)

    # Runtime registry
    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write(
        producer_id="data_center_aggregator",
        contract_class="multitf_analysis_input.v1",
        output_path=str(_VIEWS_DIR / "multitf_analysis_input.v1" / "latest.json"),
        status="ok",
        evidence={"symbols": produced},
    )

    return {"produced_at": now, "symbols": produced}


def _build_symbol_entry(sym: str, now: str, signal_evts: list) -> dict | None:
    """Build a multitf_analysis_input.v1 entry for one symbol."""

    # ── market_metrics ──
    mm_path = _VIEWS_DIR / "market_metrics" / "by_symbol" / f"{sym}.json"
    if sym == "SPCX":
        # SPCX price from command_center, not market_metrics
        cc_path = _PROJECT_ROOT / "data" / "ipo" / "spacex" / "command_center" / "latest.json"
        cc = _load_json(cc_path)
        if isinstance(cc, dict):
            price = cc.get("price")
            vwap_val = cc.get("vwap")
            freshness_state = "fresh" if price else "unknown"
        else:
            price = None
            vwap_val = None
    elif sym in ("BTC", "ETH", "SOL"):
        mm_path = _VIEWS_DIR / "market_metrics" / "by_symbol" / f"{sym}USDT.json"
    if sym != "SPCX":
        if not mm_path.exists():
            mm_path = _VIEWS_DIR / "market_metrics" / "latest.json"

        mm = _load_json(mm_path)
        if isinstance(mm, list) and mm:
            mm = mm[0]

        if isinstance(mm, dict):
            price = mm.get("last_price") or mm.get("price")
            freshness_state = mm.get("freshness_state", "unknown")
            vwap_val = mm.get("vwap")
            change_24h = mm.get("change_24h") or mm.get("price_change_24h_pct")

    if price is None or price == 0:
        price = None

    # ── vision_analysis ──
    va_path = _VIEWS_DIR / "vision_analysis" / "by_symbol"
    va_file_map = {"BTC": "BTCUSDT.P", "ETH": "ETHUSDT.P", "SOL": "SOLUSDT.P",
                   "XAUUSD": "OANDA:XAUUSD", "SPCX": "SPCX.P"}
    va_file = va_file_map.get(sym, f"{sym}USDT.P")
    va_data = _load_json(va_path / f"{va_file}.json")
    if isinstance(va_data, list) and va_data:
        va_data = va_data[0]

    trend = ""
    signals = []
    if isinstance(va_data, dict):
        # Fallback price from vision_analysis if market_metrics had none
        if price is None:
            va_signals = va_data.get("signals", [])
            num_sigs = [s for s in (va_signals or []) if isinstance(s.get("value"), (int, float))]
            if num_sigs:
                best = max(num_sigs, key=lambda s: s.get("confidence", 0))
                price = best.get("value")
        summary = va_data.get("analysis_summary", "")
        if isinstance(summary, str):
            trend = _extract_trend_from_summary(summary)
        if va_data.get("freshness_state") == "fresh":
            freshness_state = "fresh"
        # Signal events from vision
        for sig in va_data.get("signals", [])[:5]:
            if isinstance(sig, dict):
                signals.append({
                    "source": "vision_analysis",
                    "event": sig.get("type", "signal"),
                    "timeframe": va_data.get("timeframe", "M15"),
                    "price": sig.get("value") if isinstance(sig.get("value"), (int, float)) else None,
                    "confidence": sig.get("confidence", 0.5),
                    "timestamp": va_data.get("analysis_ts", now),
                    "monitor_only": True,
                })

    # ── signal_event.v1 (CDP events) ──
    for evt in signal_evts[:5]:
        event_name = evt.get("signal") or evt.get("event", "")
        if event_name:
            signals.append({
                "source": "tradingview_cdp",
                "event": event_name,
                "timeframe": evt.get("timeframe", "M15"),
                "price": evt.get("price"),
                "volume": evt.get("qty"),
                "confidence": 0.70,
                "timestamp": evt.get("ts", now),
                "monitor_only": True,
            })

    # ── levels ──
    levels = {}
    if isinstance(va_data, dict):
        va_signals = va_data.get("signals", [])
        if isinstance(va_signals, list):
            supports = [s["value"] for s in va_signals if isinstance(s, dict)
                       and s.get("type") == "support_level"
                       and isinstance(s.get("value"), (int, float))]
            resistances = [s["value"] for s in va_signals if isinstance(s, dict)
                          and s.get("type") == "resistance_level"
                          and isinstance(s.get("value"), (int, float))]
            if supports:
                levels["support_levels"] = sorted(supports)
            if resistances:
                levels["resistance_levels"] = sorted(resistances)
    if price:
        if "support_levels" not in levels:
            levels["support_levels"] = [round(price * 0.95, 2)]
        if "resistance_levels" not in levels:
            levels["resistance_levels"] = [round(price * 1.05, 2)]
        if vwap_val:
            levels["vwap"] = vwap_val

    # ── timeframes (indicators only — OHLCV bars left for future richer source) ──
    timeframes = {}
    for tf in ["H4", "H1", "M15"]:
        tf_indicators = {
            "trend": trend,
            "vwap": vwap_val,
            "price_vs_vwap": "below" if price and vwap_val and price < vwap_val else "above" if price and vwap_val else None,
            "relative_volume": 1.0,
        }
        if vwap_val and price and price > 0:
            if price > vwap_val:
                tf_indicators["price_vs_vwap"] = "above"
            elif price < vwap_val:
                tf_indicators["price_vs_vwap"] = "below"
            else:
                tf_indicators["price_vs_vwap"] = "at"
        else:
            del tf_indicators["price_vs_vwap"]
        timeframes[tf] = {
            "indicators": {k: v for k, v in tf_indicators.items() if v is not None},
            "freshness": {"state": freshness_state, "bar_count": 0, "last_bar_ts": now},
        }

    # ── macro_context ──
    macro_context = {}
    dxy_data = _load_json(_VIEWS_DIR / "market_metrics" / "by_symbol" / "DXY.json")
    if isinstance(dxy_data, dict):
        macro_context["dxy_trend"] = "unknown"

    # ── missing fields ──
    missing = []
    if not freshness_state or freshness_state == "unknown":
        missing.append("freshness_state")
    if "W1" not in timeframes:
        missing.extend(["W1", "D1", "M5"])
    if not signals:
        missing.append("signals")
    if not levels.get("support_levels"):
        missing.append("support_levels")

    entry = {
        "input_class": "multitf_analysis_input.v1",
        "symbol": sym,
        "asset_class": _ASSET_CLASS_MAP.get(sym, "unknown"),
        "as_of": now,
        "price": price,
        "source": "data_center_aggregator",
        "freshness_state": freshness_state,
        "timeframes": timeframes,
        "levels": levels,
        "signals": signals,
        "source_quality": {
            "source": "data_center",
            "producer": "multitf_analysis_producer",
            "freshness_state": freshness_state,
            "age_minutes": 0,
            "completeness_score": 0.5,
            "confidence_score": 0.7,
        },
        "missing": missing,
    }
    return entry


if __name__ == "__main__":
    r = produce_multitf_analysis_input()
    print(f"multitf_analysis_input.v1: {r['symbols']} symbols")
