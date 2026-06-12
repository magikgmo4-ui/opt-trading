from __future__ import annotations
from dataclasses import dataclass, field
from statistics import mean, stdev
from typing import Any


@dataclass
class IPORecord:
    symbol: str
    name: str
    sector: str
    category: str
    ipo_date: str
    ipo_price: float
    market_cap_bn: float

    d1_open: float
    d1_high: float
    d1_low: float
    d1_close: float
    d1_volume_m: float
    d1_gap_pct: float
    d1_return_pct: float
    d1_high_pct: float
    d1_low_pct: float
    d1_close_vs_open_pct: float
    d1_close_vs_ipo_pct: float

    d1_rel_vol: float = 1.0
    d1_vwap: float = 0.0
    d1_vwap_dist_pct: float = 0.0
    d1_atr: float = 0.0
    d1_range_pct: float = 0.0

    d1_orb_5m_high: float = 0.0
    d1_orb_5m_low: float = 0.0
    d1_orb_5m_return_pct: float = 0.0
    d1_orb_15m_high: float = 0.0
    d1_orb_15m_low: float = 0.0
    d1_orb_15m_return_pct: float = 0.0

    d1_fvg_bullish: bool = False
    d1_fvg_bearish: bool = False
    d1_bos: bool = False
    d1_vwap_reclaim: bool = False

    d2_return_pct: float = 0.0
    d2_continuation: bool = False
    d2_reversal: bool = False
    d2_fade: bool = False

    w1_return_pct: float = 0.0
    w1_volatility_pct: float = 0.0
    w1_max_dd_pct: float = 0.0
    w1_max_runup_pct: float = 0.0

    m1_return_pct: float = 0.0
    m1_volatility_pct: float = 0.0
    m1_max_dd_pct: float = 0.0
    m1_max_runup_pct: float = 0.0

    relevance: str = "moderate"    # highly_relevant, moderate, low


