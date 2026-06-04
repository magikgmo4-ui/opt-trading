"""
cross_correlation — cross-asset correlation analysis.

Checks directional agreement between related assets to confirm or weaken signals.
"""

from .vision_analysis_reader import extract_signals_from_vision

_CORRELATION_PAIRS = [
    {"pair": ("BTC", "ETH"), "weight": 1.0, "label": "BTC-ETH", "class": "CRYPTO_MAJOR"},
    {"pair": ("BTC", "GOLD"), "weight": 0.7, "label": "BTC-GOLD", "class": "MACRO_HEDGE"},
    {"pair": ("BTC", "DXY"), "weight": -0.8, "label": "BTC-DXY", "class": "MACRO_INVERSE"},
    {"pair": ("BTC", "SPX"), "weight": 0.6, "label": "BTC-SPX", "class": "RISK_ON"},
    {"pair": ("BTC", "IBIT"), "weight": 1.0, "label": "BTC-IBIT", "class": "ETF_CONFIRM"},
    {"pair": ("ETH", "SOL"), "weight": 0.9, "label": "ETH-SOL", "class": "CRYPTO_ALT"},
    {"pair": ("WTI", "GASOLINE"), "weight": 0.8, "label": "WTI-GASOLINE", "class": "ENERGY_CHAIN"},
    {"pair": ("WTI", "NATGAS"), "weight": 0.5, "label": "WTI-NATGAS", "class": "ENERGY_SIBLING"},
    {"pair": ("DXY", "GOLD"), "weight": -0.7, "label": "DXY-GOLD", "class": "MACRO_INVERSE"},
    {"pair": ("SPX", "VIX"), "weight": -0.9, "label": "SPX-VIX", "class": "VOL_INVERSE"},
]

_SYMBOL_MAP = {
    "BTC": "BTCUSDT.P",
    "ETH": "ETHUSDT.P",
    "SOL": "SOLUSDT.P",
    "GOLD": "OANDA:XAUUSD",
    "DXY": "TVC:DXY",
    "SPX": "SPY",
    "VIX": "TVC:VIX",
    "IBIT": "NASDAQ:IBIT",
    "WTI": "NYMEX:CL1!",
    "NATGAS": "NYMEX:NG1!",
    "GASOLINE": "NYMEX:RB1!",
}


def produce_cross_correlation() -> dict:
    """Analyze directional agreement across all correlation pairs."""
    results = []
    aligned = 0
    divergent = 0
    unknown = 0

    for pair_info in _CORRELATION_PAIRS:
        a, b = pair_info["pair"]
        sym_a = _SYMBOL_MAP.get(a)
        sym_b = _SYMBOL_MAP.get(b)
        if not sym_a or not sym_b:
            continue

        sig_a = extract_signals_from_vision(sym_a)
        sig_b = extract_signals_from_vision(sym_b)

        bias_a = sig_a.get("bias")
        bias_b = sig_b.get("bias")
        fresh_a = sig_a.get("freshness") == "FRESH"
        fresh_b = sig_b.get("freshness") == "FRESH"

        if bias_a is None or bias_b is None:
            status = "UNKNOWN"
            unknown += 1
        elif not fresh_a or not fresh_b:
            status = "UNKNOWN"
            unknown += 1
        else:
            expected = "AGREE" if pair_info["weight"] > 0 else "INVERTED"
            if pair_info["weight"] > 0 and bias_a == bias_b:
                status = "ALIGNED"
                aligned += 1
            elif pair_info["weight"] < 0 and bias_a != bias_b:
                status = "ALIGNED"
                aligned += 1
            else:
                status = "DIVERGENT"
                divergent += 1

        results.append({
            "label": pair_info["label"],
            "class": pair_info["class"],
            "asset_a": a,
            "bias_a": bias_a,
            "asset_b": b,
            "bias_b": bias_b,
            "status": status,
            "fresh_a": fresh_a,
            "fresh_b": fresh_b,
        })

    total = aligned + divergent + unknown
    alignment_pct = int((aligned / total) * 100) if total > 0 else 0

    return {
        "total_pairs": len(results),
        "aligned": aligned,
        "divergent": divergent,
        "unknown": unknown,
        "alignment_pct": alignment_pct,
        "signal": "CONFIRMED" if alignment_pct >= 60 else "MIXED" if alignment_pct >= 30 else "DIVERGENT",
        "pairs": results,
    }
