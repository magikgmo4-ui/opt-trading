"""
Tests for tools/trading_lab/collect_dukascopy_xauusd_m1.py

Run: pytest tools/trading_lab/tests/test_collect_dukascopy_m1.py -q
"""
from __future__ import annotations

import csv
import lzma
import struct
from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock
from zoneinfo import ZoneInfo
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.trading_lab.collect_dukascopy_xauusd_m1 import (
    build_url,
    decode_day,
    fetch_raw,
    collect,
    PRICE_DIVISOR,
    TZ_LOCAL,
    TZ_UTC,
)


# ── build_url ────────────────────────────────────────────────────────────────

class TestBuildUrl:
    def test_month_zero_indexed(self):
        url = build_url("XAUUSD", date(2026, 4, 7))
        assert "/2026/03/07/" in url

    def test_january_is_00(self):
        url = build_url("XAUUSD", date(2026, 1, 1))
        assert "/2026/00/01/" in url

    def test_december_is_11(self):
        url = build_url("XAUUSD", date(2026, 12, 31))
        assert "/2026/11/31/" in url

    def test_symbol_in_url(self):
        url = build_url("XAUUSD", date(2026, 4, 7))
        assert "XAUUSD" in url

    def test_bid_candles_min_1(self):
        url = build_url("XAUUSD", date(2026, 4, 7))
        assert "BID_candles_min_1.bi5" in url


# ── decode_day ───────────────────────────────────────────────────────────────

def _make_bi5(records: list[tuple]) -> bytes:
    """Build a minimal bi5 payload (uncompressed then LZMA-compressed)."""
    raw = b""
    for t_sec, o, c, lo, hi, vol in records:
        raw += struct.pack(">IIIIIf", t_sec, o, c, lo, hi, vol)
    return lzma.compress(raw)


class TestDecodeDay:
    def _simple_record(self):
        # price ~4659, field order: time_s, open, close, low, high, volume
        o  = int(4659.155 * PRICE_DIVISOR)
        cl = int(4651.375 * PRICE_DIVISOR)
        lo = int(4649.775 * PRICE_DIVISOR)
        hi = int(4659.155 * PRICE_DIVISOR)
        return (0, o, cl, lo, hi, 0.04)

    def test_single_record_count(self):
        bi5 = _make_bi5([self._simple_record()])
        candles = decode_day(bi5, date(2026, 4, 7))
        assert len(candles) == 1

    def test_open_high_low_close_fields(self):
        bi5 = _make_bi5([self._simple_record()])
        c = decode_day(bi5, date(2026, 4, 7))[0]
        assert c["high"] >= max(c["open"], c["close"])
        assert c["low"]  <= min(c["open"], c["close"])

    def test_timestamp_utc_to_local(self):
        # t_sec=0 → midnight UTC on 2026-04-07 = 20:00 ET (UTC-4)
        bi5 = _make_bi5([self._simple_record()])
        c = decode_day(bi5, date(2026, 4, 7))[0]
        assert c["ts"].tzinfo is not None
        assert c["ts"].utcoffset().total_seconds() == -4 * 3600  # EDT

    def test_timestamp_offset_within_day(self):
        # t_sec = 22*3600 = 79200 → 22:00 UTC = 18:00 ET
        rec = (79200, int(4718 * PRICE_DIVISOR), int(4747 * PRICE_DIVISOR),
               int(4718 * PRICE_DIVISOR), int(4747 * PRICE_DIVISOR), 0.06)
        bi5 = _make_bi5([rec])
        c = decode_day(bi5, date(2026, 4, 7))[0]
        assert c["ts"].hour == 18  # 22:00 UTC = 18:00 ET

    def test_invalid_ohlc_skipped(self):
        # hi < open → invalid
        bad = (0, int(4700 * PRICE_DIVISOR), int(4650 * PRICE_DIVISOR),
               int(4600 * PRICE_DIVISOR), int(4690 * PRICE_DIVISOR), 0.05)
        bi5 = _make_bi5([bad])
        candles = decode_day(bi5, date(2026, 4, 7))
        assert len(candles) == 0

    def test_empty_input_returns_empty(self):
        bi5 = lzma.compress(b"")
        assert decode_day(bi5, date(2026, 4, 7)) == []

    def test_malformed_lzma_returns_empty(self):
        assert decode_day(b"not lzma", date(2026, 4, 7)) == []

    def test_price_rounded_to_3dp(self):
        bi5 = _make_bi5([self._simple_record()])
        c = decode_day(bi5, date(2026, 4, 7))[0]
        for field in ("open", "high", "low", "close"):
            val = c[field]
            assert round(val, 3) == val


# ── fetch_raw ────────────────────────────────────────────────────────────────

