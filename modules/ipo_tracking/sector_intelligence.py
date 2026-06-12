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


def compute_correlation_matrix(prices: dict[str, list[float]]) -> dict[str, Any]:
    tickers = sorted(prices.keys())
    if len(tickers) < 2:
        return {"ok": False, "error": "need at least 2 tickers", "matrix": {}}

    matrix: dict[str, dict[str, float]] = {}
    for t1 in tickers:
        matrix[t1] = {}
        p1 = prices[t1]
        for t2 in tickers:
            if t1 == t2:
                matrix[t1][t2] = 1.0
                continue
            if t2 in matrix and t1 in matrix[t2]:
                matrix[t1][t2] = matrix[t2][t1]
                continue
            p2 = prices[t2]
            corr = _pearson(p1, p2)
            matrix[t1][t2] = corr

    high_corr = []
    for t1 in tickers:
        for t2 in tickers:
            if t1 < t2 and abs(matrix[t1].get(t2, 0)) > 0.7:
                high_corr.append({"pair": f"{t1}-{t2}", "correlation": round(matrix[t1][t2], 3)})

    high_corr.sort(key=lambda x: abs(x["correlation"]), reverse=True)

    return {
        "ok": True,
        "tickers": tickers,
        "matrix": {t: {t2: round(v, 3) for t2, v in row.items()} for t, row in matrix.items()},
        "high_correlations": high_corr[:10],
        "avg_correlation": round(sum(matrix[t1].get(t2, 0) for t1 in tickers for t2 in tickers if t1 < t2) / max(1, len(tickers) * (len(tickers) - 1) / 2), 3),
    }


def detect_lead_lag(leader_prices: list[float], follower_prices: list[float], max_lag: int = 10) -> dict[str, Any]:
    if len(leader_prices) < max_lag + 5 or len(follower_prices) < max_lag + 5:
        return {"ok": False, "error": "insufficient data"}

    leader_returns = [((leader_prices[i] - leader_prices[i - 1]) / max(0.01, abs(leader_prices[i - 1]))) for i in range(1, len(leader_prices))]
    follower_returns = [((follower_prices[i] - follower_prices[i - 1]) / max(0.01, abs(follower_prices[i - 1]))) for i in range(1, len(follower_prices))]

    best_lag = 0
    best_corr = 0.0
    correlations = []

    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            l_slice = leader_returns[-lag:]
            f_slice = follower_returns[:len(l_slice)]
        elif lag > 0:
            f_slice = follower_returns[lag:]
            l_slice = leader_returns[:len(f_slice)]
        else:
            l_slice = leader_returns
            f_slice = follower_returns

        if len(l_slice) < 3 or len(f_slice) < 3:
            correlations.append(0.0)
            continue

        min_len = min(len(l_slice), len(f_slice))
        corr = _pearson(l_slice[:min_len], f_slice[:min_len])
        correlations.append(round(corr, 3))
        if abs(corr) > abs(best_corr):
            best_corr = corr
            best_lag = lag

    return {
        "ok": True,
        "best_lag_bars": best_lag,
        "best_correlation": round(best_corr, 3),
        "relationship": "leader" if best_lag < 0 else ("follower" if best_lag > 0 else "synchronous"),
        "lag_description": f"leader leads by {abs(best_lag)} bars" if best_lag < 0 else (f"follower lags by {best_lag} bars" if best_lag > 0 else "moves synchronously"),
        "correlations_by_lag": correlations,
    }


