from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from .io import utc_now


IPO_PRICE = 135.0


@dataclass
class AccumulationZone:
    zone_id: str
    label: str
    priority: int          # 0=ignore, 1=watch, 2=accumulate, 3=buy
    gap_floor_pct: float
    gap_ceiling_pct: float | None
    action: str
    sizing_pct: float      # % of max position


ZONES: list[AccumulationZone] = [
    AccumulationZone("BUY_ZONE", "Buy Zone", 3, -999.0, 5.0, "AGGRESSIVE_ACCUMULATE", 80.0),
    AccumulationZone("ACCUMULATE_ZONE", "Accumulate Zone", 2, 5.0, 15.0, "REGULAR_ACCUMULATE", 60.0),
    AccumulationZone("WAIT_ZONE", "Wait Zone", 1, 15.0, 50.0, "HOLD_NO_ADD", 20.0),
    AccumulationZone("DANGER_ZONE", "Danger Zone", 0, 50.0, None, "REDUCE_ONLY", 0.0),
]


FUNDAMENTAL_FACTORS = {
    "starlink": {
        "name": "Starlink Subscribers",
        "weight": 0.20,
        "bullish_threshold": 5000000,
        "neutral_range": (3000000, 5000000),
        "bearish_threshold": 2000000,
    },
    "launch_cadence": {
        "name": "Launch Cadence (annual)",
        "weight": 0.15,
        "bullish_threshold": 150,
        "neutral_range": (80, 150),
        "bearish_threshold": 50,
    },
    "revenue_growth": {
        "name": "Revenue Growth YoY %",
        "weight": 0.25,
        "bullish_threshold": 30,
        "neutral_range": (10, 30),
        "bearish_threshold": 5,
    },
    "contracts": {
        "name": "New Contracts (quarterly)",
        "weight": 0.15,
        "bullish_threshold": 5,
        "neutral_range": (2, 5),
        "bearish_threshold": 1,
    },
    "institutional_ownership": {
        "name": "Institutional Ownership %",
        "weight": 0.15,
        "bullish_threshold": 30,
        "neutral_range": (10, 30),
        "bearish_threshold": 5,
    },
    "valuation": {
        "name": "Valuation vs IPO",
        "weight": 0.10,
        "bullish_threshold": 1.2,
        "neutral_range": (0.8, 1.2),
        "bearish_threshold": 0.5,
    },
}


def classify_zone(price: float | None, ipo_price: float = IPO_PRICE) -> AccumulationZone:
    if price is None:
        return ZONES[2]
    gap_pct = ((price - ipo_price) / ipo_price) * 100.0
    for z in ZONES:
        ceiling = z.gap_ceiling_pct if z.gap_ceiling_pct is not None else float("inf")
        if z.gap_floor_pct <= gap_pct <= ceiling:
            return z
    return ZONES[-1]


def score_fundamental(factor_name: str, value: float | None) -> dict[str, Any]:
    factor = FUNDAMENTAL_FACTORS.get(factor_name)
    if not factor or value is None:
        return {"factor": factor_name, "score": 0.0, "signal": "neutral", "available": False}

    if value >= factor["bullish_threshold"]:
        signal = "bullish"
        score = 1.0
    elif value >= factor["neutral_range"][0]:
        signal = "neutral"
        score = 0.5
    elif value >= factor["bearish_threshold"]:
        signal = "bearish"
        score = 0.2
    else:
        signal = "bearish"
        score = 0.0

    return {
        "factor": factor_name,
        "name": factor["name"],
        "score": round(score, 3),
        "weighted": round(score * factor["weight"], 3),
        "signal": signal,
        "value": value,
        "available": True,
    }


def compute_accumulation_score(
    price: float | None,
    fundamentals: dict[str, float | None] | None = None,
    ipo_price: float = IPO_PRICE,
) -> dict[str, Any]:
    zone = classify_zone(price, ipo_price)
    fundamentals = fundamentals or {}

    factor_scores = {}
    composite = 0.0
    for name in FUNDAMENTAL_FACTORS:
        val = fundamentals.get(name)
        fs = score_fundamental(name, val)
        factor_scores[name] = fs
        if fs["available"]:
            composite += fs["weighted"]

    technical_score = zone.priority / 3.0
    final_score = round(composite * 0.6 + technical_score * 0.4, 3)

    return {
        "computed_at": utc_now(),
        "price": price,
        "ipo_price": ipo_price,
        "gap_vs_ipo_pct": round(((price - ipo_price) / ipo_price) * 100, 2) if price else None,
        "zone": {
            "id": zone.zone_id,
            "label": zone.label,
            "action": zone.action,
            "sizing_pct": zone.sizing_pct,
        },
        "fundamental_factors": factor_scores,
        "technical_score": round(technical_score, 3),
        "fundamental_composite": round(composite, 3),
        "accumulation_score": final_score,
        "decision": _decision(final_score, zone),
    }


def _decision(score: float, zone: AccumulationZone) -> str:
    if score >= 0.8:
        return "STRONG_ACCUMULATE"
    if score >= 0.6:
        return "ACCUMULATE"
    if score >= 0.4:
        return "HOLD"
    if score >= 0.2:
        return "REDUCE"
    return "AVOID"


def accumulation_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    price = snapshot.get("price")
    news_count = len((snapshot.get("latest_events") or {}).get("sec_edgar", {}).get("filings", []))
    filings_count = len((snapshot.get("latest_events") or {}).get("yahoo_news_rss", {}).get("articles", []))

    fundamentals = {
        "starlink": None,
        "launch_cadence": None,
        "revenue_growth": None,
        "contracts": news_count / 10.0 if news_count else None,
        "institutional_ownership": None,
        "valuation": (price / IPO_PRICE) if price else None,
    }
    return compute_accumulation_score(price, fundamentals)
