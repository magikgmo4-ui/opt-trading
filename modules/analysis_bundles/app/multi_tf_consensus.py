"""
multi_tf_consensus — multi-timeframe bias consensus from vision analysis.

Reads multiple timeframes for the same symbol and scores agreement.
15m + 1h agree = strong conviction. Disagree = divergence warning.
"""

from .vision_analysis_reader import extract_signals_from_vision, read_vision_analysis

_TF_WEIGHTS = {
    "15m": 0.4,
    "1h": 0.35,
    "4h": 0.15,
    "1d": 0.10,
}

_ASSETS_WITH_MULTI_TF = {
    "BTC": [("BTCUSDT.P", "15m"), ("BTCUSDT.P", "1h")],
    "ETH": [("ETHUSDT.P", "15m"), ("ETHUSDT.P", "1h")],
    "WTI": [("NYMEX:CL1!", "1h"), ("NYMEX:CL1!", "4h")],
    "BRENT": [("BITGET:BZUSDT", "1h"), ("BITGET:BZUSDT", "4h")],
    "NATGAS": [("NYMEX:NG1!", "1h"), ("NYMEX:NG1!", "4h")],
    "GASOLINE": [("NYMEX:RB1!", "1h"), ("NYMEX:RB1!", "4h")],
}


def produce_multi_tf_consensus(asset: str = "BTC") -> dict:
    """Score bias agreement across multiple timeframes for an asset."""
    entries = _ASSETS_WITH_MULTI_TF.get(asset, [])
    if not entries:
        return {"asset": asset, "available": False, "consensus": False, "score": 0}

    tf_results = {}
    biases = []
    for symbol, tf in entries:
        sig = extract_signals_from_vision(symbol)
        bias = sig.get("bias")
        freshness = sig.get("freshness", "UNKNOWN")
        tf_results[tf] = {
            "bias": bias,
            "freshness": freshness,
            "supports": sig.get("supports", [])[:2],
            "resistances": sig.get("resistances", [])[:2],
        }
        if bias and freshness == "FRESH":
            biases.append((tf, bias))

    if len(biases) < 2:
        return {
            "asset": asset,
            "available": True,
            "consensus": False,
            "score": 0,
            "timeframes": len(biases),
            "detail": tf_results,
        }

    # Count agreement
    bullish_count = sum(1 for _, b in biases if b == "BULLISH")
    bearish_count = sum(1 for _, b in biases if b == "BEARISH")
    total = len(biases)

    if bullish_count == total:
        consensus_bias = "BULLISH"
        agreement_score = 100
    elif bearish_count == total:
        consensus_bias = "BEARISH"
        agreement_score = 100
    elif bullish_count > bearish_count:
        consensus_bias = "BULLISH"
        agreement_score = int((bullish_count / total) * 80)
    elif bearish_count > bullish_count:
        consensus_bias = "BEARISH"
        agreement_score = int((bearish_count / total) * 80)
    else:
        consensus_bias = "NEUTRAL"
        agreement_score = 50

    return {
        "asset": asset,
        "available": True,
        "consensus": True,
        "bias": consensus_bias,
        "score": agreement_score,
        "timeframes": total,
        "detail": tf_results,
    }
