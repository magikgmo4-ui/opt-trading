from __future__ import annotations
from dataclasses import dataclass, field
from statistics import mean, stdev
from typing import Any

from .setups import Setup, get_setup, SETUPS
from .io import utc_now


@dataclass
class TradeResult:
    setup_id: str
    side: str
    entry: float
    stop: float
    tp1: float
    tp2: float
    result: str            # win, loss, partial, open
    exit_price: float
    bars_held: int
    r_multiple: float
    exit_reason: str       # tp1, tp2, stop, eod


@dataclass
class BacktestRun:
    setup_id: str
    run_at: str
    total_trades: int
    wins: int
    losses: int
    partials: int
    win_rate: float
    avg_r: float
    profit_factor: float
    expectancy_r: float
    max_dd_r: float
    best_r: float
    worst_r: float
    consecutive_losses: int
    sharpe_estimate: float | None
    trades: list[TradeResult] = field(default_factory=list)


def run_backtest(
    bars: list[dict[str, Any]],
    setup: Setup,
    *,
    rr: float | None = None,
    partial_scale: float = 0.5,
) -> BacktestRun:
    rr = rr or setup.rr_target
    trades: list[TradeResult] = []

    if setup.setup_id == "IPO_ORB_5M":
        trades = _backtest_orb(bars, minutes=5, rr=rr, partial_scale=partial_scale, setup_id=setup.setup_id)
    elif setup.setup_id == "IPO_ORB_15M":
        trades = _backtest_orb(bars, minutes=15, rr=rr, partial_scale=partial_scale, setup_id=setup.setup_id)
    elif setup.setup_id == "GAP_AND_GO":
        trades = _backtest_gap_and_go(bars, rr=rr, partial_scale=partial_scale)
    elif setup.setup_id == "VWAP_RECLAIM":
        trades = _backtest_vwap_reclaim(bars, rr=rr, partial_scale=partial_scale)
    elif setup.setup_id == "FVG_RECLAIM":
        trades = _backtest_fvg_reclaim(bars, rr=rr, partial_scale=partial_scale)
    elif setup.setup_id == "FIRST_RED_DAY_TRAP":
        trades = _backtest_first_red_day(bars, rr=rr, partial_scale=partial_scale)
    elif setup.setup_id == "HIGH_VOLUME_CONTINUATION":
        trades = _backtest_high_vol_cont(bars, rr=rr, partial_scale=partial_scale)
    elif setup.setup_id == "TREND_DAY":
        trades = _backtest_trend_day(bars, rr=rr, partial_scale=partial_scale)
    elif setup.setup_id == "INSIDE_DAY_BREAKOUT":
        trades = _backtest_inside_day(bars, rr=rr, partial_scale=partial_scale)
    elif setup.setup_id == "WEEKLY_MOMENTUM":
        trades = _backtest_weekly_momentum(bars, rr=rr, partial_scale=partial_scale)
    elif setup.setup_id == "NEWS_CATALYST_BREAKOUT":
        trades = _backtest_news_catalyst(bars, rr=rr, partial_scale=partial_scale)
    else:
        trades = _backtest_generic_breakout(bars, rr=rr, partial_scale=partial_scale, setup_id=setup.setup_id)

    return _summarize_run(trades, setup.setup_id)


def run_all_setups(bars: list[dict[str, Any]], *, category: str | None = None, min_bars: int = 0) -> list[BacktestRun]:
    from .setups import list_setups
    setups = list_setups(category=category)
    results = []
    for s in setups:
        if len(bars) >= max(s.min_bars, min_bars):
            results.append(run_backtest(bars, s))
    return results


def run_scan(bars: list[dict[str, Any]], snapshot: dict[str, Any]) -> dict[str, Any]:
    results = run_all_setups(bars, min_bars=10)
    active = []
    for r in results:
        if r.total_trades > 0 and r.expectancy_r > 0:
            active.append({
                "setup_id": r.setup_id,
                "expectancy_r": r.expectancy_r,
                "win_rate": r.win_rate,
                "profit_factor": r.profit_factor,
            })

    scores = snapshot.get("scores", {})
    signals = snapshot.get("signals", [])

    return {
        "scanned_at": utc_now(),
        "total_setups_tested": len(results),
        "active_setups": len(active),
        "best_setups": sorted(active, key=lambda x: x["expectancy_r"], reverse=True)[:5],
        "current_scores": scores,
        "current_signals": signals,
        "bar_count": len(bars),
    }


