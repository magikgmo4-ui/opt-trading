"""
Smoke tests for read-only strategy_id adapter integration
in trading_realtime_v1.

Run: pytest modules/trading_realtime_v1/tests/test_strategy_id_adapter_readonly.py -q
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.strategy.adapter import validate_strategy_id


def test_strategy_id_xau_session_open_v1_is_registered():
    assert validate_strategy_id("xau_session_open_v1") is True


def test_import_runtime_loop_does_not_raise():
    from modules.trading_realtime_v1.app import runtime_loop_v1
    assert runtime_loop_v1.STRATEGY_ID == "xau_session_open_v1"


def test_import_event_bridge_does_not_raise():
    from modules.trading_realtime_v1.app import event_bridge_v1
    assert event_bridge_v1.STRATEGY_ID == "xau_session_open_v1"
