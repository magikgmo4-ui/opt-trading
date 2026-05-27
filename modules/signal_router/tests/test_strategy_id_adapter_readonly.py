"""
Smoke tests for read-only strategy_id adapter integration
in signal_router.

Run: pytest modules/signal_router/tests/test_strategy_id_adapter_readonly.py -q
"""

import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest
from modules.signal_router.app.router import route
from modules.strategy.adapter import validate_strategy_id

KNOWN_ID = "xau_session_open_v1"
UNKNOWN_ID = "unknown_strategy_v99"


def test_import_router_does_not_raise():
    from modules.signal_router.app import router
    assert router is not None


def test_known_strategy_id_silent(caplog):
    caplog.set_level(logging.WARNING)
    raw = {
        "engine": "test_engine",
        "signal": "BUY",
        "symbol": "BTCUSDT",
        "tf": "1h",
        "price": "65000",
        "strategy_id": KNOWN_ID,
    }
    ns = route(raw)
    assert ns.strategy_id == KNOWN_ID
    assert not any("STRATEGY_ID_UNKNOWN" in rec.message for rec in caplog.records)


def test_unknown_strategy_id_warns(caplog):
    caplog.set_level(logging.WARNING)
    raw = {
        "engine": "test_engine",
        "signal": "SELL",
        "symbol": "ETHUSDT",
        "tf": "4h",
        "price": "3200",
        "strategy_id": UNKNOWN_ID,
    }
    ns = route(raw)
    assert ns.strategy_id == UNKNOWN_ID
    assert any("STRATEGY_ID_UNKNOWN" in rec.message for rec in caplog.records)


def test_signal_output_unchanged_for_known():
    raw = {
        "engine": "strat_v1",
        "signal": "BUY",
        "symbol": "BTCUSDT",
        "tf": "1h",
        "price": "65000",
        "tp": "67000",
        "sl": "63000",
        "reason": "breakout",
        "strategy_id": KNOWN_ID,
    }
    ns = route(raw)
    assert ns.ticker == "BTCUSDT"
    assert ns.side == "BUY"
    assert ns.price == 65000.0
    assert ns.tp == 67000.0
    assert ns.sl == 63000.0
    assert ns.reason == "breakout"
    assert ns.strategy_id == KNOWN_ID
    assert ns.tf == "1h"


def test_signal_output_unchanged_for_unknown():
    raw = {
        "engine": "strat_v2",
        "signal": "SELL",
        "symbol": "ETHUSDT",
        "tf": "4h",
        "price": "3200",
        "strategy_id": UNKNOWN_ID,
    }
    ns = route(raw)
    assert ns.ticker == "ETHUSDT"
    assert ns.side == "SELL"
    assert ns.price == 3200.0
    assert ns.strategy_id == UNKNOWN_ID


def test_strategy_id_known_in_registry():
    assert validate_strategy_id(KNOWN_ID) is True


def test_strategy_id_unknown_not_in_registry():
    assert validate_strategy_id(UNKNOWN_ID) is False