class TestFetchRaw:
    def test_returns_none_on_network_error(self):
        with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.urllib.request.urlopen",
                   side_effect=OSError("timeout")):
            result = fetch_raw("http://fake/url")
        assert result is None

    def test_returns_bytes_on_success(self):
        mock_resp = MagicMock()
        mock_resp.read.return_value = b"data"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.urllib.request.urlopen",
                   return_value=mock_resp):
            result = fetch_raw("http://fake/url")
        assert result == b"data"


# ── collect ── (no network) ──────────────────────────────────────────────────

def _make_fake_raw(date_: date, n_records: int = 10) -> bytes:
    records = []
    for i in range(n_records):
        t_sec = i * 60
        base = int(4650 * PRICE_DIVISOR)
        records.append((t_sec, base, base - 100, base - 200, base, 0.03))
    return _make_bi5(records)


class TestCollect:
    def _mock_fetch_day(self, day_map: dict):
        """Return a mock for fetch_day that returns pre-built candles by date."""
        from tools.trading_lab.collect_dukascopy_xauusd_m1 import decode_day

        def _fetch(symbol, d):
            raw = day_map.get(d)
            if raw is None:
                return []
            return decode_day(raw, d)

        return _fetch

    def test_csv_header(self, tmp_path):
        raw = _make_fake_raw(date(2026, 4, 7), 3)
        day_map = {date(2026, 4, 7): raw, date(2026, 4, 8): raw}
        with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.fetch_day",
                   side_effect=self._mock_fetch_day(day_map)):
            with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.time_mod.sleep"):
                collect("XAUUSD", date(2026, 4, 7), date(2026, 4, 7),
                        tmp_path / "out.csv", delay=0)
        with open(tmp_path / "out.csv") as f:
            reader = csv.reader(f)
            header = next(reader)
        assert header == ["timestamp", "open", "high", "low", "close", "volume"]

    def test_csv_rows_written(self, tmp_path):
        raw = _make_fake_raw(date(2026, 4, 7), 5)
        day_map = {date(2026, 4, 7): raw, date(2026, 4, 8): raw}
        with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.fetch_day",
                   side_effect=self._mock_fetch_day(day_map)):
            with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.time_mod.sleep"):
                summary = collect("XAUUSD", date(2026, 4, 7), date(2026, 4, 7),
                                  tmp_path / "out.csv", delay=0)
        assert summary["rows"] > 0

    def test_summary_contains_expected_keys(self, tmp_path):
        day_map = {}
        with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.fetch_day",
                   side_effect=self._mock_fetch_day(day_map)):
            with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.time_mod.sleep"):
                summary = collect("XAUUSD", date(2026, 4, 7), date(2026, 4, 7),
                                  tmp_path / "out.csv", delay=0)
        for key in ("rows", "days_fetched", "days_empty", "dates_covered", "first_ts", "last_ts", "out"):
            assert key in summary

    def test_timestamps_are_tz_aware_in_csv(self, tmp_path):
        raw = _make_fake_raw(date(2026, 4, 7), 3)
        day_map = {date(2026, 4, 7): raw, date(2026, 4, 8): raw}
        with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.fetch_day",
                   side_effect=self._mock_fetch_day(day_map)):
            with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.time_mod.sleep"):
                collect("XAUUSD", date(2026, 4, 7), date(2026, 4, 7),
                        tmp_path / "out.csv", delay=0)
        with open(tmp_path / "out.csv") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if rows:
            ts = datetime.fromisoformat(rows[0]["timestamp"])
            assert ts.tzinfo is not None

    def test_output_sorted_by_timestamp(self, tmp_path):
        raw = _make_fake_raw(date(2026, 4, 7), 5)
        day_map = {date(2026, 4, 7): raw, date(2026, 4, 8): raw}
        with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.fetch_day",
                   side_effect=self._mock_fetch_day(day_map)):
            with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.time_mod.sleep"):
                collect("XAUUSD", date(2026, 4, 7), date(2026, 4, 7),
                        tmp_path / "out.csv", delay=0)
        with open(tmp_path / "out.csv") as f:
            reader = csv.DictReader(f)
            ts_list = [datetime.fromisoformat(r["timestamp"]) for r in reader]
        assert ts_list == sorted(ts_list)

    def test_empty_days_produce_empty_csv(self, tmp_path):
        with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.fetch_day",
                   return_value=[]):
            with patch("tools.trading_lab.collect_dukascopy_xauusd_m1.time_mod.sleep"):
                summary = collect("XAUUSD", date(2026, 4, 7), date(2026, 4, 7),
                                  tmp_path / "out.csv", delay=0)
        assert summary["rows"] == 0
        assert (tmp_path / "out.csv").exists()


# ── main (CLI) ────────────────────────────────────────────────────────────────

class TestMain:
    def test_end_before_start_returns_1(self, tmp_path):
        from tools.trading_lab.collect_dukascopy_xauusd_m1 import main
        ret = main([
            "--start", "2026-04-10",
            "--end",   "2026-04-07",
            "--out",   str(tmp_path / "out.csv"),
        ])
        assert ret == 1
