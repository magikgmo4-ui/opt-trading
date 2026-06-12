from __future__ import annotations
from statistics import mean, stdev
from typing import Any


def ema(series: list[float], period: int) -> list[float | None]:
    if len(series) < period:
        return [None] * len(series)
    k = 2.0 / (period + 1)
    result: list[float | None] = [None] * (period - 1)
    result.append(mean(series[:period]))
    for i in range(period, len(series)):
        val = series[i] * k + (result[-1] or 0) * (1 - k)
        result.append(val)
    return result


def sma(series: list[float], period: int) -> list[float | None]:
    result: list[float | None] = [None] * (period - 1)
    for i in range(period - 1, len(series)):
        result.append(mean(series[i - period + 1:i + 1]))
    return result


def rsi(closes: list[float], period: int = 14) -> list[float | None]:
    if len(closes) < period + 1:
        return [None] * len(closes)
    result: list[float | None] = [None] * period
    gains, losses = [], []
    for i in range(1, period + 1):
        delta = closes[i] - closes[i - 1]
        gains.append(max(delta, 0))
        losses.append(max(-delta, 0))
    avg_gain = mean(gains)
    avg_loss = mean(losses)
    result.append(_rsi_val(avg_gain, avg_loss))
    for i in range(period + 1, len(closes)):
        delta = closes[i] - closes[i - 1]
        gain = max(delta, 0)
        loss = max(-delta, 0)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        result.append(_rsi_val(avg_gain, avg_loss))
    return result


def _rsi_val(avg_gain: float, avg_loss: float) -> float | None:
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def macd(closes: list[float], fast: int = 12, slow: int = 26, signal_period: int = 9) -> dict[str, list[float | None]]:
    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    macd_line: list[float | None] = []
    for i in range(len(closes)):
        if ema_fast[i] is not None and ema_slow[i] is not None:
            macd_line.append(ema_fast[i] - ema_slow[i])
        else:
            macd_line.append(None)

    valid = [v for v in macd_line if v is not None]
    signal = ema(valid, signal_period)
    pad = len(macd_line) - len(signal)
    signal_padded: list[float | None] = [None] * pad + signal

    histogram: list[float | None] = []
    for i in range(len(closes)):
        if macd_line[i] is not None and signal_padded[i] is not None:
            histogram.append(macd_line[i] - signal_padded[i])
        else:
            histogram.append(None)

    return {"macd_line": macd_line, "signal": signal_padded, "histogram": histogram}


def atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> list[float | None]:
    if len(highs) < 2:
        return [None] * len(highs)
    tr: list[float] = [highs[0] - lows[0]]
    for i in range(1, len(highs)):
        tr.append(max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        ))
    result: list[float | None] = [None] * (period - 1)
    result.append(mean(tr[:period]))
    for i in range(period, len(tr)):
        result.append(((result[-1] or 0) * (period - 1) + tr[i]) / period)
    return result


def vwap(highs: list[float], lows: list[float], closes: list[float], volumes: list[float]) -> list[float | None]:
    if not volumes or not closes:
        return [None]
    result: list[float | None] = []
    cum_pv = 0.0
    cum_v = 0.0
    for i in range(len(closes)):
        typical = (highs[i] + lows[i] + closes[i]) / 3.0
        v = volumes[i] if volumes[i] is not None else 0
        cum_pv += typical * v
        cum_v += v
        result.append(cum_pv / cum_v if cum_v > 0 else None)
    return result


def bollinger_bands(series: list[float], period: int = 20, multiplier: float = 2.0) -> dict[str, list[float | None]]:
    sma_vals = sma(series, period)
    upper: list[float | None] = []
    lower: list[float | None] = []
    for i in range(len(series)):
        if sma_vals[i] is None or i < period - 1:
            upper.append(None)
            lower.append(None)
        else:
            window = series[i - period + 1:i + 1]
            if len(window) >= 2:
                sd = stdev(window)
                upper.append(sma_vals[i] + multiplier * sd)
                lower.append(sma_vals[i] - multiplier * sd)
            else:
                upper.append(None)
                lower.append(None)
    return {"middle": sma_vals, "upper": upper, "lower": lower}


def relative_volume(volumes: list[float], lookback: int = 20) -> list[float | None]:
    result: list[float | None] = [None] * (lookback - 1)
    for i in range(lookback - 1, len(volumes)):
        window = [v for v in volumes[max(0, i - lookback + 1):i + 1] if v is not None]
        if len(window) < 2:
            result.append(None)
            continue
        avg = mean(window[:-1])
        result.append(volumes[i] / avg if avg > 0 else None)
    return result


