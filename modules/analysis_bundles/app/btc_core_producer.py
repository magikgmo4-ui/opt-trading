import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .schema import BundleOutput
from .vision_analysis_reader import extract_signals_from_vision, read_vision_analysis_freshness


_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_MARKET_METRICS_PATH = _PROJECT_ROOT / "data" / "data_center" / "views" / "market_metrics" / "latest.json"
_COINGLASS_VISION_PATH = _PROJECT_ROOT / "data" / "deskpro" / "inputs" / "vision_context" / "coinglass" / "latest.json"
_TELEGRAM_SIGNALS_DIR = _PROJECT_ROOT / "data" / "telegram_screener" / "signals"


def _read_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _read_market_metrics(symbol: str = "BTCUSDT") -> dict:
    data = _read_json(_MARKET_METRICS_PATH)
    freshness = "UNKNOWN"
    produced_at = None

    if data is None:
        return {"source": "market_metrics.v1", "freshness": "MISSING", "produced_at": None}

    if data.get("input_class") != "market_metrics.v1":
        return {"source": "market_metrics.v1", "freshness": "STALE", "produced_at": None}

    if data.get("symbol") != symbol:
        freshness = "STALE"
        missing = [f"symbol mismatch: expected {symbol}, got {data.get('symbol')}"]
    else:
        freshness = data.get("freshness_state", "UNKNOWN").upper()
        produced_at = data.get("metrics_ts")
        missing = []

    result = {
        "source": "market_metrics.v1",
        "freshness": freshness,
        "produced_at": produced_at,
    }
    if missing:
        result["missing"] = missing
    return result


def _read_coinglass_vision() -> dict:
    data = _read_json(_COINGLASS_VISION_PATH)

    if data is None:
        return {"source": "vision_context.coinglass.v1", "freshness": "MISSING", "produced_at": None}

    if data.get("input_class") != "vision_context.coinglass.v1":
        return {"source": "vision_context.coinglass.v1", "freshness": "STALE", "produced_at": None}

    return {
        "source": "vision_context.coinglass.v1",
        "freshness": data.get("freshness_state", "UNKNOWN").upper(),
        "produced_at": data.get("screenshot_ts"),
    }


def _read_telegram_signals(asset: str = "BTC") -> dict:
    if not _TELEGRAM_SIGNALS_DIR.exists():
        return {"source": "telegram_signal.v1", "freshness": "MISSING", "count": 0, "latest_at": None}

    signals = []
    for f in sorted(_TELEGRAM_SIGNALS_DIR.glob("*.json")):
        data = _read_json(f)
        if data and data.get("pair", "").upper().startswith(asset):
            signals.append(data)

    if not signals:
        return {"source": "telegram_signal.v1", "freshness": "MISSING", "count": 0, "latest_at": None}

    latest = max(signals, key=lambda s: s.get("produced_at", ""))
    return {
        "source": "telegram_signal.v1",
        "freshness": "FRESH",
        "count": len(signals),
        "latest_at": latest.get("produced_at"),
    }


def _read_vision_analysis(symbol: str = "BTCUSDT.P") -> dict:
    signals = extract_signals_from_vision(symbol)
    if not signals.get("available"):
        return {"source": "vision_analysis.v1", "freshness": "MISSING", "produced_at": None, "bias": None}
    return {
        "source": "vision_analysis.v1",
        "freshness": signals.get("freshness", "UNKNOWN"),
        "produced_at": signals.get("analysis_ts"),
        "bias": signals.get("bias"),
        "supports": signals.get("supports", []),
        "resistances": signals.get("resistances", []),
        "timeframe": signals.get("timeframe"),
    }


