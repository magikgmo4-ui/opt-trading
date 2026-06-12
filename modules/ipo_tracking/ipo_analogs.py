from __future__ import annotations

IPO_ANALOGS: dict[str, dict] = {
    "ARM": {
        "name": "ARM Holdings",
        "category": "semiconductor",
        "ipo_date": "2023-09-14",
        "ipo_price": 51.0,
        "open": 56.10,
        "day1_close": 63.59,
        "day1_gap_pct": 10.0,
        "day1_return_pct": 24.7,
        "day1_high_pct": 30.0,
        "day5_return_pct": 3.2,
        "week1_return_pct": 3.2,
        "month1_return_pct": -5.1,
        "volume_day1_m": 50,
        "orb_5m_return_pct": 8.0,
        "vwap_reclaim_day1": True,
        "fvg_day1": True,
        "market_cap_bn": 54.5,
        "sector": "tech_hardware",
        "relevance": "highly_relevant",
    },
    "RDDT": {
        "name": "Reddit",
        "category": "social_media",
        "ipo_date": "2024-03-21",
        "ipo_price": 34.0,
        "open": 47.0,
        "day1_close": 50.44,
        "day1_gap_pct": 38.2,
        "day1_return_pct": 48.4,
        "day1_high_pct": 70.0,
        "day5_return_pct": -12.0,
        "week1_return_pct": -12.0,
        "month1_return_pct": -22.0,
        "volume_day1_m": 75,
        "orb_5m_return_pct": 15.0,
        "vwap_reclaim_day1": True,
        "fvg_day1": False,
        "market_cap_bn": 9.0,
        "sector": "tech_consumer",
        "relevance": "moderate",  # different sector but similar hype
    },
    "TSLA": {
        "name": "Tesla",
        "category": "automotive",
        "ipo_date": "2010-06-29",
        "ipo_price": 17.0,
        "open": 19.0,
        "day1_close": 23.89,
        "day1_gap_pct": 11.8,
        "day1_return_pct": 40.5,
        "day1_high_pct": 43.0,
        "day5_return_pct": 5.3,
        "week1_return_pct": 5.3,
        "month1_return_pct": 14.1,
        "volume_day1_m": 20,
        "orb_5m_return_pct": 12.0,
        "vwap_reclaim_day1": True,
        "fvg_day1": True,
        "market_cap_bn": 560.0,
        "sector": "tech_hardware",
        "relevance": "highly_relevant",
    },
    "SNOW": {
        "name": "Snowflake",
        "category": "saas",
        "ipo_date": "2020-09-16",
        "ipo_price": 120.0,
        "open": 245.0,
        "day1_close": 253.93,
        "day1_gap_pct": 104.2,
        "day1_return_pct": 111.6,
        "day1_high_pct": 165.0,
        "day5_return_pct": -15.0,
        "week1_return_pct": -15.0,
        "month1_return_pct": -20.0,
        "volume_day1_m": 45,
        "orb_5m_return_pct": 30.0,
        "vwap_reclaim_day1": False,
        "fvg_day1": False,
        "market_cap_bn": 70.0,
        "sector": "tech_saas",
        "relevance": "moderate",  # extreme gap, not typical
    },
    "PLTR": {
        "name": "Palantir",
        "category": "data_analytics",
        "ipo_date": "2020-09-30",
        "ipo_price": 10.0,
        "open": 10.0,
        "day1_close": 9.50,
        "day1_gap_pct": 0.0,
        "day1_return_pct": -5.0,
        "day1_high_pct": 8.0,
        "day5_return_pct": 2.3,
        "week1_return_pct": 2.3,
        "month1_return_pct": -8.0,
        "volume_day1_m": 120,
        "orb_5m_return_pct": 3.0,
        "vwap_reclaim_day1": False,
        "fvg_day1": False,
        "market_cap_bn": 22.0,
        "sector": "tech_defense",
        "relevance": "highly_relevant",  # DPO, defense/aerospace adjacent
    },
    "COIN": {
        "name": "Coinbase",
        "category": "crypto_exchange",
        "ipo_date": "2021-04-14",
        "ipo_price": 250.0,
        "open": 381.0,
        "day1_close": 328.28,
        "day1_gap_pct": 52.4,
        "day1_return_pct": 31.3,
        "day1_high_pct": 72.0,
        "day5_return_pct": -12.0,
        "week1_return_pct": -12.0,
        "month1_return_pct": -25.0,
        "volume_day1_m": 100,
        "orb_5m_return_pct": 18.0,
        "vwap_reclaim_day1": False,
        "fvg_day1": True,
        "market_cap_bn": 65.0,
        "sector": "tech_fintech",
        "relevance": "moderate",  # DPO model, high hype
    },
    "HOOD": {
        "name": "Robinhood",
        "category": "fintech",
        "ipo_date": "2021-07-29",
        "ipo_price": 38.0,
        "open": 38.0,
        "day1_close": 34.82,
        "day1_gap_pct": 0.0,
        "day1_return_pct": -8.4,
        "day1_high_pct": 2.0,
        "day5_return_pct": 5.1,
        "week1_return_pct": 5.1,
        "month1_return_pct": 35.0,
        "volume_day1_m": 55,
        "orb_5m_return_pct": -2.0,
        "vwap_reclaim_day1": False,
        "fvg_day1": False,
        "market_cap_bn": 32.0,
        "sector": "tech_fintech",
        "relevance": "moderate",
    },
    "ABNB": {
        "name": "Airbnb",
        "category": "travel",
        "ipo_date": "2020-12-10",
        "ipo_price": 68.0,
        "open": 146.0,
        "day1_close": 144.71,
        "day1_gap_pct": 114.7,
        "day1_return_pct": 112.8,
        "day1_high_pct": 142.0,
        "day5_return_pct": -8.0,
        "week1_return_pct": -8.0,
        "month1_return_pct": -15.0,
        "volume_day1_m": 55,
        "orb_5m_return_pct": 25.0,
        "vwap_reclaim_day1": False,
        "fvg_day1": True,
        "market_cap_bn": 86.0,
        "sector": "tech_consumer",
        "relevance": "moderate",
    },
    "META": {
        "name": "Meta / Facebook",
        "category": "social_media",
        "ipo_date": "2012-05-18",
        "ipo_price": 38.0,
        "open": 42.05,
        "day1_close": 38.23,
        "day1_gap_pct": 10.7,
        "day1_return_pct": 0.6,
        "day1_high_pct": 18.0,
        "day5_return_pct": -15.0,
        "week1_return_pct": -15.0,
        "month1_return_pct": -30.0,
        "volume_day1_m": 80,
        "orb_5m_return_pct": 5.0,
        "vwap_reclaim_day1": False,
        "fvg_day1": False,
        "market_cap_bn": 104.0,
        "sector": "tech_consumer",
        "relevance": "moderate",
    },
    "RBLX": {
        "name": "Roblox",
        "category": "gaming",
        "ipo_date": "2021-03-10",
        "ipo_price": 45.0,
        "open": 69.50,
        "day1_close": 69.50,
        "day1_gap_pct": 54.4,
        "day1_return_pct": 54.4,
        "day1_high_pct": 58.0,
        "day5_return_pct": 10.0,
        "week1_return_pct": 10.0,
        "month1_return_pct": 20.0,
        "volume_day1_m": 60,
        "orb_5m_return_pct": 20.0,
        "vwap_reclaim_day1": True,
        "fvg_day1": True,
        "market_cap_bn": 38.0,
        "sector": "tech_consumer",
        "relevance": "moderate",
    },
}


