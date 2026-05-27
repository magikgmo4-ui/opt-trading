"""
Tests for modules/trading_lab_v1/app/exit_outcome_v1.py

Run: pytest modules/trading_lab_v1/tests/test_exit_outcome_v1.py -q
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.trading_lab_v1.app.exit_outcome_v1 import (
    calc_tp,
    resolve_exit_outcome,
    get_post_entry_candles,
)

TZ = ZoneInfo("America/Montreal")


def _candle(ts_str: str, o: float, h: float, l: float, c: float) -> dict:
    return {"ts": datetime.fromisoformat(ts_str).replace(tzinfo=TZ), "open": o, "high": h, "low": l, "close": c, "volume": 100.0}


# ── calc_tp ──────────────────────────────────────────────────────────────────

class TestCalcTp:
    def test_bullish(self):
        assert calc_tp(3258.0, 3248.0, 2.0, "bullish") == 3278.0

    def test_bearish(self):
        assert calc_tp(3252.0, 3262.0, 2.0, "bearish") == 3232.0

    def test_rr_1(self):
        assert calc_tp(3200.0, 3195.0, 1.0, "bullish") == 3205.0

    def test_sl_above_entry_bearish(self):
        # sl is above entry for bearish
        assert calc_tp(3250.0, 3258.0, 2.0, "bearish") == 3234.0


# ── resolve_exit_outcome — win ────────────────────────────────────────────────

class TestResolveExitOutcomeWin:
    def _candles_bullish_win(self):
        # entry=3258, sl=3248, rr=2 → tp=3278. Candle 3 hits tp.
        return [
            _candle("2026-04-07T18:06:00", 3259.0, 3262.0, 3258.5, 3261.0),
            _candle("2026-04-07T18:07:00", 3261.0, 3265.0, 3260.5, 3264.0),
            _candle("2026-04-07T18:08:00", 3264.0, 3279.0, 3263.5, 3278.5),  # high=3279 >= tp=3278
        ]

    def test_result_win(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", self._candles_bullish_win())
        assert outcome["result"] == "win"

    def test_r_realized_equals_rr(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", self._candles_bullish_win())
        assert outcome["r_realized"] == 2.0

    def test_exit_price_is_tp(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", self._candles_bullish_win())
        assert outcome["exit_price"] == 3278.0

    def test_bars_held(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", self._candles_bullish_win())
        assert outcome["bars_held"] == 3

    def test_outcome_reason_tp_hit(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", self._candles_bullish_win())
        assert outcome["outcome_reason"] == "tp_hit"

    def test_exit_ts_set(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", self._candles_bullish_win())
        assert outcome["exit_ts"] is not None
        assert "18:08" in outcome["exit_ts"]

    def test_bearish_win(self):
        # entry=3252, sl=3262, rr=2 → tp=3232. Candle hits low=3231.5.
        candles = [
            _candle("2026-04-08T18:06:00", 3250.0, 3251.0, 3244.0, 3245.0),
            _candle("2026-04-08T18:07:00", 3245.0, 3246.0, 3231.0, 3232.5),  # low=3231 <= tp=3232
        ]
        outcome = resolve_exit_outcome(3252.0, 3262.0, 2.0, "bearish", candles)
        assert outcome["result"] == "win"
        assert outcome["r_realized"] == 2.0


# ── resolve_exit_outcome — loss ───────────────────────────────────────────────

class TestResolveExitOutcomeLoss:
    def _candles_bullish_loss(self):
        # entry=3258, sl=3248, rr=2 → tp=3278. SL hit on candle 2.
        return [
            _candle("2026-04-07T18:06:00", 3257.0, 3259.0, 3254.0, 3255.0),
            _candle("2026-04-07T18:07:00", 3255.0, 3256.0, 3247.5, 3248.5),  # low=3247.5 <= sl=3248
        ]

    def test_result_loss(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", self._candles_bullish_loss())
        assert outcome["result"] == "loss"

    def test_r_realized_minus_one(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", self._candles_bullish_loss())
        assert outcome["r_realized"] == -1.0

    def test_exit_price_is_sl(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", self._candles_bullish_loss())
        assert outcome["exit_price"] == 3248.0

    def test_outcome_reason_sl_hit(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", self._candles_bullish_loss())
        assert outcome["outcome_reason"] == "sl_hit"

    def test_bearish_loss(self):
        # entry=3252, sl=3262, rr=2 → tp=3232. SL hit.
        candles = [
            _candle("2026-04-08T18:06:00", 3253.0, 3263.5, 3252.0, 3263.0),  # high=3263.5 >= sl=3262
        ]
        outcome = resolve_exit_outcome(3252.0, 3262.0, 2.0, "bearish", candles)
        assert outcome["result"] == "loss"
        assert outcome["r_realized"] == -1.0


# ── resolve_exit_outcome — ambiguous same-candle ──────────────────────────────

class TestResolveExitOutcomeAmbiguous:
    def test_same_candle_conservative_loss(self):
        # entry=3258, sl=3248, tp=3278. Single candle: low=3247 (SL) and high=3279 (TP) both.
        candles = [
            _candle("2026-04-07T18:06:00", 3258.0, 3279.0, 3247.0, 3260.0),
        ]
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", candles)
        assert outcome["result"] == "loss"
        assert outcome["outcome_reason"] == "sl_tp_same_candle_conservative_loss"
        assert outcome["r_realized"] == -1.0


# ── resolve_exit_outcome — timeout ────────────────────────────────────────────

class TestResolveExitOutcomeTimeout:
    def _neutral_candles(self, n: int, base: float = 3258.0) -> list[dict]:
        return [
            _candle(f"2026-04-07T18:{6+i:02d}:00", base, base + 0.5, base - 0.3, base + 0.2)
            for i in range(n)
        ]

    def test_no_candles_timeout(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", [])
        assert outcome["result"] == "timeout"
        assert outcome["r_realized"] is None
        assert outcome["outcome_reason"] == "no_post_entry_candles"

    def test_max_bars_exhausted_timeout(self):
        # entry=3258, sl=3248, tp=3278 — small-range candles never hit
        candles = self._neutral_candles(5)
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", candles, max_bars=5)
        assert outcome["result"] == "timeout"
        assert outcome["outcome_reason"] == "max_bars_reached"
        assert outcome["bars_held"] == 5

    def test_exit_fields_none_on_timeout(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", [])
        assert outcome["exit_price"] is None
        assert outcome["exit_ts"] is None

    def test_tp_in_outcome_even_on_timeout(self):
        outcome = resolve_exit_outcome(3258.0, 3248.0, 2.0, "bullish", [])
        assert outcome["tp"] == 3278.0


# ── get_post_entry_candles ────────────────────────────────────────────────────

class TestGetPostEntryCandles:
    def _rows(self):
        tz = ZoneInfo("America/Montreal")
        return [
            {"ts": datetime(2026, 4, 7, 18, 4, tzinfo=tz), "open": 3257.0, "high": 3259.0, "low": 3255.0, "close": 3258.0},
            {"ts": datetime(2026, 4, 7, 18, 5, tzinfo=tz), "open": 3258.0, "high": 3260.0, "low": 3257.0, "close": 3259.5},
            {"ts": datetime(2026, 4, 7, 18, 6, tzinfo=tz), "open": 3259.5, "high": 3262.0, "low": 3259.0, "close": 3261.0},
            {"ts": datetime(2026, 4, 7, 18, 7, tzinfo=tz), "open": 3261.0, "high": 3264.0, "low": 3260.5, "close": 3263.5},
        ]

    def test_filters_strictly_after_entry_ts(self):
        rows = self._rows()
        # entry at 18:04 → return rows at 18:05, 18:06, 18:07
        post = get_post_entry_candles(rows, "2026-04-07T18:04:00-04:00", "America/Montreal")
        assert len(post) == 3
        assert all(r["ts"] > datetime(2026, 4, 7, 18, 4, tzinfo=ZoneInfo("America/Montreal")) for r in post)

    def test_entry_ts_equal_row_excluded(self):
        rows = self._rows()
        post = get_post_entry_candles(rows, "2026-04-07T18:05:00-04:00", "America/Montreal")
        assert len(post) == 2

    def test_all_before_entry_returns_empty(self):
        rows = self._rows()
        post = get_post_entry_candles(rows, "2026-04-07T18:09:00-04:00", "America/Montreal")
        assert post == []

    def test_naive_entry_ts_treated_as_local(self):
        rows = self._rows()
        post = get_post_entry_candles(rows, "2026-04-07T18:04:00", "America/Montreal")
        assert len(post) == 3
