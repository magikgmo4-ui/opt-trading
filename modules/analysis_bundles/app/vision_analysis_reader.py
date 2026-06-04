import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_BY_SYMBOL_DIR = _PROJECT_ROOT / "data" / "data_center" / "views" / "vision_analysis" / "by_symbol"
_STALE_THRESHOLD_HOURS = 6


def read_vision_analysis(symbol: str) -> Optional[dict]:
    """Read latest vision_analysis.v1 capture for a symbol.

    Returns the latest capture dict (first element of the JSON array), or None if missing.
    """
    path = _BY_SYMBOL_DIR / f"{symbol}.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, list) or len(data) == 0:
        return None
    first = data[0]
    if not isinstance(first, dict):
        return None
    if first.get("input_class") != "vision_analysis.v1":
        return None
    return first


def _age_degrade_freshness(freshness: str, analysis_ts_str: Optional[str]) -> str:
    """Degrade freshness to STALE if analysis_ts is older than threshold."""
    if freshness not in ("FRESH", "fresh"):
        return freshness
    if analysis_ts_str is None:
        return freshness
    try:
        analysis_dt = None
        ts = analysis_ts_str.strip()
        if "Z" in ts:
            analysis_dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        elif "+" in ts[10:]:
            analysis_dt = datetime.fromisoformat(ts)
        elif "-" in ts[10:]:
            analysis_dt = datetime.fromisoformat(ts)
        else:
            analysis_dt = datetime.fromisoformat(ts + "+00:00")
        if analysis_dt.tzinfo is None:
            analysis_dt = analysis_dt.replace(tzinfo=timezone.utc)
        age = datetime.now(timezone.utc) - analysis_dt
        if age > timedelta(hours=_STALE_THRESHOLD_HOURS):
            return "STALE"
    except (ValueError, TypeError):
        pass
    return freshness


def read_vision_analysis_freshness(symbol: str) -> dict:
    """Return freshness summary for a symbol's vision analysis."""
    capture = read_vision_analysis(symbol)
    if capture is None:
        return {
            "symbol": symbol,
            "source": "vision_analysis.v1",
            "freshness": "MISSING",
            "analysis_ts": None,
            "timeframe": None,
            "screen_type": None,
            "signal_count": 0,
        }
    signals = capture.get("signals", [])
    if not isinstance(signals, list):
        signals = []
    raw_freshness = capture.get("freshness_state", "UNKNOWN").upper()
    analysis_ts = capture.get("analysis_ts")
    freshness = _age_degrade_freshness(raw_freshness, analysis_ts)
    return {
        "symbol": symbol,
        "source": "vision_analysis.v1",
        "freshness": freshness,
        "analysis_ts": analysis_ts,
        "timeframe": capture.get("timeframe"),
        "screen_type": capture.get("screen_type"),
        "signal_count": len(signals),
        "capture_id": capture.get("capture_id"),
    }


def extract_signals_from_vision(symbol: str) -> dict:
    """Extract structured signals (supports, resistances, bias, plan) from vision analysis."""
    capture = read_vision_analysis(symbol)
    if capture is None:
        return {"symbol": symbol, "available": False, "supports": [], "resistances": [], "bias": None, "plan": None, "structure": None}

    signals = capture.get("signals", [])
    if not isinstance(signals, list):
        signals = []

    supports = []
    resistances = []
    plan = None
    invalidation = None
    bias = None
    structure = None

    for s in signals:
        if not isinstance(s, dict):
            continue
        stype = s.get("type", "")
        if stype == "support_level":
            supports.append({"value": s.get("value"), "confidence": s.get("confidence")})
        elif stype == "resistance_level":
            resistances.append({"value": s.get("value"), "confidence": s.get("confidence")})
        elif stype == "analysis_note":
            note = s.get("value", "")
            note_type = s.get("note", "")
            if "plan" in note_type:
                plan = note
            elif "invalidation" in note_type:
                invalidation = note

    summary = capture.get("analysis_summary", "")
    if isinstance(summary, str):
        s_lower = summary.lower()
        bull_count = s_lower.count("haussier") + s_lower.count("hauss")
        bear_count = s_lower.count("baissier") + s_lower.count("baiss")
        if bear_count > bull_count:
            bias = "BEARISH"
        elif bull_count > bear_count:
            bias = "BULLISH"
        elif "neutre" in s_lower or "range" in s_lower:
            bias = "NEUTRAL"

    # Plan text override: if keyword bias conflicts with explicit plan, use plan
    if plan and isinstance(plan, str):
        plan_lower = plan.lower()
        if any(w in plan_lower for w in ("short ", "vendre", "short sous", "short sur", "baissier")):
            bias = "BEARISH"
        elif any(w in plan_lower for w in ("long ", "achat", "acheter", "acheté", "haussier")):
            bias = "BULLISH"

    return {
        "symbol": symbol,
        "available": True,
        "timeframe": capture.get("timeframe"),
        "screen_type": capture.get("screen_type"),
        "freshness": _age_degrade_freshness(capture.get("freshness_state", "UNKNOWN").upper(), capture.get("analysis_ts")),
        "analysis_ts": capture.get("analysis_ts"),
        "supports": supports,
        "resistances": resistances,
        "bias": bias,
        "plan": plan,
        "invalidation": invalidation,
        "structure": structure,
    }


def list_available_symbols() -> list[str]:
    """List all symbols with vision analysis data."""
    if not _BY_SYMBOL_DIR.exists():
        return []
    symbols = []
    for f in sorted(_BY_SYMBOL_DIR.glob("*.json")):
        symbols.append(f.stem)
    return symbols


def read_all_vision_freshness() -> dict[str, dict]:
    """Read freshness for all available vision analysis symbols."""
    result = {}
    for symbol in list_available_symbols():
        result[symbol] = read_vision_analysis_freshness(symbol)
    return result
