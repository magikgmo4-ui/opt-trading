from __future__ import annotations

import logging
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.trading_lab_v1.app import trading_lab_v1


PROFILE_WITH_KNOWN_ID = """version: \"1\"
profile_id: \"xauusd_dual_stack_v1\"
frame:
  timezone: \"America/Montreal\"
  symbol: \"XAUUSD\"
  sessions:
    - session_id: \"open_1800\"
      enabled: true
strategy:
  strategy_id: \"xau_session_open_v1\"
  variants:
    - variant_id: \"xau_open_sweep_fvg\"
      enabled: true
"""


PROFILE_WITH_UNKNOWN_ID = """version: \"1\"
profile_id: \"xauusd_dual_stack_v1\"
frame:
  timezone: \"America/Montreal\"
  symbol: \"XAUUSD\"
  sessions:
    - session_id: \"open_1800\"
      enabled: true
strategy:
  strategy_id: \"unknown_strategy_v99\"
  variants:
    - variant_id: \"xau_open_sweep_fvg\"
      enabled: true
"""


PROFILE_WITHOUT_ID = """version: \"1\"
profile_id: \"xauusd_dual_stack_v1\"
frame:
  timezone: \"America/Montreal\"
  symbol: \"XAUUSD\"
  sessions:
    - session_id: \"open_1800\"
      enabled: true
strategy:
  variants:
    - variant_id: \"xau_open_sweep_fvg\"
      enabled: true
"""


def _write_profile(tmp_path: Path, content: str) -> Path:
    profile_path = tmp_path / "xauusd_dual_stack_v1.profile.yaml"
    profile_path.write_text(content, encoding="utf-8")
    return profile_path


def _features() -> dict:
    return {
        "feature_id": "feat_20260518_010101_open_1800",
        "feature_ts": "2026-05-18T01:01:01-04:00",
        "profile_id": "xauusd_dual_stack_v1",
        "symbol": "XAUUSD",
        "session_name": "open_1800",
        "local_date": "2026-05-18",
        "timezone": "America/Montreal",
        "source_csv": "sample_xauusd_m1.csv",
        "sequence_complete": True,
        "variant_id": "xau_open_sweep_fvg",
        "first5_direction": "bearish",
    }


def _session() -> dict:
    return {
        "session_id": "open_1800",
        "signal_window_start": "18:00",
        "signal_window_end": "18:05",
    }


def test_known_strategy_id_silent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    monkeypatch.setattr(trading_lab_v1, "PROFILE_PATH", _write_profile(tmp_path, PROFILE_WITH_KNOWN_ID))
    caplog.set_level(logging.WARNING)

    profile = trading_lab_v1.load_profile()
    event = trading_lab_v1.build_market_event(profile, _session(), _features())

    assert event["strategy_id"] == "xau_session_open_v1"
    assert not any("unknown" in rec.message for rec in caplog.records)


def test_unknown_strategy_id_warns(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    monkeypatch.setattr(trading_lab_v1, "PROFILE_PATH", _write_profile(tmp_path, PROFILE_WITH_UNKNOWN_ID))
    caplog.set_level(logging.WARNING)

    profile = trading_lab_v1.load_profile()
    event = trading_lab_v1.build_market_event(profile, _session(), _features())

    assert event["strategy_id"] == "unknown_strategy_v99"
    assert any("unknown profile strategy_id" in rec.message for rec in caplog.records)


def test_missing_strategy_id_uses_and_validates_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    monkeypatch.setattr(trading_lab_v1, "PROFILE_PATH", _write_profile(tmp_path, PROFILE_WITHOUT_ID))
    caplog.set_level(logging.WARNING)

    profile = trading_lab_v1.load_profile()
    event = trading_lab_v1.build_market_event(profile, _session(), _features())

    assert event["strategy_id"] == "xau_session_open_v1"
    assert not any("unknown" in rec.message for rec in caplog.records)


def test_build_market_event_output_unchanged_except_warning_side_effect(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(trading_lab_v1, "PROFILE_PATH", _write_profile(tmp_path, PROFILE_WITH_KNOWN_ID))

    profile = trading_lab_v1.load_profile()
    event = trading_lab_v1.build_market_event(profile, _session(), _features())

    assert event["event_type"] == "setup_classified"
    assert event["decision_state"] == "observed"
    assert event["variant_id"] == "xau_open_sweep_fvg"
    assert event["symbol"] == "XAUUSD"
    assert event["strategy_id"] == "xau_session_open_v1"
