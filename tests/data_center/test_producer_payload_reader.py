"""Tests for producer_payload_reader.py — P01-P02."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from modules.data_center.producer_payload_reader import (
    read_latest_payload,
    extract_value,
    validate_payload_shape,
)


COINGLASS_PAYLOAD = {
    "input_class": "vision_context.coinglass.v1",
    "source_id": "coinglass_headless_bot",
    "symbol": "BTCUSDT",
    "freshness_state": "fresh",
    "detections": [
        {"detected_metric_type": "open_interest", "extracted_value": 102899875.114, "confidence": 1.0},
        {"detected_metric_type": "liquidations_long", "extracted_value": 235.3, "confidence": 1.0},
        {"detected_metric_type": "liquidations_short", "extracted_value": 172.03, "confidence": 1.0},
        {"detected_metric_type": "long_short_ratio", "extracted_value": 50.57, "confidence": 1.0},
        {"detected_metric_type": "liquidation_heatmap_level", "extracted_value": 979.95, "confidence": 1.0},
    ],
}

VISION_ANALYSIS_PAYLOAD = {
    "input_class": "vision_analysis.v1",
    "symbol": "BTCUSDT.P",
    "freshness_state": "fresh",
    "signals": [
        {"type": "support_level", "value": 58000.0, "confidence": 0.75},
        {"type": "resistance_level", "value": 62000.0, "confidence": 0.70},
        {"type": "trend", "value": "bullish", "confidence": 0.80},
    ],
}

TELEGRAM_SIGNAL_PAYLOAD = {
    "input_class": "telegram_signals.v1",
    "provider_id": "telegram_screener_bridge",
    "signals": 258,
    "active_channels": 39,
    "produced_at": "2026-06-11T00:00:00Z",
}


class TestExtractValue:
    """P01 — extract values from producer payloads."""

    def test_extract_open_interest_from_coinglass(self):
        value = extract_value(COINGLASS_PAYLOAD, "vision_context.coinglass.v1", "BTCUSDT", "open_interest")
        assert value == 102899875.114

    def test_extract_liquidations_long(self):
        value = extract_value(COINGLASS_PAYLOAD, "vision_context.coinglass.v1", "BTCUSDT", "liquidations_long")
        assert value == 235.3

    def test_extract_liquidations_short(self):
        value = extract_value(COINGLASS_PAYLOAD, "vision_context.coinglass.v1", "BTCUSDT", "liquidations_short")
        assert value == 172.03

    def test_extract_long_short_ratio(self):
        value = extract_value(COINGLASS_PAYLOAD, "vision_context.coinglass.v1", "BTCUSDT", "long_short_ratio")
        assert value == 50.57

    def test_extract_heatmap_level(self):
        value = extract_value(COINGLASS_PAYLOAD, "vision_context.coinglass.v1", "BTCUSDT", "liquidation_heatmap_level")
        assert value == 979.95

    def test_extract_support_level(self):
        value = extract_value(VISION_ANALYSIS_PAYLOAD, "vision_analysis.v1", "BTCUSDT.P", "support_level")
        assert value == 58000.0

    def test_extract_resistance_level(self):
        value = extract_value(VISION_ANALYSIS_PAYLOAD, "vision_analysis.v1", "BTCUSDT.P", "resistance_level")
        assert value == 62000.0

    def test_extract_trend(self):
        value = extract_value(VISION_ANALYSIS_PAYLOAD, "vision_analysis.v1", "BTCUSDT.P", "trend")
        assert value == "bullish"

    def test_extract_signal_count(self):
        value = extract_value(TELEGRAM_SIGNAL_PAYLOAD, "telegram_signal.v1", "BTCUSDT", "signal_count")
        assert value == 258

    def test_extract_active_channels(self):
        value = extract_value(TELEGRAM_SIGNAL_PAYLOAD, "telegram_signal.v1", "BTCUSDT", "active_channels")
        assert value == 39

    def test_extract_nonexistent_key_returns_none(self):
        value = extract_value(COINGLASS_PAYLOAD, "vision_context.coinglass.v1", "BTCUSDT", "nonexistent_key")
        assert value is None


class TestValidatePayload:
    """P02 — validate payload shape."""

    def test_valid_payload(self):
        ok, errors = validate_payload_shape(COINGLASS_PAYLOAD, "vision_context.coinglass.v1")
        assert ok is True
        assert len(errors) == 0

    def test_stale_payload(self):
        payload = {**COINGLASS_PAYLOAD, "freshness_state": "stale"}
        ok, errors = validate_payload_shape(payload, "vision_context.coinglass.v1")
        assert ok is False
        assert any("stale" in e.lower() for e in errors)

    def test_input_class_mismatch(self):
        payload = {**COINGLASS_PAYLOAD, "input_class": "wrong.v1"}
        ok, errors = validate_payload_shape(payload, "vision_context.coinglass.v1")
        assert ok is False
        assert any("mismatch" in e.lower() for e in errors)

    def test_not_a_dict(self):
        ok, errors = validate_payload_shape([], "vision_context.coinglass.v1")  # type: ignore
        assert ok is False

    def test_missing_freshness(self):
        payload = {"input_class": "vision_context.coinglass.v1"}
        ok, errors = validate_payload_shape(payload, "vision_context.coinglass.v1")
        # No freshness_state → empty string → not "stale" → OK
        assert ok is True


class TestReadPayload:
    """P02 — read latest payload from disk."""

    def test_read_nonexistent_returns_none(self):
        # Contract with no paths registered
        result = read_latest_payload("unknown_producer", "nonexistent.v1")
        assert result is None

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.read_text")
    def test_read_valid_payload(self, mock_read, mock_exists):
        mock_read.return_value = json.dumps(COINGLASS_PAYLOAD)
        result = read_latest_payload("coinglass_headless_bot", "vision_context.coinglass.v1")
        assert result is not None
        assert result["input_class"] == "vision_context.coinglass.v1"
        assert result["symbol"] == "BTCUSDT"