def _summarize_run(trades: list[TradeResult], setup_id: str) -> BacktestRun:
    wins = [t for t in trades if t.result == "win"]
    losses = [t for t in trades if t.result == "loss"]
    partials = [t for t in trades if t.result == "partial"]
    r_vals = [t.r_multiple for t in trades]

    equity_curve = [0.0]
    for t in trades:
        equity_curve.append(equity_curve[-1] + t.r_multiple)

    dd = 0.0
    peak = 0.0
    for e in equity_curve:
        peak = max(peak, e)
        dd = max(dd, peak - e)

    profit_factor = _safe_div(
        sum(t.r_multiple for t in wins + partials if t.r_multiple > 0),
        abs(sum(t.r_multiple for t in losses))
    )

    cons_losses = 0
    max_cons = 0
    for t in trades:
        if t.result == "loss":
            cons_losses += 1
            max_cons = max(max_cons, cons_losses)
        else:
            cons_losses = 0

    sharpe = None
    if len(r_vals) > 1 and stdev(r_vals) > 0:
        sharpe = round(mean(r_vals) / stdev(r_vals) * (252 ** 0.5), 3) if len(r_vals) > 5 else None

    return BacktestRun(
        setup_id=setup_id,
        run_at=utc_now(),
        total_trades=len(trades),
        wins=len(wins),
        losses=len(losses),
        partials=len(partials),
        win_rate=round(len(wins + partials) / len(trades), 3) if trades else 0,
        avg_r=round(mean(r_vals), 3) if r_vals else 0,
        profit_factor=round(profit_factor, 2),
        expectancy_r=round(mean(r_vals), 3) if r_vals else 0,
        max_dd_r=round(dd, 3),
        best_r=round(max(r_vals), 3) if r_vals else 0,
        worst_r=round(min(r_vals), 3) if r_vals else 0,
        consecutive_losses=max_cons,
        sharpe_estimate=sharpe,
        trades=trades,
    )


def _backtest_orb(bars, minutes, rr, partial_scale, setup_id):
    if len(bars) <= minutes + 2:
        return []
    opening = bars[:minutes]
    hi = max(r.get("high", 0) for r in opening if r.get("high") is not None)
    lo = min(r.get("low", float("inf")) for r in opening if r.get("low") is not None)
    trades = []
    for i, r in enumerate(bars[minutes:], start=minutes):
        c = r.get("close")
        if c is None:
            continue
        if c > hi:
            entry = c; stop = lo
            tp1 = entry + (entry - stop) * rr * partial_scale
            tp2 = entry + (entry - stop) * rr
            out = _forward_sim(bars[i + 1:], entry, stop, tp1, tp2, "long", setup_id)
            trades.append(out)
            break
    return trades


def _backtest_gap_and_go(bars, rr, partial_scale):
    if len(bars) < 10:
        return []
    first_open = _num(bars[0].get("open"))
    prev_close = _num(bars[0].get("close"))
    if not first_open or not prev_close or first_open <= prev_close * 1.02:
        return []
    lo = min(r.get("low", float("inf")) for r in bars[:5] if r.get("low") is not None)
    entry_candle = None
    for i, r in enumerate(bars[5:], start=5):
        c = r.get("close")
        if c and c > first_open:
            entry_candle = (i, c)
            break
    if not entry_candle:
        return []
    i, entry = entry_candle
    stop = max(prev_close, lo)
    tp1 = entry + (entry - stop) * rr * partial_scale
    tp2 = entry + (entry - stop) * rr
    return [_forward_sim(bars[i + 1:], entry, stop, tp1, tp2, "long", "GAP_AND_GO")]


