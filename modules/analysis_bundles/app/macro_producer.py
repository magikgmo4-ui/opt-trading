import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .schema import BundleOutput
from .vision_analysis_reader import extract_signals_from_vision, read_vision_analysis_freshness


_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_BY_SYMBOL_DIR = _PROJECT_ROOT / "data" / "data_center" / "views" / "vision_analysis" / "by_symbol"

_VISION_MACRO_MAP = {
    "TVC:DXY": {"asset": "DXY", "label": "Dollar Index", "status": "ESTABLISHED"},
    "TVC:VIX": {"asset": "VIX", "label": "Volatility Index", "status": "ESTABLISHED"},
    "TVC:US10Y": {"asset": "US10Y", "label": "US 10Y Yield", "status": "ESTABLISHED"},
    "OANDA:XAUUSD": {"asset": "GOLD", "label": "Gold Spot", "status": "ESTABLISHED"},
    "SPY": {"asset": "SPX", "label": "S&P 500 ETF", "status": "ESTABLISHED"},
    "NYMEX:CL1!": {"asset": "WTI", "label": "Crude Oil WTI", "status": "ESTABLISHED"},
    "NYMEX:RB1!": {"asset": "GASOLINE", "label": "RBOB Gasoline", "status": "HYPOTHESIS"},
    "NYMEX:NG1!": {"asset": "NATGAS", "label": "Natural Gas", "status": "HYPOTHESIS"},
    "BITGET:BZUSDT": {"asset": "BRENT", "label": "Brent Oil", "status": "HYPOTHESIS"},
    "FX:EURUSD": {"asset": "EURUSD", "label": "EUR/USD", "status": "ESTABLISHED"},
}

_CRYPTO_MACRO_MAP = {
    "CRYPTOCAP:BTC.D": {"asset": "BTC_DOM", "label": "BTC Dominance", "status": "ESTABLISHED"},
    "CRYPTOCAP:TOTAL": {"asset": "TOTAL_MCAP", "label": "Total Crypto Market Cap", "status": "ESTABLISHED"},
    "CRYPTOCAP:TOTAL2": {"asset": "TOTAL2", "label": "Total Crypto ex-BTC", "status": "ESTABLISHED"},
    "CRYPTOCAP:TOTAL3": {"asset": "TOTAL3", "label": "Total Crypto ex-BTC+ETH", "status": "ESTABLISHED"},
}


def _read_vision_for_symbol(tv_symbol: str, asset_info: dict) -> dict:
    freshness = read_vision_analysis_freshness(tv_symbol)
    signals = extract_signals_from_vision(tv_symbol)

    result = {
        "source": "vision_analysis.v1",
        "tradingview_symbol": tv_symbol,
        "asset": asset_info["asset"],
        "label": asset_info["label"],
        "status": asset_info["status"],
        "freshness": freshness.get("freshness", "MISSING"),
        "produced_at": freshness.get("analysis_ts"),
        "bias": signals.get("bias"),
        "supports": signals.get("supports", []),
        "resistances": signals.get("resistances", []),
        "plan": signals.get("plan"),
        "invalidation": signals.get("invalidation"),
    }
    return result