def volume_zscore(volumes: list[float], lookback: int = 50) -> list[float | None]:
    result: list[float | None] = [None] * (lookback - 1)
    for i in range(lookback - 1, len(volumes)):
        window = [v for v in volumes[max(0, i - lookback + 1):i + 1] if v is not None]
        if len(window) < 5:
            result.append(None)
            continue
        m = mean(window)
        sd = stdev(window)
        result.append((volumes[i] - m) / sd if sd > 0 else 0.0)
    return result


def opening_range(bars: list[dict[str, Any]], minutes: int) -> dict[str, Any]:
    if len(bars) < minutes:
        return {"high": None, "low": None, "range": None}
    opening = bars[:minutes]
    highs = [b.get("high") for b in opening if b.get("high") is not None]
    lows = [b.get("low") for b in opening if b.get("low") is not None]
    if not highs or not lows:
        return {"high": None, "low": None, "range": None}
    or_high = max(highs)
    or_low = min(lows)
    return {"high": or_high, "low": or_low, "range": or_high - or_low}


def compute_all_indicators(bars: list[dict[str, Any]], ipo_price: float = 135.0) -> dict[str, Any]:
    if not bars:
        return {}

    opens = [_safe(b.get("open")) for b in bars]
    highs = [_safe(b.get("high")) for b in bars]
    lows = [_safe(b.get("low")) for b in bars]
    closes = [_safe(b.get("close")) for b in bars]
    volumes = [_safe(b.get("volume")) for b in bars]

    last_close = next((c for c in reversed(closes) if c is not None), None)
    prev_close = closes[-2] if len(closes) > 1 and closes[-2] is not None else None

    ema9 = ema(closes, 9)
    ema20 = ema(closes, 20)
    ema50 = ema(closes, 50)
    ema200 = ema(closes, 200)
    sma20 = sma(closes, 20)
    sma50 = sma(closes, 50)
    sma200 = sma(closes, 200)
    rsi14 = rsi(closes, 14)
    macd_data = macd(closes)
    atr14 = atr(highs, lows, closes, 14)
    vwap_vals = vwap(highs, lows, closes, volumes)
    bb = bollinger_bands(closes, 20)
    rel_vol = relative_volume(volumes, 20)
    vol_z = volume_zscore(volumes, 50)

    or5 = opening_range(bars, 5)
    or15 = opening_range(bars, 15)
    or30 = opening_range(bars, 30) if len(bars) >= 30 else opening_range(bars, len(bars))

    prev_gap = ((last_close - prev_close) / prev_close * 100) if last_close and prev_close else None
    ipo_gap = ((last_close - ipo_price) / ipo_price * 100) if last_close else None
    vwap_dist = ((last_close - (vwap_vals[-1] or last_close)) / (vwap_vals[-1] or last_close) * 100) if last_close and vwap_vals[-1] else None

    return {
        "price": last_close,
        "open": opens[-1],
        "high": highs[-1] if highs[-1] is not None else None,
        "low": lows[-1] if lows[-1] is not None else None,
        "close": last_close,
        "volume": volumes[-1] if volumes[-1] is not None else None,
        "previous_close": prev_close,
        "prev_gap_pct": round(prev_gap, 2) if prev_gap is not None else None,
        "ipo_gap_pct": round(ipo_gap, 2) if ipo_gap is not None else None,
        "vwap_distance_pct": round(vwap_dist, 2) if vwap_dist is not None else None,
        "ema_9": _last(ema9),
        "ema_20": _last(ema20),
        "ema_50": _last(ema50),
        "ema_200": _last(ema200),
        "sma_20": _last(sma20),
        "sma_50": _last(sma50),
        "sma_200": _last(sma200),
        "rsi_14": _last(rsi14),
        "macd_line": _last(macd_data["macd_line"]),
        "macd_signal": _last(macd_data["signal"]),
        "macd_histogram": _last(macd_data["histogram"]),
        "atr_14": _last(atr14),
        "vwap": _last(vwap_vals),
        "bb_upper": _last(bb["upper"]),
        "bb_middle": _last(bb["middle"]),
        "bb_lower": _last(bb["lower"]),
        "relative_volume": _last(rel_vol),
        "volume_zscore": _last(vol_z),
        "opening_range_5m": or5,
        "opening_range_15m": or15,
        "opening_range_30m": or30,
        "bars_count": len(bars),
    }


def _safe(v: Any) -> float:
    try:
        return float(v) if v is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def _last(lst: list[float | None]) -> float | None:
    for v in reversed(lst):
        if v is not None:
            return round(v, 4)
    return None
