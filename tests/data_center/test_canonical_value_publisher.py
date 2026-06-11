"""Tests for canonical_value_publisher.py — P03-P05."""

import pytest
from unittest.mock import patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

COINGLASS_PAYLOAD = {
    "input_class": "vision_context.coinglass.v1",
    "source_id": "coinglass_headless_bot", "symbol": "BTCUSDT", "freshness_state": "fresh",
    "detections": [{"detected_metric_type": "open_interest", "extracted_value": 102899875.114}],
}

MOCK_WIN = {
    "resolver_decision": {
        "decision_id": "dec-001", "contract_class": "vision_context.coinglass.v1",
        "symbol": "BTCUSDT", "data_key": "open_interest", "selected_producer_id": "coinglass_headless_bot",
        "selected_score": 0.9, "selection_rule": "highest_score", "candidates": [],
        "schema_version": "resolver_decision.v1", "decided_at": "2026-06-11T00:00:00Z",
        "selection_reason": "test", "min_score_threshold": 0.3,
        "resolver_version": "best_value_resolver.v1",
    },
    "canonical_value": {
        "canonical_value": None, "winning_producer_id": "coinglass_headless_bot",
        "winning_score": 0.9, "alternative_sources": [], "stale": False,
        "schema_version": "canonical_value.v1", "resolved_at": "2026-06-11T00:00:00Z",
        "resolver_decision_ref": "dec-001", "contract_class": "vision_context.coinglass.v1",
        "symbol": "BTCUSDT", "data_key": "open_interest",
    },
}

MOCK_STALE = {
    "resolver_decision": {
        "decision_id": "dec-002", "contract_class": "vision_context.coinglass.v1",
        "symbol": "BTCUSDT", "data_key": "open_interest", "selected_producer_id": None,
        "selection_rule": "stale_fallback", "candidates": [],
        "schema_version": "resolver_decision.v1", "decided_at": "2026-06-11T00:00:00Z",
        "selection_reason": "no_candidates", "min_score_threshold": 0.3,
        "resolver_version": "best_value_resolver.v1", "selected_score": 0,
    },
    "canonical_value": {
        "canonical_value": None, "winning_producer_id": None,
        "winning_score": 0, "alternative_sources": [], "stale": True,
        "schema_version": "canonical_value.v1", "resolved_at": "2026-06-11T00:00:00Z",
        "resolver_decision_ref": "dec-002", "contract_class": "vision_context.coinglass.v1",
        "symbol": "BTCUSDT", "data_key": "open_interest",
    },
}

# Patch paths for the imported module references in canonical_value_publisher
# The publisher uses: _source_selector.resolve(), _payload_reader.read_latest_payload(), etc.
# So we patch the source modules directly.
PATCH_BASE = [
    patch("modules.data_center.canonical_value_publisher._atomic_write"),
    patch("modules.data_center.runtime_registry.update_producer_last_write"),
    patch("modules.data_center.source_selector.resolve"),
    patch("modules.data_center.producer_payload_reader.read_latest_payload"),
    patch("modules.data_center.producer_payload_reader.extract_value"),
    patch("modules.data_center.producer_payload_reader.validate_payload_shape"),
]


class TestCanonicalValuePublisher:

    def test_p03_resolve_with_real_value(self):
        with patch("modules.data_center.canonical_value_publisher._atomic_write"), \
             patch("modules.data_center.runtime_registry.update_producer_last_write"), \
             patch("modules.data_center.source_selector.resolve") as mr, \
             patch("modules.data_center.producer_payload_reader.read_latest_payload") as mrl, \
             patch("modules.data_center.producer_payload_reader.extract_value") as me, \
             patch("modules.data_center.producer_payload_reader.validate_payload_shape") as mv:
            mr.return_value = MOCK_WIN
            mrl.return_value = COINGLASS_PAYLOAD
            me.return_value = 102899875.114
            mv.return_value = (True, [])

            from modules.data_center.canonical_value_publisher import resolve_and_publish
            result = resolve_and_publish("vision_context.coinglass.v1", "BTCUSDT", "open_interest")
            assert result["canonical_value"]["canonical_value"] == 102899875.114
            assert result["canonical_value"]["stale"] is False

    def test_p04_payload_missing_returns_stale(self):
        with patch("modules.data_center.canonical_value_publisher._atomic_write"), \
             patch("modules.data_center.runtime_registry.update_producer_last_write"), \
             patch("modules.data_center.source_selector.resolve") as mr, \
             patch("modules.data_center.producer_payload_reader.read_latest_payload") as mrl, \
             patch("modules.data_center.producer_payload_reader.extract_value") as me, \
             patch("modules.data_center.producer_payload_reader.validate_payload_shape") as mv:
            mr.return_value = MOCK_WIN
            mrl.return_value = None
            me.return_value = None
            mv.return_value = (False, ["not found"])

            from modules.data_center.canonical_value_publisher import resolve_and_publish
            result = resolve_and_publish("vision_context.coinglass.v1", "BTCUSDT", "open_interest")
            assert result["canonical_value"]["canonical_value"] is None
            assert result["canonical_value"]["stale"] is True

    def test_p05_no_candidates_returns_stale(self):
        with patch("modules.data_center.canonical_value_publisher._atomic_write"), \
             patch("modules.data_center.runtime_registry.update_producer_last_write"), \
             patch("modules.data_center.source_selector.resolve") as mr, \
             patch("modules.data_center.producer_payload_reader.read_latest_payload") as mrl, \
             patch("modules.data_center.producer_payload_reader.extract_value") as me, \
             patch("modules.data_center.producer_payload_reader.validate_payload_shape") as mv:
            mr.return_value = MOCK_STALE
            mrl.return_value = None
            me.return_value = None
            mv.return_value = (False, [])

            from modules.data_center.canonical_value_publisher import resolve_and_publish
            result = resolve_and_publish("vision_context.coinglass.v1", "BTCUSDT", "open_interest")
            assert result["canonical_value"]["canonical_value"] is None
            assert result["canonical_value"]["stale"] is True
            assert result["resolver_decision"]["selection_rule"] == "stale_fallback"

    def test_publish_batch(self):
        from copy import deepcopy
        with patch("modules.data_center.canonical_value_publisher._atomic_write"), \
             patch("modules.data_center.runtime_registry.update_producer_last_write"), \
             patch("modules.data_center.source_selector.resolve") as mr, \
             patch("modules.data_center.producer_payload_reader.read_latest_payload") as mrl, \
             patch("modules.data_center.producer_payload_reader.extract_value") as me, \
             patch("modules.data_center.producer_payload_reader.validate_payload_shape") as mv:
            # Return fresh copies each time to prevent shared-mutation
            mr.side_effect = lambda *a, **kw: deepcopy(MOCK_WIN)
            mrl.return_value = COINGLASS_PAYLOAD
            me.side_effect = [235.3, 172.03, 50.57]
            mv.return_value = (True, [])

            from modules.data_center.canonical_value_publisher import publish_batch
            results = publish_batch("vision_context.coinglass.v1", [
                ("BTCUSDT", "liquidations_long"),
                ("BTCUSDT", "liquidations_short"),
                ("BTCUSDT", "long_short_ratio"),
            ])
            assert len(results) == 3
            assert results[0]["canonical_value"]["canonical_value"] == 235.3
            assert results[1]["canonical_value"]["canonical_value"] == 172.03
            assert results[2]["canonical_value"]["canonical_value"] == 50.57
