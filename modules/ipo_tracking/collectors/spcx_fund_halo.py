"""
SPCX Fund/ETF Exposure + Sector Halo Scoring (P2)
GO_SPACEX_P2_FUND_ETF_AND_HALO_01

Tracks indirect SPCX exposure via ETFs/funds + scores sector peers.
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]

# Known SPCX exposure vectors
FUND_EXPOSURE = {
    "GOOGL": {
        "note": "Alphabet invested $900M in SpaceX (2015). Stake revalued post-IPO.",
        "exposure_type": "direct_equity_stake",
        "estimated_pct": 7.5,
    },
    "ARKX": {
        "note": "Space Exploration ETF. May add SPCX at next rebalance.",
        "exposure_type": "etf_potential",
        "estimated_pct": None,
    },
    "UFO": {
        "note": "Procure Space ETF. Tracks space economy.",
        "exposure_type": "etf_potential",
        "estimated_pct": None,
    },
    "QQQ": {
        "note": "Nasdaq-100. SPCX inclusion possible if market cap qualifies.",
        "exposure_type": "index_potential",
        "estimated_pct": None,
    },
    "XAR": {
        "note": "SPDR Aerospace & Defense ETF.",
        "exposure_type": "sector_etf",
        "estimated_pct": None,
    },
    "ITA": {
        "note": "iShares US Aerospace & Defense ETF.",
        "exposure_type": "sector_etf",
        "estimated_pct": None,
    },
}

HALO_TICKERS = {
    "RKLB": {"role": "space_peer_direct", "weight": 0.25},
    "ASTS": {"role": "space_satellite", "weight": 0.20},
    "LUNR": {"role": "space_infra", "weight": 0.15},
    "RDW":  {"role": "space_infra", "weight": 0.15},
    "TSLA": {"role": "musk_halo", "weight": 0.15},
    "QQQ":  {"role": "market_regime", "weight": 0.10},
}


def collect_fund_exposure() -> dict[str, Any]:
    return {
        "source": "spcx_fund_etf_exposure",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "available": True,
        "exposures": FUND_EXPOSURE,
        "direct_stake_holders": ["GOOGL"],
        "potential_etf_inclusions": ["ARKX", "UFO", "XAR", "ITA"],
        "potential_index_inclusions": ["QQQ"],
        "note": "Check ETF holdings weekly for SPCX additions. GOOGL stake is pre-IPO, may have changed.",
    }


def compute_sector_halo_score(spcx_price: float | None = None) -> dict[str, Any]:
    """Score sector halo from existing DOM captures of comparable symbols."""
    vision_dir = REPO_ROOT / "data" / "vision_inbox"
    peers = {}

    for sym in HALO_TICKERS:
        pattern = sym.lower()
        for f in sorted(vision_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True) if vision_dir.exists() else []:
            if pattern in f.name.lower() and "tradingview" in f.name.lower() and f.name.endswith(".json"):
                try:
                    data = json.loads(f.read_text())
                    dom = data.get("dom_extracted", {})
                    if dom and isinstance(dom, dict):
                        close = _parse(dom.get("close"))
                        if close:
                            peers[sym] = {
                                "close": close,
                                "open": _parse(dom.get("open")),
                                "high": _parse(dom.get("high")),
                                "low": _parse(dom.get("low")),
                                "volume": dom.get("volume"),
                                "role": HALO_TICKERS[sym]["role"],
                                "weight": HALO_TICKERS[sym]["weight"],
                                "captured_at": str(datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)),
                            }
                except Exception:
                    pass
                break

    # Score: count peers with DOM data
    score = len(peers) / len(HALO_TICKERS) if HALO_TICKERS else 0
    roles_found = set(p["role"] for p in peers.values())

    return {
        "source": "spcx_sector_halo",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "available": len(peers) > 0,
        "peer_count": len(peers),
        "total_peers": len(HALO_TICKERS),
        "coverage_score": round(score, 2),
        "roles_covered": sorted(roles_found),
        "peers": peers,
        "spcx_reference_price": spcx_price,
    }


def _parse(v: Any) -> float | None:
    if v is None: return None
    try: return float(str(v).replace(",", "").replace("$", ""))
    except: return None
