from __future__ import annotations
from typing import Any

SECTOR_WATCH = {
    "space_stocks": {
        "tickers": ["RKLB", "ASTS", "RDW", "LUNR", "PL"],
        "label": "Space Pure Play",
        "weight": 0.30,
    },
    "space_adjacent": {
        "tickers": ["TSLA", "NVDA"],
        "label": "Space Adjacent (Halo)",
        "weight": 0.20,
    },
    "space_etfs": {
        "tickers": ["ARKX", "UFO", "ITA", "XAR"],
        "label": "Space ETFs & Defense",
        "weight": 0.25,
    },
    "broad_market": {
        "tickers": ["QQQ", "SPY", "IWM"],
        "label": "Broad Market Indexes",
        "weight": 0.25,
    },
}


SECTOR_TICKER_INFO = {
    "RKLB": {"name": "Rocket Lab", "sector": "space_launch", "notes": "Small satellite launch competitor"},
    "ASTS": {"name": "AST SpaceMobile", "sector": "space_comm", "notes": "Direct-to-cell broadband constellation"},
    "RDW": {"name": "Redwire", "sector": "space_infra", "notes": "Space infrastructure and manufacturing"},
    "LUNR": {"name": "Intuitive Machines", "sector": "space_lunar", "notes": "Lunar lander/exploration"},
    "PL": {"name": "Planet Labs", "sector": "space_imaging", "notes": "Earth imaging satellite constellation"},
    "TSLA": {"name": "Tesla", "sector": "auto_tech", "notes": "Elon Musk halo stock"},
    "NVDA": {"name": "NVIDIA", "sector": "semiconductors", "notes": "AI/GPU — space-adjacent demand"},
    "ARKX": {"name": "ARK Space ETF", "sector": "etf", "notes": "Space Exploration ETF"},
    "UFO": {"name": "Procure Space ETF", "sector": "etf", "notes": "Space ETF"},
    "ITA": {"name": "iShares Aerospace & Defense", "sector": "etf", "notes": "Aerospace & Defense ETF"},
    "XAR": {"name": "SPDR Aerospace & Defense", "sector": "etf", "notes": "Aerospace & Defense ETF"},
    "QQQ": {"name": "Nasdaq 100 ETF", "sector": "broad_market", "notes": "Tech-heavy benchmark"},
    "SPY": {"name": "S&P 500 ETF", "sector": "broad_market", "notes": "Broad market benchmark"},
    "IWM": {"name": "Russell 2000 ETF", "sector": "broad_market", "notes": "Small-cap benchmark"},
}


def compute_sector_intelligence(
    spcx_gap_pct: float,
    spcx_volume_class: str,
    spcx_scoring: dict[str, float],
) -> dict[str, Any]:
    groups = {}
    for group_name, group_data in SECTOR_WATCH.items():
        tickers = group_data["tickers"]
        entries = []
        for t in tickers:
            info = SECTOR_TICKER_INFO.get(t, {})
            entries.append({
                "ticker": t,
                "name": info.get("name", t),
                "sector": info.get("sector", "unknown"),
                "notes": info.get("notes", ""),
                "tracking": True,
            })
        groups[group_name] = {
            "label": group_data["label"],
            "weight": group_data["weight"],
            "tickers": entries,
            "count": len(entries),
        }

    risk_flags = []
    if spcx_volume_class in ("EXPLOSIVE", "ELEVATED"):
        risk_flags.append("HIGH_VOLUME_REGIME — sector rotation possible")
    if spcx_gap_pct and spcx_gap_pct > 20:
        risk_flags.append("EXTREME_GAP — expect volatility across space sector")
    if spcx_gap_pct and spcx_gap_pct < 0:
        risk_flags.append("NEGATIVE_OPEN — watch for sector contagion")

    return {
        "generated_at": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
        "watch_groups": groups,
        "total_tickers": sum(len(g["tickers"]) for g in groups.values()),
        "recommended_trackers": ["RKLB", "ASTS", "ARKX", "QQQ"],
        "risk_flags": risk_flags,
        "lead_lag_hypothesis": {
            "if_spcx_gap_positive": "Expect RKLB/ASTS to follow with 1-5 min lag",
            "if_spcx_gap_negative": "Space ETFs (ARKX/UFO) may fade first",
            "if_spcx_high_vol": "Watch TSLA/NVDA for institutional rotation signals",
        },
    }


def sector_summary() -> dict[str, Any]:
    return {
        "universe": "14 tickers across 4 groups",
        "groups": list(SECTOR_WATCH.keys()),
        "primary_benchmarks": ["SPY", "QQQ", "ARKX"],
        "correlation_hypothesis": "Space stocks show high intraday correlation during catalyst events (launches, contracts, earnings). SPCX is expected to lead the sector on IPO day.",
    }