IPO_DATASET: list[IPORecord] = [
    IPORecord("ARM", "ARM Holdings", "semiconductors", "tech_hardware", "2023-09-14", 51.0, 54.5,
              56.10, 66.30, 55.50, 63.59, 50, 10.0, 24.7, 30.0, 8.8, 13.3, 24.7,
              d1_rel_vol=2.5, d1_vwap_reclaim=True, d1_fvg_bullish=True, d1_bos=True, d1_range_pct=21.2,
              d1_orb_5m_return_pct=8.0, d1_orb_15m_return_pct=11.0,
              d2_return_pct=-2.1, d2_continuation=False, d2_fade=True,
              w1_return_pct=3.2, w1_max_dd_pct=-8.0, w1_max_runup_pct=10.0,
              m1_return_pct=-5.1, m1_max_dd_pct=-15.0, m1_max_runup_pct=15.0,
              relevance="highly_relevant"),

    IPORecord("RDDT", "Reddit", "social_media", "tech_consumer", "2024-03-21", 34.0, 9.0,
              47.0, 57.80, 46.50, 50.44, 75, 38.2, 48.4, 70.0, 26.5, 7.3, 48.4,
              d1_rel_vol=3.5, d1_vwap_reclaim=True, d1_fvg_bullish=False, d1_range_pct=24.3,
              d1_orb_5m_return_pct=15.0, d1_orb_15m_return_pct=12.0,
              d2_return_pct=-8.0, d2_reversal=True,
              w1_return_pct=-12.0, w1_max_dd_pct=-22.0, w1_max_runup_pct=8.0,
              m1_return_pct=-22.0, m1_max_dd_pct=-38.0, m1_max_runup_pct=12.0,
              relevance="moderate"),

    IPORecord("TSLA", "Tesla", "automotive", "tech_hardware", "2010-06-29", 17.0, 560.0,
              19.0, 24.30, 18.50, 23.89, 20, 11.8, 40.5, 43.0, 8.8, 25.7, 40.5,
              d1_rel_vol=1.8, d1_vwap_reclaim=True, d1_fvg_bullish=True, d1_bos=True, d1_range_pct=31.4,
              d1_orb_5m_return_pct=12.0, d1_orb_15m_return_pct=8.0,
              d2_return_pct=3.1, d2_continuation=True,
              w1_return_pct=5.3, w1_max_dd_pct=-5.0, w1_max_runup_pct=15.0,
              m1_return_pct=14.1, m1_max_dd_pct=-10.0, m1_max_runup_pct=25.0,
              relevance="highly_relevant"),

    IPORecord("SNOW", "Snowflake", "saas", "tech_saas", "2020-09-16", 120.0, 70.0,
              245.0, 319.00, 220.00, 253.93, 45, 104.2, 111.6, 165.0, 31.7, 3.6, 111.6,
              d1_rel_vol=4.0, d1_vwap_reclaim=False, d1_fvg_bullish=False, d1_range_pct=42.9,
              d1_orb_5m_return_pct=30.0, d1_orb_15m_return_pct=15.0,
              d2_return_pct=-10.0, d2_reversal=True,
              w1_return_pct=-15.0, w1_max_dd_pct=-25.0, w1_max_runup_pct=5.0,
              m1_return_pct=-20.0, m1_max_dd_pct=-35.0, m1_max_runup_pct=8.0,
              relevance="low"),

    IPORecord("PLTR", "Palantir", "data_analytics", "tech_defense", "2020-09-30", 10.0, 22.0,
              10.0, 10.80, 9.30, 9.50, 120, 0.0, -5.0, 8.0, -7.0, -5.0, -5.0,
              d1_rel_vol=5.0, d1_vwap_reclaim=False, d1_fvg_bullish=False, d1_range_pct=16.1,
              d1_orb_5m_return_pct=3.0, d1_orb_15m_return_pct=-1.0,
              d2_return_pct=1.2, d2_continuation=True,
              w1_return_pct=2.3, w1_max_dd_pct=-10.0, w1_max_runup_pct=8.0,
              m1_return_pct=-8.0, m1_max_dd_pct=-20.0, m1_max_runup_pct=12.0,
              relevance="highly_relevant"),

    IPORecord("COIN", "Coinbase", "crypto_exchange", "tech_fintech", "2021-04-14", 250.0, 65.0,
              381.0, 429.54, 310.00, 328.28, 100, 52.4, 31.3, 72.0, 24.0, -13.8, 31.3,
              d1_rel_vol=3.0, d1_vwap_reclaim=False, d1_fvg_bullish=True, d1_bos=True, d1_range_pct=38.5,
              d1_orb_5m_return_pct=18.0, d1_orb_15m_return_pct=8.0,
              d2_return_pct=-5.0, d2_reversal=True,
              w1_return_pct=-12.0, w1_max_dd_pct=-25.0, w1_max_runup_pct=10.0,
              m1_return_pct=-25.0, m1_max_dd_pct=-40.0, m1_max_runup_pct=15.0,
              relevance="moderate"),

    IPORecord("HOOD", "Robinhood", "fintech", "tech_fintech", "2021-07-29", 38.0, 32.0,
              38.0, 38.80, 34.00, 34.82, 55, 0.0, -8.4, 2.0, -10.5, -8.4, -8.4,
              d1_rel_vol=2.8, d1_vwap_reclaim=False, d1_fvg_bullish=False, d1_range_pct=14.1,
              d1_orb_5m_return_pct=-2.0, d1_orb_15m_return_pct=-4.0,
              d2_return_pct=3.0, d2_continuation=True,
              w1_return_pct=5.1, w1_max_dd_pct=-12.0, w1_max_runup_pct=10.0,
              m1_return_pct=35.0, m1_max_dd_pct=-15.0, m1_max_runup_pct=40.0,
              relevance="moderate"),

    IPORecord("ABNB", "Airbnb", "travel", "tech_consumer", "2020-12-10", 68.0, 86.0,
              146.0, 165.00, 130.00, 144.71, 55, 114.7, 112.8, 142.0, 91.0, -0.9, 112.8,
              d1_rel_vol=3.2, d1_vwap_reclaim=False, d1_fvg_bullish=True, d1_range_pct=26.9,
              d1_orb_5m_return_pct=25.0, d1_orb_15m_return_pct=10.0,
              d2_return_pct=-3.0, d2_fade=True,
              w1_return_pct=-8.0, w1_max_dd_pct=-20.0, w1_max_runup_pct=12.0,
              m1_return_pct=-15.0, m1_max_dd_pct=-28.0, m1_max_runup_pct=15.0,
              relevance="low"),

    IPORecord("META", "Meta (Facebook)", "social_media", "tech_consumer", "2012-05-18", 38.0, 104.0,
              42.05, 45.00, 38.00, 38.23, 80, 10.7, 0.6, 18.0, -2.6, -9.1, 0.6,
              d1_rel_vol=2.0, d1_vwap_reclaim=False, d1_fvg_bullish=False, d1_range_pct=18.4,
              d1_orb_5m_return_pct=5.0, d1_orb_15m_return_pct=2.0,
              d2_return_pct=-11.0, d2_reversal=True,
              w1_return_pct=-15.0, w1_max_dd_pct=-20.0, w1_max_runup_pct=3.0,
              m1_return_pct=-30.0, m1_max_dd_pct=-35.0, m1_max_runup_pct=5.0,
              relevance="moderate"),

    IPORecord("RBLX", "Roblox", "gaming", "tech_consumer", "2021-03-10", 45.0, 38.0,
              69.50, 74.50, 67.00, 69.50, 60, 54.4, 54.4, 65.0, 49.0, 0.0, 54.4,
              d1_rel_vol=3.0, d1_vwap_reclaim=True, d1_fvg_bullish=True, d1_bos=True, d1_range_pct=11.2,
              d1_orb_5m_return_pct=20.0, d1_orb_15m_return_pct=12.0,
              d2_return_pct=5.0, d2_continuation=True,
              w1_return_pct=10.0, w1_max_dd_pct=-8.0, w1_max_runup_pct=18.0,
              m1_return_pct=20.0, m1_max_dd_pct=-12.0, m1_max_runup_pct=28.0,
              relevance="moderate"),

    IPORecord("UBER", "Uber", "ride_hailing", "tech_consumer", "2019-05-10", 45.0, 75.0,
              42.0, 43.00, 41.06, 41.57, 100, -6.7, -7.6, -4.4, -8.9, -1.0, -7.6,
              d1_rel_vol=3.8, d1_vwap_reclaim=False, d1_fvg_bullish=False, d1_range_pct=4.7,
              d1_orb_5m_return_pct=-2.0, d1_orb_15m_return_pct=-3.0,
              d2_return_pct=-1.0, d2_continuation=False, d2_fade=True,
              w1_return_pct=-8.0, w1_max_dd_pct=-15.0, w1_max_runup_pct=2.0,
              m1_return_pct=-5.0, m1_max_dd_pct=-18.0, m1_max_runup_pct=5.0,
              relevance="moderate"),

    IPORecord("LYFT", "Lyft", "ride_hailing", "tech_consumer", "2019-03-29", 72.0, 24.0,
              87.24, 88.60, 78.00, 78.29, 65, 21.2, 8.7, 23.1, 8.3, -10.3, 8.7,
              d1_rel_vol=3.0, d1_vwap_reclaim=False, d1_fvg_bullish=False, d1_range_pct=13.3,
              d1_orb_5m_return_pct=5.0, d1_orb_15m_return_pct=-2.0,
              d2_return_pct=-11.0, d2_reversal=True,
              w1_return_pct=-15.0, w1_max_dd_pct=-22.0, w1_max_runup_pct=2.0,
              m1_return_pct=-25.0, m1_max_dd_pct=-35.0, m1_max_runup_pct=3.0,
              relevance="low"),

    IPORecord("PINS", "Pinterest", "social_media", "tech_consumer", "2019-04-18", 19.0, 12.0,
              23.75, 25.55, 23.30, 24.40, 35, 25.0, 28.4, 34.5, 22.6, 2.7, 28.4,
              d1_rel_vol=2.2, d1_vwap_reclaim=True, d1_fvg_bullish=True, d1_range_pct=9.6,
              d1_orb_5m_return_pct=10.0, d1_orb_15m_return_pct=5.0,
              d2_return_pct=-5.0, d2_reversal=True,
              w1_return_pct=-8.0, w1_max_dd_pct=-15.0, w1_max_runup_pct=5.0,
              m1_return_pct=-35.0, m1_max_dd_pct=-50.0, m1_max_runup_pct=5.0,
              relevance="low"),

    IPORecord("ZM", "Zoom", "video_conf", "tech_saas", "2019-04-18", 36.0, 9.0,
              65.0, 66.00, 62.00, 62.00, 20, 80.6, 72.2, 83.3, 72.2, -4.6, 72.2,
              d1_rel_vol=2.0, d1_vwap_reclaim=True, d1_fvg_bullish=True, d1_bos=True, d1_range_pct=6.5,
              d1_orb_5m_return_pct=15.0, d1_orb_15m_return_pct=8.0,
              d2_return_pct=3.0, d2_continuation=True,
              w1_return_pct=15.0, w1_max_dd_pct=-5.0, w1_max_runup_pct=20.0,
              m1_return_pct=25.0, m1_max_dd_pct=-10.0, m1_max_runup_pct=30.0,
              relevance="moderate"),

    IPORecord("SNAP", "Snapchat", "social_media", "tech_consumer", "2017-03-02", 17.0, 24.0,
              24.0, 26.05, 23.50, 24.48, 80, 41.2, 44.0, 53.2, 38.2, 2.0, 44.0,
              d1_rel_vol=2.5, d1_vwap_reclaim=True, d1_fvg_bullish=True, d1_bos=True, d1_range_pct=10.9,
              d1_orb_5m_return_pct=12.0, d1_orb_15m_return_pct=6.0,
              d2_return_pct=2.0, d2_continuation=True,
              w1_return_pct=8.0, w1_max_dd_pct=-8.0, w1_max_runup_pct=12.0,
              m1_return_pct=15.0, m1_max_dd_pct=-12.0, m1_max_runup_pct=20.0,
              relevance="moderate"),

    IPORecord("TWLO", "Twilio", "cloud_comm", "tech_saas", "2016-06-23", 15.0, 1.2,
              23.66, 29.86, 23.25, 28.79, 15, 57.7, 91.9, 99.1, 55.0, 21.7, 91.9,
              d1_rel_vol=2.0, d1_vwap_reclaim=True, d1_fvg_bullish=True, d1_bos=True, d1_range_pct=28.4,
              d1_orb_5m_return_pct=20.0, d1_orb_15m_return_pct=15.0,
              d2_return_pct=5.0, d2_continuation=True,
              w1_return_pct=12.0, w1_max_dd_pct=-8.0, w1_max_runup_pct=18.0,
              m1_return_pct=30.0, m1_max_dd_pct=-10.0, m1_max_runup_pct=35.0,
              relevance="low"),

    IPORecord("BYND", "Beyond Meat", "food_tech", "consumer", "2019-05-02", 25.0, 1.5,
              46.0, 72.95, 45.50, 65.75, 25, 84.0, 163.0, 191.8, 82.0, 42.9, 163.0,
              d1_rel_vol=3.0, d1_vwap_reclaim=True, d1_fvg_bullish=True, d1_bos=True, d1_range_pct=60.3,
              d1_orb_5m_return_pct=35.0, d1_orb_15m_return_pct=25.0,
              d2_return_pct=10.0, d2_continuation=True,
              w1_return_pct=20.0, w1_max_dd_pct=-10.0, w1_max_runup_pct=30.0,
              m1_return_pct=40.0, m1_max_dd_pct=-15.0, m1_max_runup_pct=50.0,
              relevance="low"),

    IPORecord("DASH", "DoorDash", "food_delivery", "tech_consumer", "2020-12-09", 102.0, 39.0,
              182.0, 195.50, 175.00, 189.51, 25, 78.4, 85.8, 91.7, 71.6, 4.1, 85.8,
              d1_rel_vol=2.5, d1_vwap_reclaim=True, d1_fvg_bullish=True, d1_range_pct=11.7,
              d1_orb_5m_return_pct=15.0, d1_orb_15m_return_pct=10.0,
              d2_return_pct=-3.0, d2_fade=True,
              w1_return_pct=-5.0, w1_max_dd_pct=-15.0, w1_max_runup_pct=5.0,
              m1_return_pct=-10.0, m1_max_dd_pct=-20.0, m1_max_runup_pct=8.0,
              relevance="low"),

    IPORecord("BMBL", "Bumble", "dating", "tech_consumer", "2021-02-11", 43.0, 8.0,
              76.0, 80.80, 70.31, 70.31, 25, 76.7, 63.5, 87.9, 63.5, -7.5, 63.5,
              d1_rel_vol=2.5, d1_vwap_reclaim=False, d1_fvg_bullish=True, d1_range_pct=14.9,
              d1_orb_5m_return_pct=12.0, d1_orb_15m_return_pct=3.0,
              d2_return_pct=-2.0, d2_fade=True,
              w1_return_pct=-5.0, w1_max_dd_pct=-15.0, w1_max_runup_pct=5.0,
              m1_return_pct=-15.0, m1_max_dd_pct=-25.0, m1_max_runup_pct=8.0,
              relevance="low"),

    IPORecord("AFRM", "Affirm", "fintech", "tech_fintech", "2021-01-13", 49.0, 12.0,
              90.90, 112.58, 87.00, 97.24, 15, 85.5, 98.5, 129.8, 77.6, 7.0, 98.5,
              d1_rel_vol=2.0, d1_vwap_reclaim=True, d1_fvg_bullish=True, d1_bos=True, d1_range_pct=29.4,
              d1_orb_5m_return_pct=22.0, d1_orb_15m_return_pct=15.0,
              d2_return_pct=5.0, d2_continuation=True,
              w1_return_pct=8.0, w1_max_dd_pct=-15.0, w1_max_runup_pct=12.0,
              m1_return_pct=-10.0, m1_max_dd_pct=-30.0, m1_max_runup_pct=15.0,
              relevance="low"),
]


