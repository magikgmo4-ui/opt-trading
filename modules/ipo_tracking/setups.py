from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Setup:
    setup_id: str
    name: str
    category: str              # momentum, mean_reversion, breakout, trend, catalyst
    direction: str             # long, short, both
    timeframe: str             # M5, M15, H1, D1
    min_bars: int              # minimum bars needed
    entry_rule: str
    stop_rule: str
    tp1_rule: str              # first target
    tp2_rule: str              # runner target
    rr_target: float           # default R:R
    filters: list[str] = field(default_factory=list)
    invalidation: str = ""
    notes: str = ""


SETUPS: dict[str, Setup] = {
    "IPO_ORB_5M": Setup(
        setup_id="IPO_ORB_5M",
        name="IPO Opening Range Breakout 5M",
        category="breakout",
        direction="long",
        timeframe="M5",
        min_bars=15,
        entry_rule="price > opening_range_high with volume > avg_volume",
        stop_rule="opening_range_low or 1.5*ATR below entry",
        tp1_rule="entry + 1.5R",
        tp2_rule="entry + 3R (runner)",
        rr_target=2.0,
        filters=["ipo_gap > 0", "rel_volume > 1.2", "no FVG bearish"],
        invalidation="price re-enters opening range",
        notes="Classic IPO setup. Highest probability first 30 min.",
    ),
    "IPO_ORB_15M": Setup(
        setup_id="IPO_ORB_15M",
        name="IPO Opening Range Breakout 15M",
        category="breakout",
        direction="long",
        timeframe="M15",
        min_bars=30,
        entry_rule="price > opening_range_15_high with volume > avg_volume * 1.3",
        stop_rule="opening_range_15_low or 2*ATR below entry",
        tp1_rule="entry + 1.5R",
        tp2_rule="entry + 3R (runner)",
        rr_target=2.0,
        filters=["ipo_gap > 2%", "rel_volume > 1.5", "no bearish FVG", "above VWAP"],
        invalidation="price drops below VWAP",
        notes="Wider range version. Lower noise but needs clear momentum.",
    ),
    "GAP_AND_GO": Setup(
        setup_id="GAP_AND_GO",
        name="Gap and Go",
        category="momentum",
        direction="long",
        timeframe="M5",
        min_bars=10,
        entry_rule="price opens > previous_close + 2% AND first pullback holds above VWAP AND resumes above pre-market high",
        stop_rule="VWAP or previous_close, whichever is higher",
        tp1_rule="entry + 1R",
        tp2_rule="entry + 2.5R (trail to VWAP)",
        rr_target=1.75,
        filters=["ipo_gap > 3%", "first_candle_bullish", "rel_volume > 2.0"],
        invalidation="price closes below VWAP on 5m candle",
        notes="Momentum continuation after gap. Crypto/IPO hybrid pattern.",
    ),
    "VWAP_RECLAIM": Setup(
        setup_id="VWAP_RECLAIM",
        name="VWAP Reclaim",
        category="mean_reversion",
        direction="long",
        timeframe="M5",
        min_bars=20,
        entry_rule="price reclaims VWAP from below after being below for >= 3 candles, with bullish engulfing confirmation",
        stop_rule="swing low before reclaim or 1*ATR below entry",
        tp1_rule="pre-reclaim high or entry + 1R",
        tp2_rule="entry + 2R (target prior resistance)",
        rr_target=1.5,
        filters=["price > IPO price", "no FVG bearish on H1", "rel_volume > 1.0"],
        invalidation="price loses VWAP again within 3 candles",
        notes="High probability institutional pattern. Works on any liquid equity.",
    ),
    "FVG_RECLAIM": Setup(
        setup_id="FVG_RECLAIM",
        name="Fair Value Gap Reclaim",
        category="mean_reversion",
        direction="long",
        timeframe="M15",
        min_bars=30,
        entry_rule="bullish FVG detected AND price retraces into FVG zone AND holds above lower boundary",
        stop_rule="below FVG lower boundary by 0.5*ATR",
        tp1_rule="FVG upper boundary (fill)",
        tp2_rule="prior swing high",
        rr_target=2.0,
        filters=["FVG size > 0.3%", "above VWAP", "not in congestion zone"],
        invalidation="price closes below FVG lower boundary",
        notes="Smart money concept. Wait for FVG fill then resume.",
    ),
    "FIRST_RED_DAY_TRAP": Setup(
        setup_id="FIRST_RED_DAY_TRAP",
        name="First Red Day Trap",
        category="mean_reversion",
        direction="long",
        timeframe="D1",
        min_bars=2,
        entry_rule="day 1: large red candle (>= -3%) with high volume. day 2: opens above day 1 close AND holds, buy first 30 min",
        stop_rule="day 1 low",
        tp1_rule="50% retracement of day 1 range",
        tp2_rule="full retracement of day 1 range",
        rr_target=2.0,
        filters=["ipo_gap < 50%", "volume on day 1 > 2x avg", "no negative news"],
        invalidation="price makes new low below day 1 low",
        notes="IPO-specific overnight setup. First red day often traps sellers.",
    ),
    "HIGH_VOLUME_CONTINUATION": Setup(
        setup_id="HIGH_VOLUME_CONTINUATION",
        name="High Volume Continuation",
        category="trend",
        direction="long",
        timeframe="M5",
        min_bars=20,
        entry_rule="volume > 3x avg_volume, candle closes green, price > EMA20, next candle pullback to EMA20 = entry",
        stop_rule="below EMA20 and below prior swing low, whichever is lower",
        tp1_rule="entry + 1R",
        tp2_rule="entry + 2R (let runner to VWAP extension)",
        rr_target=1.5,
        filters=["price > VWAP", "trend intact (EMA20 > EMA50)", "no bearish divergence"],
        invalidation="volume drops below avg on next candle",
        notes="High probability continuation. Follow the volume.",
    ),
    "NEWS_CATALYST_BREAKOUT": Setup(
        setup_id="NEWS_CATALYST_BREAKOUT",
        name="News Catalyst Breakout",
        category="catalyst",
        direction="long",
        timeframe="M5",
        min_bars=15,
        entry_rule="positive news detected + price breaks above prior swing high within 15 min of news + volume spike > 2x",
        stop_rule="prior swing low or EMA20, whichever is higher",
        tp1_rule="entry + 1.5R",
        tp2_rule="entry + 3R (let runner on momentum)",
        rr_target=2.0,
        filters=["news event validated", "price > VWAP", "no halt risk"],
        invalidation="price gives back 50% of news move",
        notes="Catalyst-driven. Requires real-time news validation.",
    ),
    "TREND_DAY": Setup(
        setup_id="TREND_DAY",
        name="Trend Day Continuation",
        category="trend",
        direction="long",
        timeframe="M15",
        min_bars=40,
        entry_rule="price consistently above EMA20 for last 10 candles, pullback to EMA20 holds, next green candle = entry",
        stop_rule="EMA50 or 1.5*ATR below entry, whichever is higher",
        tp1_rule="entry + 1R",
        tp2_rule="entry + 2.5R (trail to EMA20 on M15)",
        rr_target=1.75,
        filters=["price > VWAP", "higher highs AND higher lows", "rel_volume > 0.8"],
        invalidation="price closes below EMA50",
        notes="Trend day: don't fight the tape. Join on pullbacks.",
    ),
    "INSIDE_DAY_BREAKOUT": Setup(
        setup_id="INSIDE_DAY_BREAKOUT",
        name="Inside Day Breakout",
        category="breakout",
        direction="both",
        timeframe="D1",
        min_bars=3,
        entry_rule="day 2 range fully inside day 1 range. day 3: break above day 1 high = long, break below day 1 low = short",
        stop_rule="opposite side of day 1 range (long: day 1 low, short: day 1 high)",
        tp1_rule="day 1 high + (day 1 range)",
        tp2_rule="day 1 high + (2 * day 1 range)",
        rr_target=2.0,
        filters=["day 1 range > ATR", "no earnings in 2 days"],
        invalidation="price re-enters inside day range",
        notes="Coiled spring. Inside day precedes expansion 70% of the time.",
    ),
    "WEEKLY_MOMENTUM": Setup(
        setup_id="WEEKLY_MOMENTUM",
        name="Weekly Momentum Continuation",
        category="trend",
        direction="long",
        timeframe="W1",
        min_bars=4,
        entry_rule="last week closed green AND above EMA20 on weekly, new week opens above prior week high, buy at open",
        stop_rule="prior week low",
        tp1_rule="entry + 1R",
        tp2_rule="entry + 3R (runner for swing)",
        rr_target=2.0,
        filters=["price > EMA20 on W1", "MACD bullish", "no negative catalyst"],
        invalidation="weekly candle closes red below EMA20",
        notes="Swing setup. Low frequency, high conviction. Hold for weeks.",
    ),
}

CATEGORIES = {
    "breakout": ["IPO_ORB_5M", "IPO_ORB_15M", "INSIDE_DAY_BREAKOUT"],
    "momentum": ["GAP_AND_GO"],
    "trend": ["HIGH_VOLUME_CONTINUATION", "TREND_DAY", "WEEKLY_MOMENTUM"],
    "mean_reversion": ["VWAP_RECLAIM", "FVG_RECLAIM", "FIRST_RED_DAY_TRAP"],
    "catalyst": ["NEWS_CATALYST_BREAKOUT"],
}


def get_setup(setup_id: str) -> Setup | None:
    return SETUPS.get(setup_id)


def list_setups(category: str | None = None) -> list[Setup]:
    if category:
        ids = CATEGORIES.get(category, [])
        return [SETUPS[sid] for sid in ids if sid in SETUPS]
    return list(SETUPS.values())


def setup_summary(setup: Setup) -> dict[str, Any]:
    return {
        "id": setup.setup_id,
        "name": setup.name,
        "category": setup.category,
        "direction": setup.direction,
        "timeframe": setup.timeframe,
        "rr_target": setup.rr_target,
        "filters": setup.filters,
    }