def _backtest_vwap_reclaim(bars, rr, partial_scale):
    if len(bars) < 20:
        return []
    prices = [_num(r.get("close")) for r in bars if _num(r.get("close")) is not None]
    vols = [_num(r.get("volume")) for r in bars if _num(r.get("volume")) is not None]
    if not prices or not vols:
        return []
    vwap = sum(p * v for p, v in zip(prices[:16], vols[:16]) if v) / max(1, sum(v for v in vols[:16] if v))
    below = sum(1 for p in prices[-8:-3] if p < vwap) if len(prices) >= 8 else 0
    if below < 3:
        return []
    entry = None; stop = None; entry_i = 0
    for i in range(max(0, len(bars) - 5), len(bars)):
        c = _num(bars[i].get("close"))
        l = _num(bars[i].get("low"))
        if c and c > vwap:
            entry = c; stop = min(prices[-5:]) if len(prices) >= 5 else c * 0.98; entry_i = i
            break
    if not entry or not stop:
        return []
    tp1 = entry + (entry - stop) * rr * partial_scale
    tp2 = entry + (entry - stop) * rr
    return [_forward_sim(bars[entry_i + 1:], entry, stop, tp1, tp2, "long", "VWAP_RECLAIM")]


def _backtest_fvg_reclaim(bars, rr, partial_scale):
    if len(bars) < 3:
        return []
    a, _, c = bars[-3], bars[-2], bars[-1]
    a_h, a_l = _num(a.get("high")), _num(a.get("low"))
    c_h, c_l = _num(c.get("high")), _num(c.get("low"))
    if not (a_h and c_l and c_l > a_h):
        return []
    fvg_top, fvg_bot = c_l, a_h
    entry = _num(c.get("close"))
    stop = fvg_bot - (fvg_top - fvg_bot) * 0.5
    if not entry or not stop:
        return []
    tp1 = entry + (entry - stop) * rr * partial_scale
    tp2 = entry + (entry - stop) * rr
    return [_forward_sim([], entry, stop, tp1, tp2, "long", "FVG_RECLAIM")]


def _backtest_first_red_day(bars, rr, partial_scale):
    if len(bars) < 2:
        return []
    day1 = bars[0]; day2 = bars[-1]
    d1_o, d1_c = _num(day1.get("open")), _num(day1.get("close"))
    d1_h, d1_l = _num(day1.get("high")), _num(day1.get("low"))
    d2_o = _num(day2.get("open"))
    if not (d1_o and d1_c and d2_o and d1_c < d1_o * 0.97 and d2_o > d1_c):
        return []
    entry = d2_o; stop = d1_l or d1_c * 0.95
    tp1 = entry + (entry - stop) * rr * partial_scale
    tp2 = entry + (entry - stop) * rr
    return [_forward_sim([], entry, stop, tp1, tp2, "long", "FIRST_RED_DAY_TRAP")]


def _backtest_high_vol_cont(bars, rr, partial_scale):
    if len(bars) < 20:
        return []
    vols = [_num(r.get("volume")) for r in bars if _num(r.get("volume")) is not None]
    if len(vols) < 20:
        return []
    avg_vol = mean(vols[-20:-1])
    last_vol = vols[-1]
    if not last_vol or last_vol <= avg_vol * 3:
        return []
    entry = _num(bars[-1].get("close"))
    lows = [_num(r.get("low")) for r in bars[-10:] if _num(r.get("low")) is not None]
    stop = min(lows) if lows else entry * 0.97
    if not entry or not stop:
        return []
    tp1 = entry + (entry - stop) * rr * partial_scale
    tp2 = entry + (entry - stop) * rr
    return [_forward_sim([], entry, stop, tp1, tp2, "long", "HIGH_VOLUME_CONTINUATION")]


def _backtest_trend_day(bars, rr, partial_scale):
    if len(bars) < 40:
        return []
    entry = _num(bars[-1].get("close"))
    lows = [_num(r.get("low")) for r in bars[-10:] if _num(r.get("low")) is not None]
    stop = min(lows) if lows else entry * 0.98
    if not entry or not stop:
        return []
    tp1 = entry + (entry - stop) * rr * partial_scale
    tp2 = entry + (entry - stop) * rr
    return [_forward_sim([], entry, stop, tp1, tp2, "long", "TREND_DAY")]


