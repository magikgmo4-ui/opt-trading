from __future__ import annotations
import csv
from pathlib import Path
from statistics import mean
from .io import utc_now

SETUPS = ["IPO_ORB_5M", "IPO_ORB_15M", "GAP_AND_GO", "VWAP_RECLAIM", "FVG_RECLAIM", "IPO_PRICE_FLUSH_RECLAIM", "FIRST_RED_DAY_TRAP", "NEWS_CATALYST_BREAKOUT"]

def load_ohlcv_csv(path: str | Path) -> list[dict]:
    rows = []
    with Path(path).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append({k.lower(): _num(v) if k.lower() in {"open", "high", "low", "close", "volume"} else v for k, v in r.items()})
    return rows

def backtest_orb(rows: list[dict], minutes: int = 15, rr: float = 2.0) -> dict:
    if len(rows) <= minutes + 2:
        return {"ok": False, "error": "not enough rows"}
    opening = rows[:minutes]
    hi = max(r["high"] for r in opening if r.get("high") is not None)
    lo = min(r["low"] for r in opening if r.get("low") is not None)
    trades = []
    for i, r in enumerate(rows[minutes:], start=minutes):
        c = r.get("close")
        if c is None:
            continue
        if c > hi:
            entry = c; stop = lo; target = entry + (entry - stop) * rr
            outcome = _forward_outcome(rows[i + 1 :], entry, stop, target, "long")
            trades.append({"setup": f"IPO_ORB_{minutes}M", "side": "long", "entry": entry, "stop": stop, "target": target, **outcome})
            break
        if c < lo:
            entry = c; stop = hi; target = entry - (stop - entry) * rr
            outcome = _forward_outcome(rows[i + 1 :], entry, stop, target, "short")
            trades.append({"setup": f"IPO_ORB_{minutes}M", "side": "short", "entry": entry, "stop": stop, "target": target, **outcome})
            break
    return summarize(trades)

def summarize(trades: list[dict]) -> dict:
    wins = [t for t in trades if t.get("result") == "win"]
    losses = [t for t in trades if t.get("result") == "loss"]
    rvals = [t.get("r", 0) for t in trades]
    return {"ok": True, "generated_at": utc_now(), "trades": trades, "count": len(trades), "wins": len(wins), "losses": len(losses), "winrate": round(len(wins) / len(trades), 3) if trades else None, "expectancy_r": round(mean(rvals), 3) if rvals else None}

def _forward_outcome(rows, entry, stop, target, side):
    risk = abs(entry - stop) or 1
    for j, r in enumerate(rows):
        h, l = r.get("high"), r.get("low")
        if h is None or l is None:
            continue
        if side == "long":
            if l <= stop:
                return {"result": "loss", "bars_held": j + 1, "r": -1}
            if h >= target:
                return {"result": "win", "bars_held": j + 1, "r": round(abs(target - entry) / risk, 3)}
        else:
            if h >= stop:
                return {"result": "loss", "bars_held": j + 1, "r": -1}
            if l <= target:
                return {"result": "win", "bars_held": j + 1, "r": round(abs(entry - target) / risk, 3)}
    last = rows[-1].get("close") if rows else entry
    r = (last - entry) / risk if side == "long" else (entry - last) / risk
    return {"result": "open_or_eod", "bars_held": len(rows), "r": round(r, 3)}

def _num(v):
    try:
        return float(v) if v not in (None, "") else None
    except Exception:
        return None