def compute_analog_score(spcx_metrics: dict) -> dict:
    gap_pct = spcx_metrics.get("gap_pct", 0) or 0
    rel_vol = spcx_metrics.get("relative_volume", 1) or 1
    has_fvg = spcx_metrics.get("fvg_bullish", False)
    has_bos = spcx_metrics.get("bos", False)
    vwap_dist = spcx_metrics.get("vwap_distance_pct", 0) or 0

    rankings: list[dict] = []
    for symbol, data in IPO_ANALOGS.items():
        score = 0.0
        score += max(0, 30 - abs(gap_pct - data["day1_gap_pct"]) * 2)
        score += max(0, 20 - abs(rel_vol - (data.get("volume_day1_m", 50) / 50)) * 5)
        if has_fvg == data.get("fvg_day1", False):
            score += 15
        if has_bos == (data.get("orb_5m_return_pct", 0) > 10):
            score += 10
        if data["relevance"] == "highly_relevant":
            score *= 1.3
        cap_match = 10 if abs((spcx_metrics.get("ipo_price", 135) - data["ipo_price"]) / max(1, data["ipo_price"])) < 0.5 else 0
        score += cap_match
        sector_bonus = 10 if data["sector"] in ("tech_hardware", "tech_defense", "tech_aerospace") else 0
        score += sector_bonus
        rankings.append({"symbol": symbol, "name": data["name"], "score": round(score, 1), "day1_return": data["day1_return_pct"], "day1_gap": data["day1_gap_pct"], "orb_5m": data["orb_5m_return_pct"], "sector": data["sector"]})

    rankings.sort(key=lambda x: x["score"], reverse=True)
    total = sum(r["score"] for r in rankings) or 1

    top3 = rankings[:3]
    probabilities = {r["symbol"]: round(r["score"] / total * 100, 1) for r in top3}

    return {
        "top_match": top3[0] if top3 else None,
        "top3": top3,
        "probabilities": probabilities,
        "analog_consensus": _analog_consensus(top3),
        "rankings": rankings,
    }


def _analog_consensus(top3: list[dict]) -> dict:
    if not top3:
        return {}
    avg_day1 = sum(r["day1_return"] for r in top3) / len(top3)
    avg_orb = sum(r["orb_5m"] for r in top3) / len(top3)
    setups_likely = []
    if avg_orb > 5:
        setups_likely.append("IPO_ORB_5M")
    if avg_day1 > 10:
        setups_likely.append("GAP_AND_GO")
    if avg_day1 > 0:
        setups_likely.append("VWAP_RECLAIM")
    if avg_day1 > 20:
        setups_likely.append("HIGH_VOLUME_CONTINUATION")
    return {
        "avg_day1_return_pct": round(avg_day1, 1),
        "avg_orb_5m_return_pct": round(avg_orb, 1),
        "likely_setups": setups_likely,
        "direction": "BULLISH" if avg_day1 > 0 else "BEARISH",
    }