def _derive_macro_analysis(inputs: dict) -> tuple[dict, list[str]]:
    missing = []

    dxy = inputs.get("TVC:DXY", {})
    vix = inputs.get("TVC:VIX", {})
    gold = inputs.get("OANDA:XAUUSD", {})
    spy = inputs.get("SPY", {})
    us10y = inputs.get("TVC:US10Y", {})

    dxy_avail = dxy.get("freshness") not in ("MISSING",)
    spy_avail = spy.get("freshness") not in ("MISSING",)
    gold_avail = gold.get("freshness") not in ("MISSING",)
    vix_avail = vix.get("freshness") not in ("MISSING",)
    dxy_fresh = dxy.get("freshness") == "FRESH"
    spy_fresh = spy.get("freshness") == "FRESH"
    gold_fresh = gold.get("freshness") == "FRESH"

    avail_count = sum([dxy_avail, spy_avail, gold_avail, vix_avail])
    fresh_count = sum([dxy_fresh, spy_fresh, gold_fresh, vix_avail and vix.get("freshness") == "FRESH"])

    if avail_count == 0:
        missing.append("ALL: no macro data available")
        return {
            "timeframe": "1D",
            "bias_short_term": "UNKNOWN",
            "bias_intraday": "UNKNOWN",
            "regime": "UNKNOWN",
            "squeeze_or_stress_level": "UNKNOWN",
            "invalidation": None,
            "confidence": "UNKNOWN",
        }, missing

    # Use bias even from stale data, degrade confidence
    spy_bias = spy.get("bias")
    dxy_bias = dxy.get("bias")
    gold_bias = gold.get("bias")

    if spy_avail and spy_bias == "BULLISH":
        regime = "RISK_ON"
    elif spy_avail and spy_bias == "BEARISH":
        regime = "RISK_OFF"
    elif dxy_avail and dxy_bias == "BULLISH" and gold_bias == "BEARISH":
        regime = "RISK_OFF"
    elif gold_avail and gold_bias == "BULLISH":
        regime = "RISK_ON"
    else:
        regime = "RISK_OFF" if gold_bias == "BEARISH" else "UNKNOWN"

    bias_short = spy_bias if spy_bias else gold_bias if gold_bias else "NEUTRAL"
    confidence = "MEDIUM" if fresh_count >= 3 else "LOW"
    if fresh_count < avail_count:
        missing.append(f"macro: {avail_count - fresh_count}/{avail_count} sources stale, confidence degraded")

    for tv_sym, info in _VISION_MACRO_MAP.items():
        inp = inputs.get(tv_sym, {})
        if inp.get("freshness") == "MISSING":
            missing.append(f"{info['asset']} ({info['label']}): no data")

    return {
        "timeframe": "1D",
        "bias_short_term": bias_short,
        "bias_intraday": "NEUTRAL",
        "regime": regime,
        "squeeze_or_stress_level": "LOW",
        "invalidation": "VIX > 30" if regime != "UNKNOWN" else None,
        "confidence": confidence,
        "notes": f"Vision analysis: {fresh_count}/4 macro sources fresh",
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


def produce_macro() -> BundleOutput:
    now = datetime.now(timezone.utc).isoformat()

    inputs = {}
    assets = []

    for tv_sym, info in _VISION_MACRO_MAP.items():
        inp = _read_vision_for_symbol(tv_sym, info)
        inputs[tv_sym] = inp
        assets.append(info["asset"])

    for tv_sym, info in _CRYPTO_MACRO_MAP.items():
        inp = _read_vision_for_symbol(tv_sym, info)
        inputs[tv_sym] = inp
        assets.append(info["asset"])

    analysis, missing = _derive_macro_analysis(inputs)

    established_inputs = {
        k: v for k, v in inputs.items()
        if _VISION_MACRO_MAP.get(k, _CRYPTO_MACRO_MAP.get(k, {})).get("status") == "ESTABLISHED"
    }
    freshness = _derive_freshness(established_inputs) if established_inputs else "UNKNOWN"

    source_refs = []
    for tv_sym in _VISION_MACRO_MAP:
        path = _BY_SYMBOL_DIR / f"{tv_sym}.json"
        if path.exists():
            source_refs.append(str(path))
    for tv_sym in _CRYPTO_MACRO_MAP:
        path = _BY_SYMBOL_DIR / f"{tv_sym}.json"
        if path.exists():
            source_refs.append(str(path))

    return BundleOutput(
        contract="bundle.macro.v1",
        bundle_id="macro.v1",
        produced_at=now,
        freshness_state=freshness,
        assets=assets,
        inputs=inputs,
        analysis=analysis,
        missing_inputs=missing,
        source_refs=source_refs,
    )
