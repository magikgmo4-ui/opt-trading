"""
Smoke tests for read-only strategy_id adapter integration
in proposition_engine.

Run: pytest modules/proposition_engine/tests/test_strategy_id_adapter_readonly.py -q
"""

import logging
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest
from modules.proposition_engine.app.schema import NormalizedSignal, PropositionRequest
from modules.proposition_engine.app.engine import PropositionEngine
from modules.strategy.adapter import validate_strategy_id

KNOWN_ID = "xau_session_open_v1"
UNKNOWN_ID = "unknown_strategy_v99"


def _signal(strategy_id=KNOWN_ID, side="BUY", ticker="BTCUSDT", price=65000.0):
    return NormalizedSignal(
        signal_id="test-sig-001",
        ticker=ticker,
        side=side,
        price=price,
        timestamp=time.time(),
        strategy_id=strategy_id,
        tf="1h",
    )


def test_known_strategy_id_silent(caplog):
    caplog.set_level(logging.WARNING)
    eng = PropositionEngine()
    req = PropositionRequest(signal=_signal(KNOWN_ID), dry_run=True)
    prop = eng.propose(req)
    assert prop.status == "ok"
    assert not any("STRATEGY_ID_UNKNOWN" in rec.message for rec in caplog.records)


def test_unknown_strategy_id_warns(caplog):
    caplog.set_level(logging.WARNING)
    eng = PropositionEngine()
    req = PropositionRequest(signal=_signal(UNKNOWN_ID), dry_run=True)
    prop = eng.propose(req)
    assert prop.status == "ok"
    assert any("STRATEGY_ID_UNKNOWN" in rec.message for rec in caplog.records)
    assert prop.action == "HOLD"


def test_known_strategy_id_proposal_output_unchanged():
    def get_proposal(sid):
        eng = PropositionEngine()
        req = PropositionRequest(signal=_signal(sid, price=70000.0), dry_run=True)
        return eng.propose(req)

    known = get_proposal(KNOWN_ID)
    unknown = get_proposal(UNKNOWN_ID)

    assert known.action == unknown.action == "HOLD"
    assert known.entry == unknown.entry == 70000.0
    assert known.dry_run is True
    assert known.status == "ok"


def test_strategy_id_known_in_registry():
    assert validate_strategy_id(KNOWN_ID) is True


def test_strategy_id_unknown_not_in_registry():
    assert validate_strategy_id(UNKNOWN_ID) is False
