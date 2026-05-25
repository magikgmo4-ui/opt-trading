import json
from pathlib import Path

from modules.desk_pro.dry_run import (
    build_desk_pro_dry_run_synthesis,
    run_desk_pro_dry_run,
    validate_desk_pro_dry_run_inputs,
)
from modules.desk_pro.signal_event_adapter import normalize_signal_event_v1


FIXTURES = Path(__file__).parent / "fixtures" / "admin_trading_contract_smoke"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class TestDeskProDryRun:
    def test_dry_run_accepts_v0_minimal_via_adapter(self):
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap)
        assert result["signal_event"]["event_type"] == "signal_event"
        assert result["status"] == "WARN"

    def test_dry_run_accepts_v1_already_normalized(self):
        v0 = _load("signal_event_v0_complete.json")
        v1 = normalize_signal_event_v1(v0)
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v1, desk_snapshot=snap)
        assert result["signal_event"]["direction"] == "BUY"
        assert result["status"] == "WARN"

    def test_dry_run_accepts_visual_context_v1(self):
        v0 = _load("signal_event_v0_minimal.json")
        vc = _load("visual_context_v1_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v0, visual_context=vc, desk_snapshot=snap)
        assert result["visual_context"]["capture_id"] == vc["capture_id"]

    def test_dry_run_accepts_desk_snapshot(self):
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap)
        assert result["desk_snapshot"]["path"] == snap["path"]

    def test_dry_run_produces_synthesis_with_no_trade(self):
        v0 = _load("signal_event_v0_complete.json")
        vc = _load("visual_context_v1_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        result = build_desk_pro_dry_run_synthesis(v0, vc, snap)
        assert result["no_trade"] is True

    def test_dry_run_produces_no_telegram(self):
        v0 = _load("signal_event_v0_complete.json")
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap)
        assert result["no_telegram"] is True

    def test_dry_run_produces_no_webhook(self):
        v0 = _load("signal_event_v0_complete.json")
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap)
        assert result["no_webhook"] is True

    def test_missing_optional_visual_context_is_warn_non_blocking(self):
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap)
        assert result["status"] == "WARN"
        assert any("visual_context missing" in warning for warning in result["warnings"])

    def test_missing_required_signal_field_fails_validation(self):
        bad = _load("signal_event_v0_minimal.json")
        bad["symbol"] = ""
        snap = _load("desk_snapshot_minimal.json")
        ok, errors = validate_desk_pro_dry_run_inputs(bad, desk_snapshot=snap)
        assert ok is False
        assert any("missing symbol" in error for error in errors)

    def test_no_runtime_side_effect_dependencies(self):
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap)
        assert result["no_systemd"] is True
        assert result["summary"]["desk_snapshot_present"] is True

    def test_missing_desk_snapshot_is_warn_non_blocking(self):
        v0 = _load("signal_event_v0_minimal.json")
        result = run_desk_pro_dry_run(v0)
        assert result["status"] == "WARN"
        assert any("desk_snapshot missing" in warning for warning in result["warnings"])

    def test_timer_payload_normalizes_to_warn_without_snapshot(self):
        timer_payload = {
            "engine": "DESK_PRO_TIMER",
            "signal": "BUY",
            "symbol": "BTCUSDT",
            "tf": "H1",
            "_ts": "2026-05-09T10:14:21+00:00",
        }
        result = run_desk_pro_dry_run(timer_payload)
        assert result["status"] == "WARN"
        assert result["signal_event"]["event_type"] == "signal_event"
        assert result["signal_event"]["source"] == "tradingview.webhook"
        assert result["signal_event"]["direction"] == "BUY"
        assert result["signal_event"]["engine"] == "DESK_PRO_TIMER"
        assert result["errors"] == []

    def test_timer_payload_validation_is_non_blocking_without_snapshot(self):
        timer_payload = {
            "engine": "DESK_PRO_TIMER",
            "signal": "BUY",
            "symbol": "BTCUSDT",
            "tf": "H1",
            "_ts": "2026-05-09T10:14:21+00:00",
        }
        ok, errors = validate_desk_pro_dry_run_inputs(timer_payload)
        assert ok is True
        assert errors == []

    def test_missing_market_metrics_is_warn_non_blocking(self):
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap, market_metrics=None)
        assert result["status"] == "WARN"
        assert any("market_metrics missing" in w for w in result["warnings"])

    def test_market_metrics_present_sets_summary_flag(self):
        from modules.desk_pro.service.market_metrics_reader import read_market_metrics
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        mm_fixture = _load("market_metrics_v1_minimal.json")
        import tempfile, json
        from pathlib import Path
        td = Path(tempfile.mkdtemp())
        try:
            mm_path = td / "market_metrics_latest.json"
            mm_path.write_text(json.dumps(mm_fixture), encoding="utf-8")
            metrics = read_market_metrics(path=mm_path)
            result = run_desk_pro_dry_run(v0, desk_snapshot=snap, market_metrics=metrics)
            assert result["summary"]["market_metrics_present"] is True
        finally:
            import shutil; shutil.rmtree(td)

    def test_market_metrics_present_removes_missing_warning(self):
        from modules.desk_pro.service.market_metrics_reader import read_market_metrics
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        mm_fixture = _load("market_metrics_v1_minimal.json")
        import tempfile, json, shutil
        from pathlib import Path
        td = Path(tempfile.mkdtemp())
        try:
            mm_path = td / "market_metrics_latest.json"
            mm_path.write_text(json.dumps(mm_fixture), encoding="utf-8")
            metrics = read_market_metrics(path=mm_path)
            result = run_desk_pro_dry_run(v0, desk_snapshot=snap, market_metrics=metrics)
            assert not any("market_metrics missing" in w for w in result["warnings"])
        finally:
            shutil.rmtree(td)

    def test_summary_market_metrics_present_false_when_absent(self):
        v0 = _load("signal_event_v0_minimal.json")
        result = run_desk_pro_dry_run(v0)
        assert result["summary"]["market_metrics_present"] is False

    def test_missing_vision_analysis_is_warn_non_blocking(self):
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap, vision_analysis=None)
        assert result["status"] == "WARN"
        assert any("vision_analysis missing" in w for w in result["warnings"])

    def test_vision_analysis_present_sets_summary_flag(self):
        from modules.desk_pro.service.vision_analysis_reader import read_vision_analysis
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        va_fixture = _load("vision_analysis_v1_minimal.json")
        import tempfile, shutil
        from pathlib import Path
        td = Path(tempfile.mkdtemp())
        try:
            va_path = td / "vision_analysis_latest.json"
            import json
            va_path.write_text(json.dumps(va_fixture), encoding="utf-8")
            va = read_vision_analysis(path=va_path)
            result = run_desk_pro_dry_run(v0, desk_snapshot=snap, vision_analysis=va)
            assert result["summary"]["vision_analysis_present"] is True
        finally:
            shutil.rmtree(td)

    def test_vision_analysis_present_removes_missing_warning(self):
        from modules.desk_pro.service.vision_analysis_reader import read_vision_analysis
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        va_fixture = _load("vision_analysis_v1_minimal.json")
        import tempfile, shutil, json
        from pathlib import Path
        td = Path(tempfile.mkdtemp())
        try:
            va_path = td / "vision_analysis_latest.json"
            va_path.write_text(json.dumps(va_fixture), encoding="utf-8")
            va = read_vision_analysis(path=va_path)
            result = run_desk_pro_dry_run(v0, desk_snapshot=snap, vision_analysis=va)
            assert not any("vision_analysis missing" in w for w in result["warnings"])
        finally:
            shutil.rmtree(td)

    def test_summary_vision_analysis_present_false_when_absent(self):
        v0 = _load("signal_event_v0_minimal.json")
        result = run_desk_pro_dry_run(v0)
        assert result["summary"]["vision_analysis_present"] is False

    def test_missing_telegram_claim_is_warn_non_blocking(self):
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap, telegram_claim=None)
        assert result["status"] == "WARN"
        assert any("telegram_claim missing" in w for w in result["warnings"])

    def test_telegram_claim_present_sets_summary_flag(self):
        from modules.desk_pro.service.telegram_claim_reader import read_telegram_claim
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        tc_fixture = _load("telegram_claim_v1_minimal.json")
        import tempfile, shutil, json
        from pathlib import Path
        td = Path(tempfile.mkdtemp())
        try:
            tc_path = td / "telegram_claim_latest.json"
            tc_path.write_text(json.dumps(tc_fixture), encoding="utf-8")
            tc = read_telegram_claim(path=tc_path)
            result = run_desk_pro_dry_run(v0, desk_snapshot=snap, telegram_claim=tc)
            assert result["summary"]["telegram_claim_present"] is True
        finally:
            shutil.rmtree(td)

    def test_telegram_claim_present_removes_missing_warning(self):
        from modules.desk_pro.service.telegram_claim_reader import read_telegram_claim
        v0 = _load("signal_event_v0_minimal.json")
        snap = _load("desk_snapshot_minimal.json")
        tc_fixture = _load("telegram_claim_v1_minimal.json")
        import tempfile, shutil, json
        from pathlib import Path
        td = Path(tempfile.mkdtemp())
        try:
            tc_path = td / "telegram_claim_latest.json"
            tc_path.write_text(json.dumps(tc_fixture), encoding="utf-8")
            tc = read_telegram_claim(path=tc_path)
            result = run_desk_pro_dry_run(v0, desk_snapshot=snap, telegram_claim=tc)
            assert not any("telegram_claim missing" in w for w in result["warnings"])
        finally:
            shutil.rmtree(td)

    def test_summary_telegram_claim_present_false_when_absent(self):
        v0 = _load("signal_event_v0_minimal.json")
        result = run_desk_pro_dry_run(v0)
        assert result["summary"]["telegram_claim_present"] is False
