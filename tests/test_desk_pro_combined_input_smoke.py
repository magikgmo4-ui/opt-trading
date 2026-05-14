import json
from pathlib import Path

from modules.desk_pro.dry_run import (
    run_desk_pro_dry_run,
    write_desk_pro_dry_run_artifacts,
)
from modules.desk_pro.signal_event_adapter import normalize_signal_event_v1


FIXTURES = Path(__file__).parent / "fixtures" / "admin_trading_contract_smoke"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class TestDeskProCombinedInputSmoke:
    def _combined(self):
        se = _load("signal_event_v0_complete.json")
        vc = _load("visual_context_v1_minimal.json")
        snap = {"symbol": "BTCUSDT.P", "tf": "H1", "snapshot_ts": "now", "path": "/tmp/test.png"}
        return run_desk_pro_dry_run(se, visual_context=vc, desk_snapshot=snap)

    def test_no_input_missing_warnings(self):
        result = self._combined()
        assert "missing" not in str(result["warnings"])

    def test_errors_empty(self):
        result = self._combined()
        assert result["errors"] == []

    def test_safety_flags_true(self):
        result = self._combined()
        assert result["no_trade"] is True
        assert result["no_telegram"] is True
        assert result["no_webhook"] is True
        assert result["no_systemd"] is True

    def test_three_inputs_present(self):
        result = self._combined()
        assert result["summary"]["signal_event_present"] is True
        assert result["summary"]["visual_context_present"] is True
        assert result["summary"]["desk_snapshot_present"] is True

    def test_artifact_contains_three_refs(self, tmp_path):
        result = self._combined()
        meta = write_desk_pro_dry_run_artifacts(result, tmp_path)
        latest = json.loads(Path(meta["written_files"]["latest_json"]).read_text(encoding="utf-8"))
        assert latest["summary"]["signal_event_present"] is True
        assert latest["summary"]["visual_context_present"] is True
        assert latest["summary"]["desk_snapshot_present"] is True

    def test_history_appends(self, tmp_path):
        result = self._combined()
        write_desk_pro_dry_run_artifacts(result, tmp_path)
        write_desk_pro_dry_run_artifacts(result, tmp_path)
        history = Path(tmp_path / "history.jsonl")
        lines = [l for l in history.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(lines) == 2

    def test_v0_signal_normalized_in_combined(self):
        result = self._combined()
        assert result["signal_event"]["event_type"] == "signal_event"
        assert result["signal_event"]["direction"] == "BUY"

    def test_output_dir_isolated(self, tmp_path):
        result = self._combined()
        write_desk_pro_dry_run_artifacts(result, tmp_path)
        created = list(tmp_path.iterdir())
        assert len(created) == 3
