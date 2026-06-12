from __future__ import annotations
from typing import Any

from .io import utc_now

SETUP_PROBABILITY_WEIGHTS = {
    "IPO_ORB_5M": {
        "momentum": 0.25, "volume": 0.20, "gap": 0.20, "smc": 0.15,
        "consensus": 0.10, "news": 0.05, "dataset": 0.05,
    },
    "GAP_AND_GO": {
        "gap": 0.30, "momentum": 0.20, "volume": 0.20, "smc": 0.10,
        "consensus": 0.10, "news": 0.05, "dataset": 0.05,
    },
    "VWAP_RECLAIM": {
        "smc": 0.25, "volume": 0.20, "vwap_dist": 0.20, "momentum": 0.10,
        "consensus": 0.10, "gap": 0.10, "dataset": 0.05,
    },
    "FVG_RECLAIM": {
        "smc": 0.35, "vwap_dist": 0.20, "momentum": 0.15,
        "consensus": 0.10, "dataset": 0.10, "volume": 0.10,
    },
    "HIGH_VOLUME_CONTINUATION": {
        "volume": 0.35, "momentum": 0.25, "smc": 0.15,
        "consensus": 0.10, "news": 0.10, "dataset": 0.05,
    },
    "FIRST_RED_DAY_TRAP": {
        "gap": 0.25, "smc": 0.20, "volume": 0.20, "momentum": 0.15,
        "dataset": 0.10, "consensus": 0.10,
    },
}


def _score_to_prob(score: float, threshold: float = 0.5) -> float:
    if score >= threshold:
        return min(0.95, 0.5 + score * 0.45)
    return max(0.05, score * 0.5)


def compute_setup_probabilities(
    indicators: dict[str, Any],
    smart_money: dict[str, Any],
    consensus: dict[str, Any],
    scores: dict[str, Any],
    enriched: dict[str, Any],
    analog_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    gap_pct = indicators.get("ipo_gap_pct") or 0
    rel_vol = indicators.get("relative_volume") or 1.0
    vol_z = indicators.get("volume_zscore") or 0.0
    vwap_dist = indicators.get("vwap_distance_pct") or 0.0
    rsi = indicators.get("rsi_14") or 50.0

    fvg_bull = smart_money.get("fvg_bullish", False)
    fvg_bear = smart_money.get("fvg_bearish", False)
    bos = smart_money.get("bos", False)
    smc_score = smart_money.get("smc_score", 0) or 0
    smc_bias = smart_money.get("smc_bias", "neutral")

    trust = consensus.get("weighted_trust_score", 0.5) or 0.5
    disagreement = consensus.get("source_disagreement_score", 0) or 0

    momentum_s = scores.get("momentum", 0) or 0
    trade_ready = scores.get("trade_ready", 0) or 0
    accumulation = scores.get("accumulation", 0) or 0
    risk_s = scores.get("risk", 0) or 0
    news_v = scores.get("news_velocity", 0) or 0

    news_count = enriched.get("context", {}).get("news_count", 0)
    filings_count = enriched.get("context", {}).get("sec_filings_count", 0)

    gap_signal = 1.0 if gap_pct > 5 else (0.7 if gap_pct > 2 else (0.4 if gap_pct > 0 else 0.2))
    vol_signal = min(1.0, max(0.0, (rel_vol - 0.5) / 3.0))
    smc_signal = (smc_score + 1.0) / 2.0 if smc_score is not None else 0.5
    vwap_signal = 1.0 if vwap_dist > 0.5 else (0.6 if vwap_dist > -0.5 else 0.2)
    consensus_quality = max(0.0, trust - disagreement / 100.0 * 0.5)
    news_signal = min(1.0, (news_count + filings_count * 0.1) / 10.0)

    analog_bonus = 0.0
    if analog_result and analog_result.get("top_match"):
        top = analog_result["top_match"]
        if top.get("d1_return", 0) > 20:
            analog_bonus = 0.15
        elif top.get("d1_return", 0) > 10:
            analog_bonus = 0.10
        elif top.get("d1_return", 0) > 0:
            analog_bonus = 0.05

    factors = {
        "gap": gap_signal, "volume": vol_signal, "smc": smc_signal,
        "vwap_dist": vwap_signal, "momentum": momentum_s,
        "consensus": consensus_quality, "news": news_signal,
        "dataset": 0.5 + analog_bonus,
    }

    probabilities = {}
    for setup_id, weights in SETUP_PROBABILITY_WEIGHTS.items():
        prob = 0.0
        for factor, weight in weights.items():
            val = factors.get(factor, 0.5)
            prob += val * weight
        prob = max(0.05, min(0.95, prob))
        probabilities[setup_id] = round(prob, 3)

    risk_discount = min(0.3, risk_s * 0.5)
    for k in probabilities:
        if risk_s > 0.5:
            probabilities[k] = round(max(0.01, probabilities[k] - risk_discount), 3)

    best_setup = max(probabilities, key=probabilities.get)
    best_prob = probabilities[best_setup]

    edge_score = round(probabilities.get("IPO_ORB_5M", 0) * 0.25
        + probabilities.get("GAP_AND_GO", 0) * 0.20
        + probabilities.get("VWAP_RECLAIM", 0) * 0.15
        + probabilities.get("FVG_RECLAIM", 0) * 0.15
        + probabilities.get("HIGH_VOLUME_CONTINUATION", 0) * 0.15
        + probabilities.get("FIRST_RED_DAY_TRAP", 0) * 0.10, 3)

    classification = (
        "A+" if edge_score >= 0.85 else
        "A" if edge_score >= 0.75 else
        "B" if edge_score >= 0.65 else
        "C" if edge_score >= 0.50 else
        "NO_TRADE"
    )

    return {
        "generated_at": utc_now(),
        "setup_probabilities": probabilities,
        "best_setup": {"id": best_setup, "probability": best_prob},
        "edge_score": edge_score,
        "classification": classification,
        "factors": {k: round(v, 3) for k, v in factors.items()},
        "analog_bonus": round(analog_bonus, 3),
        "trade_ready": classification != "NO_TRADE",
    }


def edge_summary(edge: dict[str, Any]) -> str:
    lines = [
        f"EDGE_SCORE: {edge['edge_score']:.2f} ({edge['classification']})",
        f"Best setup: {edge['best_setup']['id']} ({edge['best_setup']['probability']:.0%})",
        "",
        "Setup probabilities:",
    ]
    for setup, prob in sorted(edge["setup_probabilities"].items(), key=lambda x: x[1], reverse=True):
        bar = "\u2588" * int(prob * 20) + "\u2591" * (20 - int(prob * 20))
        lines.append(f"  {setup:30s} [{bar}] {prob:.0%}")
    lines.append(f"")
    lines.append(f"Trade ready: {'YES' if edge['trade_ready'] else 'NO'} | Analog bonus: {edge['analog_bonus']:.0%}")
    return "\n".join(lines)