def query_dataset(*,
    sector: str | None = None,
    category: str | None = None,
    relevance: str | None = None,
    min_gap_pct: float | None = None,
    max_gap_pct: float | None = None,
    min_return_pct: float | None = None,
    min_rel_vol: float | None = None,
    fvg_bullish: bool | None = None,
    bos: bool | None = None,
    limit: int = 20,
) -> list[IPORecord]:
    results = []
    for ipo in IPO_DATASET:
        if sector and ipo.sector != sector:
            continue
        if category and ipo.category != category:
            continue
        if relevance and ipo.relevance != relevance:
            continue
        if min_gap_pct is not None and ipo.d1_gap_pct < min_gap_pct:
            continue
        if max_gap_pct is not None and ipo.d1_gap_pct > max_gap_pct:
            continue
        if min_return_pct is not None and ipo.d1_return_pct < min_return_pct:
            continue
        if min_rel_vol is not None and ipo.d1_rel_vol < min_rel_vol:
            continue
        if fvg_bullish is not None and ipo.d1_fvg_bullish != fvg_bullish:
            continue
        if bos is not None and ipo.d1_bos != bos:
            continue
        results.append(ipo)
    return results[:limit]


def compute_analog_match(spcx_gap_pct: float, spcx_rel_vol: float, spcx_fvg: bool, spcx_bos: bool) -> dict[str, Any]:
    rankings = []
    for ipo in IPO_DATASET:
        score = 0.0
        score += max(0, 40 - abs(spcx_gap_pct - ipo.d1_gap_pct) * 2)
        score += max(0, 25 - abs(spcx_rel_vol - ipo.d1_rel_vol) * 5)
        if spcx_fvg == ipo.d1_fvg_bullish:
            score += 15
        if spcx_bos == ipo.d1_bos:
            score += 10
        sector_match = ipo.sector in ("semiconductors", "data_analytics", "automotive") and score > 0
        if sector_match:
            score *= 1.2
        if ipo.relevance == "highly_relevant":
            score *= 1.3
        rankings.append({"symbol": ipo.symbol, "name": ipo.name, "score": round(score, 1),
                         "d1_return": ipo.d1_return_pct, "d1_gap": ipo.d1_gap_pct,
                         "w1_return": ipo.w1_return_pct, "m1_return": ipo.m1_return_pct,
                         "orb_5m": ipo.d1_orb_5m_return_pct, "sector": ipo.sector})

    rankings.sort(key=lambda x: x["score"], reverse=True)
    total = sum(r["score"] for r in rankings) or 1

    top3 = rankings[:3]
    return {
        "top_match": top3[0] if top3 else None,
        "top3": top3,
        "probabilities": {r["symbol"]: round(r["score"] / total * 100, 1) for r in top3},
        "full_rankings": rankings,
    }


