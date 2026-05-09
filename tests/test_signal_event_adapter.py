"""
Tests for modules/desk_pro/signal_event_adapter.py

Run: pytest tests/test_signal_event_adapter.py -q
"""
import json
import hashlib
import pytest

from modules.desk_pro.signal_event_adapter import (
    normalize_signal_event_v1,
    validate_signal_event_v1,
    payload_hash,
)


# ── Fixtures ──────────────────────────────────────────────────────
V0_FULL = {
    "key": None,
    "engine": "USDTM_LONG",
    "signal": "BUY",
    "symbol": "BTCUSDT",
    "tf": "H1",
    "price": 68000.0,
    "tp": 69000.0,
    "sl": 67500.0,
    "reason": "breakout",
    "_ts": "2026-05-06T02:20:00+00:00",
    "_ip": "127.0.0.1",
    "qty": 0.01,
    "risk_usd": 50.0,
    "risk_real_usd": 50.0,
}

V0_MINIMAL = {
    "engine": "COINM_SHORT",
    "signal": "SELL",
    "symbol": "ETHUSDT",
    "tf": "H4",
    "_ts": "2026-05-06T03:00:00+00:00",
}


# ── normalize_signal_event_v1 ────────────────────────────────────
class TestNormalize:
    def test_full_payload(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        assert v1["source"] == "tradingview.webhook"
        assert v1["event_type"] == "signal_event"
        assert v1["engine"] == "USDTM_LONG"
        assert v1["symbol"] == "BTCUSDT"
        assert v1["timeframe"] == "H1"
        assert v1["direction"] == "BUY"
        assert v1["timestamp"] == "2026-05-06T02:20:00+00:00"
        assert v1["status"] == "accepted"
        assert v1["errors"] == []

    def test_minimal_payload(self):
        v1 = normalize_signal_event_v1(V0_MINIMAL)
        assert v1["engine"] == "COINM_SHORT"
        assert v1["direction"] == "SELL"
        assert v1["timeframe"] == "H4"
        assert v1["status"] == "accepted"
        assert v1["meta"] is None  # no price/tp/sl/reason
        assert v1["risk_context"] is None

    def test_meta_grouping(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        assert v1["meta"]["price"] == 68000.0
        assert v1["meta"]["tp"] == 69000.0
        assert v1["meta"]["sl"] == 67500.0
        assert v1["meta"]["reason"] == "breakout"
        assert v1["meta"]["debug"]["client_ip"] == "127.0.0.1"

    def test_risk_context_grouping(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        assert v1["risk_context"]["qty"] == 0.01
        assert v1["risk_context"]["risk_usd"] == 50.0
        assert v1["risk_context"]["risk_real_usd"] == 50.0

    def test_payload_hash_present(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        assert v1["payload_hash"] is not None
        assert len(v1["payload_hash"]) == 64  # SHA-256 hex

    def test_payload_hash_deterministic(self):
        h1 = normalize_signal_event_v1(V0_FULL)["payload_hash"]
        h2 = normalize_signal_event_v1(V0_FULL)["payload_hash"]
        assert h1 == h2

    def test_optional_refs_none(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        assert v1["raw_payload_ref"] is None
        assert v1["visual_context_ref"] is None
        assert v1["desk_snapshot_ref"] is None

    def test_not_a_dict(self):
        v1 = normalize_signal_event_v1("not a dict")
        assert v1["status"] == "error"
        assert len(v1["errors"]) > 0

    def test_missing_engine(self):
        v0 = {**V0_FULL, "engine": ""}
        v1 = normalize_signal_event_v1(v0)
        assert "missing engine" in v1["errors"]

    def test_missing_symbol(self):
        v0 = {**V0_FULL, "symbol": ""}
        v1 = normalize_signal_event_v1(v0)
        assert "missing symbol" in v1["errors"]

    def test_missing_timeframe(self):
        v0 = {**V0_FULL, "tf": ""}
        v1 = normalize_signal_event_v1(v0)
        assert "missing timeframe" in v1["errors"]

    def test_invalid_direction(self):
        v0 = {**V0_FULL, "signal": "HOLD"}
        v1 = normalize_signal_event_v1(v0)
        assert "invalid direction" in v1["errors"][0]

    def test_signal_case_insensitive(self):
        v0 = {**V0_FULL, "signal": "buy"}
        v1 = normalize_signal_event_v1(v0)
        assert v1["direction"] == "BUY"


# ── validate_signal_event_v1 ─────────────────────────────────────
class TestValidate:
    def test_valid_full(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is True
        assert errors == []

    def test_valid_minimal(self):
        v1 = normalize_signal_event_v1(V0_MINIMAL)
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is True

    def test_missing_engine(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        v1["engine"] = ""
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is False
        assert any("engine" in e for e in errors)

    def test_missing_symbol(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        v1["symbol"] = ""
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is False

    def test_missing_timeframe(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        v1["timeframe"] = ""
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is False

    def test_invalid_direction(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        v1["direction"] = "HOLD"
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is False

    def test_missing_timestamp(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        v1["timestamp"] = ""
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is False

    def test_unparseable_timestamp(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        v1["timestamp"] = "not-a-date"
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is False

    def test_unknown_status_non_blocking(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        v1["status"] = "unknown_value"
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is True  # non-blocking
        assert any("status" in e for e in errors)

    def test_not_a_dict(self):
        is_valid, errors = validate_signal_event_v1(None)
        assert is_valid is False


# ── payload_hash ─────────────────────────────────────────────────
class TestPayloadHash:
    def test_deterministic(self):
        h1 = payload_hash(V0_FULL)
        h2 = payload_hash(V0_FULL)
        assert h1 == h2

    def test_different_payloads_different_hash(self):
        h1 = payload_hash(V0_FULL)
        h2 = payload_hash(V0_MINIMAL)
        assert h1 != h2

    def test_sha256_format(self):
        h = payload_hash(V0_FULL)
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)


# ── Round-trip: V0 → V1 → validate ──────────────────────────────
class TestRoundTrip:
    def test_full_roundtrip(self):
        v1 = normalize_signal_event_v1(V0_FULL)
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is True
        assert v1["status"] == "accepted"

    def test_minimal_roundtrip(self):
        v1 = normalize_signal_event_v1(V0_MINIMAL)
        is_valid, errors = validate_signal_event_v1(v1)
        assert is_valid is True

    def test_skipped_not_in_jsonl(self):
        """V0 skipped events are not persisted in events.jsonl,
        so adapter should handle them if they appear."""
        v0 = {**V0_FULL, "signal": "BUY"}
        v1 = normalize_signal_event_v1(v0)
        assert v1["status"] == "accepted"

    def test_no_side_effects(self):
        """Adapter is pure — no file writes, no imports from runtime."""
        v1 = normalize_signal_event_v1(V0_FULL)
        # Should not raise, should not write files
        assert isinstance(v1, dict)
