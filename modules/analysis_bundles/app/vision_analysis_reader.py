import json
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_BY_SYMBOL_DIR = _PROJECT_ROOT / "data" / "data_center" / "views" / "vision_analysis" / "by_symbol"


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
    return {
        "symbol": symbol,
        "source": "vision_analysis.v1",
        "freshness": capture.get("freshness_state", "UNKNOWN").upper(),
        "analysis_ts": capture.get("analysis_ts"),
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
        if "haussier" in summary.lower() or "hauss" in summary.lower():
            bias = "BULLISH"
        elif "baissier" in summary.lower() or "baiss" in summary.lower():
            bias = "BEARISH"
        elif "neutre" in summary.lower() or "range" in summary.lower():
            bias = "NEUTRAL"

    return {
        "symbol": symbol,
        "available": True,
        "timeframe": capture.get("timeframe"),
        "screen_type": capture.get("screen_type"),
        "freshness": capture.get("freshness_state", "UNKNOWN").upper(),
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