def _backtest_inside_day(bars, rr, partial_scale):
    if len(bars) < 3:
        return []
    day1, day2, day3 = bars[-3], bars[-2], bars[-1]
    d1_h, d1_l = _num(day1.get("high")), _num(day1.get("low"))
    d2_h, d2_l = _num(day2.get("high")), _num(day2.get("low"))
    d3_o = _num(day3.get("open"))
    if not (d1_h and d1_l and d2_h and d2_l and d1_h >= d2_h and d1_l <= d2_l):
        return []
    entry = d3_o
    if entry > d1_h:
        stop = d1_l; side = "long"
    elif entry < d1_l:
        stop = d1_h; side = "short"
    else:
        return []
    tp1 = entry + (entry - stop) * rr * partial_scale if side == "long" else entry - (stop - entry) * rr * partial_scale
    tp2 = entry + (entry - stop) * rr if side == "long" else entry - (stop - entry) * rr
    return [_forward_sim([], entry, stop, tp1, tp2, side, "INSIDE_DAY_BREAKOUT")]


def _backtest_weekly_momentum(bars, rr, partial_scale):
    if len(bars) < 4:
        return []
    entry = _num(bars[-1].get("open"))
    prev_low = _num(bars[-2].get("low"))
    if not entry or not prev_low or entry <= prev_low:
        return []
    stop = prev_low
    tp1 = entry + (entry - stop) * rr * partial_scale
    tp2 = entry + (entry - stop) * rr
    return [_forward_sim([], entry, stop, tp1, tp2, "long", "WEEKLY_MOMENTUM")]


def _backtest_news_catalyst(bars, rr, partial_scale):
    return _backtest_generic_breakout(bars, rr=rr, partial_scale=partial_scale, setup_id="NEWS_CATALYST_BREAKOUT")


def _backtest_generic_breakout(bars, rr, partial_scale, setup_id):
    if len(bars) < 10:
        return []
    hi = max(r.get("high", 0) for r in bars[-10:-1] if r.get("high") is not None)
    lo = min(r.get("low", float("inf")) for r in bars[-10:-1] if r.get("low") is not None)
    entry = _num(bars[-1].get("close"))
    if not entry or entry <= hi:
        return []
    stop = lo
    tp1 = entry + (entry - stop) * rr * partial_scale
    tp2 = entry + (entry - stop) * rr
    return [_forward_sim([], entry, stop, tp1, tp2, "long", setup_id)]


def _forward_sim(remaining, entry, stop, tp1, tp2, side, setup_id):
    risk = abs(entry - stop) or 0.001
    exited = False
    for j, r in enumerate(remaining):
        h, l = r.get("high"), r.get("low")
        if h is None or l is None:
            continue
        if side == "long":
            if l <= stop:
                return TradeResult(setup_id, side, entry, stop, tp1, tp2, "loss", stop, j + 1, -1, "stop")
            if h >= tp2:
                return TradeResult(setup_id, side, entry, stop, tp1, tp2, "win", tp2, j + 1, round((tp2 - entry) / risk, 3), "tp2")
            if h >= tp1:
                return TradeResult(setup_id, side, entry, stop, tp1, tp2, "partial", tp1, j + 1, round((tp1 - entry) / risk, 3), "tp1")
        else:
            if h >= stop:
                return TradeResult(setup_id, side, entry, stop, tp1, tp2, "loss", stop, j + 1, -1, "stop")
            if l <= tp2:
                return TradeResult(setup_id, side, entry, stop, tp1, tp2, "win", tp2, j + 1, round((entry - tp2) / risk, 3), "tp2")
            if l <= tp1:
                return TradeResult(setup_id, side, entry, stop, tp1, tp2, "partial", tp1, j + 1, round((entry - tp1) / risk, 3), "tp1")
    if not exited:
        last_close = remaining[-1].get("close") if remaining else entry
        final_r = round((last_close - entry) / risk, 3) if side == "long" else round((entry - last_close) / risk, 3)
        return TradeResult(setup_id, side, entry, stop, tp1, tp2, "open", last_close, len(remaining), final_r, "eod")
    return TradeResult(setup_id, side, entry, stop, tp1, tp2, "loss", stop, len(remaining), -1, "eod")


def _num(v):
    try:
        return float(v) if v not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _safe_div(a, b):
    return a / b if b else 0.0
