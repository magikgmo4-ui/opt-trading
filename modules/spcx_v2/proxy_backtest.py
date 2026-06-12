"""SPCX V2 — Proxy IPO backtest: replay detector on historical IPO candles."""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from modules.spcx_v2.config import MarketSnapshot, PROJECT_ROOT
from modules.spcx_v2.setup_detector import detect
from modules.spcx_v2.paper_logger import log_candidate, log_reject, log_result, get_summary
from modules.spcx_v2.perf_calculator import (
    calculate_mfe,
    calculate_mae,
    calculate_r_multiple,
    compute_stats,
    compute_stats_by_setup,
    compute_stats_by_grade,
)
from shared.logger import setup_logger

logger = setup_logger("spcx_v2.proxy_backtest")

PROXY_SYMBOLS = [
    "RKLB", "ASTS", "RDW", "LUNR", "PL",
    "IONQ", "ARM", "RDDT", "COIN", "RIVN",
    "HOOD", "SNOW", "PLTR",
]


def load_csv(path: str) -> list[dict]:
    p = Path(path)
    if not p.exists():
        p = PROJECT_ROOT / path
    if not p.exists():
        logger.error("CSV not found: %s", path)
        return []

    rows = []
    with open(p, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def candle_to_snapshot(candle: dict, symbol: str, idx: int, prev_volume: float = 0) -> MarketSnapshot:
    o = float(candle.get("open", 0))
    h = float(candle.get("high", 0))
    l = float(candle.get("low", 0))
    c = float(candle.get("close", 0))
    vol = float(candle.get("volume", 0))
    vwap_val = float(candle.get("vwap", 0)) if candle.get("vwap") else None

    if vwap_val is None and (h + l + c) > 0:
        vwap_val = (h + l + c) / 3

    ts = candle.get("ts", candle.get("timestamp", candle.get("date", f"T+{idx:04d}")))

    rel_vol = (vol / prev_volume) if prev_volume > 0 else 1.0

    smc_structures = []
    if idx >= 1:
        smc_structures.append({"type": "BOS"})
    if rel_vol > 1.5:
        smc_structures.append({"type": "FVG_BULLISH"})

    spread_est = abs(h - l) / ((h + l) / 2) * 100 if (h + l) > 0 else 0

    return MarketSnapshot(
        symbol=symbol,
        timestamp=ts,
        price=c,
        price_status="live",
        bars_count=idx + 1,
        volume=int(vol),
        price_trust=90,
        source_count=1,
        spread_pct=round(spread_est, 4),
        dollar_volume=vol * c,
        vwap=vwap_val,
        halt_active=False,
        nasdaq_contradiction=False,
        yahoo_contradiction=False,
        smc_structures=smc_structures,
    )


def replay_csv(csv_path: str, symbol: str) -> list[dict]:
    candles = load_csv(csv_path)
    if not candles:
        return []

    results_log = []
    prev_vol = 0
    future_prices = []

    for idx, candle in enumerate(candles):
        snap = candle_to_snapshot(candle, symbol, idx, prev_vol)
        prev_vol = float(candle.get("volume", prev_vol))

        candidate = detect(snap)

        future_prices = [
            float(c.get("close", 0))
            for c in candles[idx+1:idx+16]
        ]

        entry_price = snap.price if snap.price > 0 else None
        if candidate.grade in ("A+", "A", "B") and entry_price:
            c_close = float(candle.get("close", 0))
            sl_price = float(candle.get("low", c_close * 0.98))
            r_mult = 0.0
            mfe = calculate_mfe(entry_price, future_prices, "long") if future_prices else 0
            mae = calculate_mae(entry_price, future_prices, "long") if future_prices else 0
            exit_price = future_prices[-1] if future_prices else entry_price
            r_mult = calculate_r_multiple(entry_price, sl_price, exit_price, "long")

            log_candidate(candidate)
            log_result(candidate.candidate_id or "N/A", {
                "entry": entry_price,
                "exit": exit_price,
                "mfe": mfe,
                "mae": mae,
                "r_multiple": r_mult,
                "hit_tp1": any(p >= entry_price * 1.01 for p in future_prices) if future_prices else False,
                "hit_tp2": any(p >= entry_price * 1.02 for p in future_prices) if future_prices else False,
                "hit_sl": any(p <= sl_price for p in future_prices) if future_prices else False,
            })

            results_log.append({
                "symbol": symbol,
                "ts": snap.timestamp,
                "setup_type": candidate.setup_type,
                "grade": candidate.grade,
                "entry": entry_price,
                "exit": exit_price,
                "r_multiple": r_mult,
                "mfe": mfe,
                "mae": mae,
            })

        elif candidate.grade == "reject":
            log_reject(candidate)

    return results_log


def run_proxy_backtest(symbol: str, csv_path: Optional[str] = None) -> dict:
    if csv_path is None:
        csv_path = f"data/ipo/proxy/{symbol}_ipo.csv"

    logger.info("running proxy backtest for %s (%s)", symbol, csv_path)
    results = replay_csv(csv_path, symbol)

    summary = get_summary()
    stats = compute_stats(results) if results else {}

    return {
        "symbol": symbol,
        "candles_replayed": len(results),
        "results": results,
        "summary": summary,
        "stats": stats,
    }


def run_all_proxy(symbols: Optional[list[str]] = None) -> dict:
    if symbols is None:
        symbols = PROXY_SYMBOLS

    all_results = {}
    for sym in symbols:
        try:
            all_results[sym] = run_proxy_backtest(sym)
        except Exception as e:
            logger.warning("proxy backtest failed for %s: %s", sym, e)
            all_results[sym] = {"symbol": sym, "error": str(e)}

    return all_results


def write_proxy_report(results: dict, path: Optional[str] = None) -> Path:
    if path:
        out = Path(path)
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        out = PROJECT_ROOT / "reports" / "ipo" / "spacex" / f"proxy_backtest_{date_str}.md"

    out.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# SPCX V2 — Proxy IPO Backtest Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Symbol Results",
        "",
        "| Symbol | Candles | Setups | Winrate | Expectancy R | Profit Factor |",
        "|--------|---------|--------|---------|--------------|---------------|",
    ]

    for sym, data in sorted(results.items()):
        stats = data.get("stats", {})
        summary = data.get("summary", {})
        candles = data.get("candles_replayed", 0)
        setups = summary.get("total_candidates", 0)
        wr = stats.get("winrate", 0)
        exp_r = stats.get("expectancy_R", 0)
        pf = stats.get("profit_factor", "N/A")

        lines.append(
            f"| {sym} | {candles} | {setups} | {wr}% | {exp_r}R | {pf} |"
        )

    lines += [
        "",
        "## Per Setup Type",
        "",
        "| Setup | Trades | Winrate | Expectancy R |",
        "|-------|--------|---------|--------------|",
    ]

    all_trades = []
    for sym, data in results.items():
        for r in data.get("results", []):
            all_trades.append(r)

    by_setup = {}
    for t in all_trades:
        st = t.get("setup_type", "UNKNOWN")
        by_setup.setdefault(st, []).append(t)

    for st in sorted(by_setup):
        trades = by_setup[st]
        r_vals = [t.get("r_multiple", 0) for t in trades if t.get("r_multiple") is not None]
        win_count = sum(1 for rv in r_vals if rv > 0)
        wr = round(win_count / len(r_vals) * 100, 1) if r_vals else 0
        exp_r = round(sum(r_vals) / len(r_vals), 3) if r_vals else 0
        lines.append(f"| {st} | {len(trades)} | {wr}% | {exp_r}R |")

    lines += [
        "",
        "---",
        "",
        "<i>Paper-only. Backtest on proxy IPO historical data.</i>",
    ]

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info("proxy report written to %s", out)
    return out