def compute_relative_strength(prices: dict[str, float], benchmark: str = "SPY", changes: dict[str, float] | None = None) -> dict[str, Any]:
    changes = changes or {}
    benchmark_change = changes.get(benchmark, 0.0)

    rankings = []
    for ticker, price in prices.items():
        if ticker == benchmark:
            continue
        chg = changes.get(ticker, 0.0)
        rs = round(chg - benchmark_change, 2)
        rankings.append({
            "ticker": ticker,
            "price": round(price, 2) if price else None,
            "change_pct": round(chg, 2),
            "relative_strength": rs,
            "vs_benchmark": benchmark,
            "grade": "STRONG" if rs > 2 else ("MODERATE" if rs > 0 else ("WEAK" if rs > -2 else "VERY_WEAK")),
        })

    rankings.sort(key=lambda x: x["relative_strength"], reverse=True)

    leaders = [r for r in rankings if r["grade"] == "STRONG"]
    laggards = [r for r in rankings if r["grade"] == "VERY_WEAK"]

    return {
        "ok": True,
        "benchmark": benchmark,
        "benchmark_change_pct": round(benchmark_change, 2),
        "rankings": rankings,
        "leaders": [r["ticker"] for r in leaders],
        "laggards": [r["ticker"] for r in laggards],
        "breadth": round(len(leaders) / max(1, len(rankings)) * 100, 1),
    }


def detect_capital_rotation(flows: dict[str, float]) -> dict[str, Any]:
    total = sum(abs(v) for v in flows.values()) or 1
    entries = []
    for sector, flow in sorted(flows.items(), key=lambda x: abs(x[1]), reverse=True):
        entries.append({
            "sector": sector,
            "flow": round(flow, 2),
            "flow_pct": round(abs(flow) / total * 100, 1),
            "direction": "INFLOW" if flow > 0 else "OUTFLOW",
            "intensity": "HIGH" if abs(flow) / max(1, total) > 0.3 else ("MEDIUM" if abs(flow) / max(1, total) > 0.1 else "LOW"),
        })

    inflow_sectors = [e["sector"] for e in entries if e["direction"] == "INFLOW"]
    outflow_sectors = [e["sector"] for e in entries if e["direction"] == "OUTFLOW"]

    rotation_detected = len(inflow_sectors) > 0 and len(outflow_sectors) > 0

    return {
        "ok": True,
        "rotation_detected": rotation_detected,
        "inflow_sectors": inflow_sectors,
        "outflow_sectors": outflow_sectors,
        "dominant_flow": entries[0] if entries else None,
        "flows": entries,
    }


def compute_sector_health(prices: dict[str, float], changes: dict[str, float]) -> dict[str, Any]:
    group_scores = {}
    for group_name, group_data in SECTOR_WATCH.items():
        tickers = group_data["tickers"]
        available_changes = [changes.get(t, 0) for t in tickers if t in changes]
        if not available_changes:
            group_scores[group_name] = {"label": group_data["label"], "score": 0, "signal": "NO_DATA", "tickers_available": 0}
            continue
        avg_change = sum(available_changes) / len(available_changes)
        signal = "BULLISH" if avg_change > 1 else ("BEARISH" if avg_change < -1 else "NEUTRAL")
        group_scores[group_name] = {
            "label": group_data["label"],
            "score": round(avg_change, 2),
            "signal": signal,
            "tickers_available": len(available_changes),
            "tickers_total": len(tickers),
        }

    overall_bullish = sum(1 for g in group_scores.values() if g["signal"] == "BULLISH")
    overall_bearish = sum(1 for g in group_scores.values() if g["signal"] == "BEARISH")
    regime = "RISK_ON" if overall_bullish > overall_bearish else ("RISK_OFF" if overall_bearish > overall_bullish else "NEUTRAL")

    return {
        "ok": True,
        "regime": regime,
        "bullish_groups": overall_bullish,
        "bearish_groups": overall_bearish,
        "groups": group_scores,
    }


def _pearson(a: list[float], b: list[float]) -> float:
    n = min(len(a), len(b))
    if n < 3:
        return 0.0
    a = a[:n]
    b = b[:n]
    ma = sum(a) / n
    mb = sum(b) / n
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    da = (sum((x - ma) ** 2 for x in a)) ** 0.5
    db = (sum((x - mb) ** 2 for x in b)) ** 0.5
    return num / (da * db) if da and db else 0.0