def _derive_analysis(
    mm: dict,
    cg: dict,
    ts: dict,
    va: dict,
) -> tuple[dict, list[str]]:
    missing = []
    va_bias = va.get("bias") if isinstance(va, dict) else None
    va_fresh = va.get("freshness") in ("FRESH", "fresh") if isinstance(va, dict) else False

    oi_present = cg.get("freshness") not in ("MISSING", "STALE")
    ts_count = ts.get("count", 0) if isinstance(ts, dict) else 0

    # Derive bias: prefer vision analysis if available, else fallback to stubs
    if va_fresh and va_bias is not None:
        bias_short = va_bias
        regime = "TRENDING" if va_bias != "NEUTRAL" else "RANGING"
        confidence = "MEDIUM"
    elif oi_present and ts_count > 0:
        bias_short = "BULLISH"
        regime = "TRENDING"
        confidence = "LOW"
    elif mm.get("freshness") == "FRESH":
        bias_short = "NEUTRAL"
        regime = "RANGING"
        confidence = "LOW"
    else:
        bias_short = "UNKNOWN"
        regime = "UNKNOWN"
        confidence = "UNKNOWN"
        missing.append("ALL: no data available")

    bias_intra = bias_short if bias_short != "UNKNOWN" else "UNKNOWN"
    squeeze = "LOW"

    if mm.get("freshness") == "MISSING":
        missing.append("market_metrics: data file not found")
    if cg.get("freshness") == "MISSING":
        missing.append("coinglass_vision: data file not found")
    if ts.get("count", 0) == 0:
        missing.append("telegram_signals: no BTC signals found")
    if not va_fresh:
        missing.append("vision_analysis: no BTC chart analysis available")

    invalidation = None
    supports = va.get("supports", []) if isinstance(va, dict) else []
    if supports:
        invalidation = f"BTC < {supports[0].get('value', 'N/A')}"

    return {
        "timeframe": "1H",
        "bias_short_term": bias_short,
        "bias_intraday": bias_intra,
        "regime": regime,
        "squeeze_or_stress_level": squeeze,
        "invalidation": "BTC < 86000" if bias_short != "UNKNOWN" else None,
        "confidence": confidence,
        "notes": None,
    }, missing


def _derive_freshness(inputs: dict) -> str:
    states = []
    for inp in inputs.values():
        if isinstance(inp, dict):
            states.append(inp.get("freshness", "UNKNOWN").upper())
    if not states:
        return "UNKNOWN"
    if all(s == "FRESH" for s in states):
        return "FRESH"
    if "MISSING" in states:
        return "STALE"
    return "STALE"


def produce_btc_core(symbol: str = "BTCUSDT", asset: str = "BTC") -> BundleOutput:
    now = datetime.now(timezone.utc).isoformat()

    mm = _read_market_metrics(symbol)
    cg = _read_coinglass_vision()
    ts = _read_telegram_signals(asset)
    va = _read_vision_analysis("BTCUSDT.P")

    analysis, missing = _derive_analysis(mm, cg, ts, va)

    inputs = {
        "market_metrics": mm,
        "coinglass_vision": cg,
        "telegram_signals": ts,
        "vision_analysis": va,
    }

    freshness = _derive_freshness(inputs)

    source_refs = []
    if _MARKET_METRICS_PATH.exists():
        source_refs.append(str(_MARKET_METRICS_PATH))
    if _COINGLASS_VISION_PATH.exists():
        source_refs.append(str(_COINGLASS_VISION_PATH))
    if _TELEGRAM_SIGNALS_DIR.exists():
        source_refs.append(str(_TELEGRAM_SIGNALS_DIR))
    _va_path = _PROJECT_ROOT / "data" / "data_center" / "views" / "vision_analysis" / "by_symbol" / "BTCUSDT.P.json"
    if _va_path.exists():
        source_refs.append(str(_va_path))

    return BundleOutput(
        contract="bundle.btc_core.v1",
        bundle_id="btc.core.v1",
        produced_at=now,
        freshness_state=freshness,
        assets=[asset, symbol],
        inputs=inputs,
        analysis=analysis,
        missing_inputs=missing,
        source_refs=source_refs,
    )