def dataset_stats(sector: str | None = None) -> dict[str, Any]:
    data = [r for r in IPO_DATASET if not sector or r.sector == sector]
    if not data:
        return {}
    d1_returns = [r.d1_return_pct for r in data]
    w1_returns = [r.w1_return_pct for r in data]
    m1_returns = [r.m1_return_pct for r in data]
    orb5 = [r.d1_orb_5m_return_pct for r in data if r.d1_orb_5m_return_pct]
    gaps = [r.d1_gap_pct for r in data]
    fvg_rate = sum(1 for r in data if r.d1_fvg_bullish) / len(data)
    bos_rate = sum(1 for r in data if r.d1_bos) / len(data)
    vwap_reclaim_rate = sum(1 for r in data if r.d1_vwap_reclaim) / len(data)
    continuation_rate = sum(1 for r in data if r.d2_continuation) / len(data)
    reversal_rate = sum(1 for r in data if r.d2_reversal) / len(data)
    return {
        "count": len(data),
        "sector": sector or "all",
        "d1_avg_return_pct": round(mean(d1_returns), 1),
        "d1_med_return_pct": round(sorted(d1_returns)[len(d1_returns) // 2], 1),
        "d1_max_return_pct": round(max(d1_returns), 1),
        "d1_min_return_pct": round(min(d1_returns), 1),
        "w1_avg_return_pct": round(mean(w1_returns), 1),
        "m1_avg_return_pct": round(mean(m1_returns), 1),
        "orb5_avg_return_pct": round(mean(orb5), 1) if orb5 else None,
        "avg_gap_pct": round(mean(gaps), 1),
        "fvg_bullish_rate": round(fvg_rate, 3),
        "bos_rate": round(bos_rate, 3),
        "vwap_reclaim_rate": round(vwap_reclaim_rate, 3),
        "d2_continuation_rate": round(continuation_rate, 3),
        "d2_reversal_rate": round(reversal_rate, 3),
    }
