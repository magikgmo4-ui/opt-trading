"""SPCX V2 — Performance calculator: MFE, MAE, R-multiple, stats aggregation."""

from typing import Optional


# ── Core metrics ─────────────────────────────────────────────────────
def calculate_mfe(entry: float, price_series: list[float], direction: str = "long") -> float:
    if not price_series:
        return 0.0
    if direction == "long":
        best = max(price_series)
    else:
        best = min(price_series)
    mfe = (best - entry) / entry if direction == "long" else (entry - best) / entry
    return round(mfe, 6)


def calculate_mae(entry: float, price_series: list[float], direction: str = "long") -> float:
    if not price_series:
        return 0.0
    if direction == "long":
        worst = min(price_series)
    else:
        worst = max(price_series)
    mae = (entry - worst) / entry if direction == "long" else (worst - entry) / entry
    return round(mae, 6)


def calculate_r_multiple(entry: float, sl: float, exit_price: float, direction: str = "long") -> float:
    if entry == sl:
        return 0.0
    risk = abs(entry - sl)
    if risk == 0:
        return 0.0
    if direction == "long":
        result = (exit_price - entry) / risk
    else:
        result = (entry - exit_price) / risk
    return round(result, 4)


# ── Trigger checks ───────────────────────────────────────────────────
def check_tp1_hit(price_series: list[float], tp1: float, direction: str = "long") -> bool:
    if tp1 is None or not price_series:
        return False
    if direction == "long":
        return any(p >= tp1 for p in price_series)
    else:
        return any(p <= tp1 for p in price_series)


def check_tp2_hit(price_series: list[float], tp2: float, direction: str = "long") -> bool:
    if tp2 is None or not price_series:
        return False
    if direction == "long":
        return any(p >= tp2 for p in price_series)
    else:
        return any(p <= tp2 for p in price_series)


def check_sl_hit(price_series: list[float], sl: float, direction: str = "long") -> bool:
    if sl is None or not price_series:
        return False
    if direction == "long":
        return any(p <= sl for p in price_series)
    else:
        return any(p >= sl for p in price_series)


# ── Stats aggregation ────────────────────────────────────────────────
def compute_stats(candidates_with_results: list[dict]) -> dict:
    if not candidates_with_results:
        return _empty_stats()

    r_values = []
    win_count = 0
    loss_count = 0
    mfe_values = []
    mae_values = []
    tp1_hits = 0
    tp2_hits = 0
    sl_hits = 0

    for c in candidates_with_results:
        r = c.get("r_multiple")
        if r is not None:
            r_values.append(r)
            if r > 0:
                win_count += 1
            elif r < 0:
                loss_count += 1

        mfe = c.get("mfe")
        if mfe is not None:
            mfe_values.append(mfe)

        mae = c.get("mae")
        if mae is not None:
            mae_values.append(mae)

        if c.get("hit_tp1"):
            tp1_hits += 1
        if c.get("hit_tp2"):
            tp2_hits += 1
        if c.get("hit_sl"):
            sl_hits += 1

    total = len(r_values)
    winrate = (win_count / total * 100) if total > 0 else 0
    expectancy = sum(r_values) / total if total > 0 else 0

    gross_profit = sum(r for r in r_values if r > 0)
    gross_loss = abs(sum(r for r in r_values if r < 0))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (float("inf") if gross_profit > 0 else 0)

    cumulative = 0.0
    peak = 0.0
    max_drawdown = 0.0
    for r in r_values:
        cumulative += r
        if cumulative > peak:
            peak = cumulative
        dd = peak - cumulative
        if dd > max_drawdown:
            max_drawdown = dd

    return {
        "total_trades": total,
        "win_count": win_count,
        "loss_count": loss_count,
        "winrate": round(winrate, 2),
        "expectancy_R": round(expectancy, 3),
        "profit_factor": round(profit_factor, 2) if profit_factor != float("inf") else None,
        "max_drawdown_R": round(max_drawdown, 3),
        "avg_MFE": round(sum(mfe_values) / len(mfe_values), 5) if mfe_values else 0,
        "avg_MAE": round(sum(mae_values) / len(mae_values), 5) if mae_values else 0,
        "tp1_hit_rate": round(tp1_hits / total * 100, 2) if total > 0 else 0,
        "tp2_hit_rate": round(tp2_hits / total * 100, 2) if total > 0 else 0,
        "sl_hit_rate": round(sl_hits / total * 100, 2) if total > 0 else 0,
    }


def compute_stats_by_setup(candidates_with_results: list[dict]) -> dict:
    by_setup = {}
    for c in candidates_with_results:
        st = c.get("setup_type", "UNKNOWN")
        by_setup.setdefault(st, []).append(c)

    result = {}
    for st, items in by_setup.items():
        result[st] = compute_stats(items)
    return result


def compute_stats_by_grade(candidates_with_results: list[dict]) -> dict:
    by_grade = {}
    for c in candidates_with_results:
        g = c.get("grade", "reject")
        by_grade.setdefault(g, []).append(c)

    result = {}
    for g, items in by_grade.items():
        result[g] = compute_stats(items)
    return result


# ── Helpers ──────────────────────────────────────────────────────────
def _empty_stats() -> dict:
    return {
        "total_trades": 0,
        "win_count": 0,
        "loss_count": 0,
        "winrate": 0,
        "expectancy_R": 0,
        "profit_factor": None,
        "max_drawdown_R": 0,
        "avg_MFE": 0,
        "avg_MAE": 0,
        "tp1_hit_rate": 0,
        "tp2_hit_rate": 0,
        "sl_hit_rate": 0,
    }
