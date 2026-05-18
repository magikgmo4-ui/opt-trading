"""
Smoke tests for read-only strategy_id adapter integration
in notification_dispatcher.

Run: pytest modules/notification_dispatcher/tests/test_strategy_id_adapter_readonly.py -q
"""

import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest
from modules.notification_dispatcher.app.dispatcher import NotificationDispatcher
from modules.notification_dispatcher.app.events import PipelineEvent
from modules.strategy.adapter import validate_strategy_id

KNOWN_ID = "xau_session_open_v1"
UNKNOWN_ID = "unknown_strategy_v99"


def _event(payload: dict = None) -> PipelineEvent:
    return PipelineEvent(
        event_type="signal_received",
        payload=payload or {},
    )


def test_known_strategy_id_silent(caplog):
    caplog.set_level(logging.WARNING)
    e = _event({"ticker": "BTCUSDT", "side": "BUY", "price": 65000, "tf": "1h", "strategy_id": KNOWN_ID})
    result = NotificationDispatcher().dispatch(e, dry_run=True)
    assert result["ok"] is True
    assert not any("unknown strategy_id" in rec.message for rec in caplog.records)


def test_unknown_strategy_id_warns(caplog):
    caplog.set_level(logging.WARNING)
    e = _event({"ticker": "BTCUSDT", "side": "BUY", "price": 65000, "tf": "1h", "strategy_id": UNKNOWN_ID})
    result = NotificationDispatcher().dispatch(e, dry_run=True)
    assert result["ok"] is True
    assert any("unknown strategy_id" in rec.message for rec in caplog.records)


def test_no_strategy_id_no_validation(caplog):
    caplog.set_level(logging.WARNING)
    e = _event({"ticker": "BTCUSDT", "side": "BUY", "price": 65000, "tf": "1h"})
    result = NotificationDispatcher().dispatch(e, dry_run=True)
    assert result["ok"] is True
    assert not any("unknown strategy_id" in rec.message for rec in caplog.records)


def test_message_output_unchanged_for_known():
    e = _event({"ticker": "ETHUSDT", "side": "SELL", "price": 3200, "tf": "4h", "strategy_id": KNOWN_ID})
    result = NotificationDispatcher().dispatch(e, dry_run=True)
    assert "ETHUSDT" in result["message"]
    assert "SELL" in result["message"]
    assert "3200" in result["message"]
    assert KNOWN_ID in result["message"]


def test_message_output_unchanged_for_unknown():
    e = _event({"ticker": "ETHUSDT", "side": "SELL", "price": 3200, "tf": "4h", "strategy_id": UNKNOWN_ID})
    result = NotificationDispatcher().dispatch(e, dry_run=True)
    assert "ETHUSDT" in result["message"]
    assert "SELL" in result["message"]
    assert UNKNOWN_ID in result["message"]


def test_strategy_id_known_in_registry():
    assert validate_strategy_id(KNOWN_ID) is True


def test_strategy_id_unknown_not_in_registry():
    assert validate_strategy_id(UNKNOWN_ID) is False
