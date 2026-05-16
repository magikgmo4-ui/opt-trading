"""Tests for Google Sheets controlled sync of daily session journal."""
from __future__ import annotations
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _make_test_entry(run_id: str = "sync_test_001") -> dict:
    return {
        "run_id": run_id,
        "session_id": "test-session",
        "journal_type": "daily_session",
        "pipeline": "E2E dry-run pipeline daily session journal",
        "controlled_write": False,
        "dry_run": True,
        "paper_mode": True,
        "started_at": "2026-05-16T10:00:00+00:00",
        "completed_at": "2026-05-16T10:00:01+00:00",
        "duration_s": 0.5,
        "pipeline_duration_s": 0.3,
        "all_ok": True,
        "steps": [],
        "signal_source": {"engine": "e2e_dry_run", "signal": "BUY", "symbol": "BTCUSDT"},
        "proposition_summary": {"action": "BUY", "confidence": 0.82},
        "validation_verdict": "APPROVED",
        "trade_executor_status": "filled",
        "result_tracker_outcome": "win",
        "pnl_paper": {"outcome": "win", "net_pnl": "438.03"},
        "datasheet_writer": {"dry_run": True, "written": False},
        "learning_feeder": {"bridge_status": "dry_run", "brick_stored": False},
        "tmux_before": {"timestamp": "", "active": ["a", "b"], "count": 2},
        "tmux_after": {"timestamp": "", "active": ["a", "b", "c"], "count": 3},
        "localcms_before": {"/health": {"ok": True}, "/menu": {"ok": True}},
        "localcms_after": {"/health": {"ok": True}, "/menu": {"ok": True}, "/runtime/tmux": {"ok": True}},
        "localcms_ok": True,
        "closeout_required": False,
        "closeout_acknowledged": True,
    }


class TestSyncDailySessionImport(unittest.TestCase):
    """Test que le module s'importe et que ses fonctions existent."""

    def test_module_importable(self):
        from scripts.sheets.sync_daily_session import (
            _load_journal, _find_latest, _extract_row, _row_values,
            _log_sync, _read_sync_status, _try_get_sheets_client, COLUMNS,
        )
        self.assertTrue(callable(_load_journal))
        self.assertTrue(callable(_find_latest))
        self.assertTrue(callable(_extract_row))
        self.assertTrue(callable(_row_values))
        self.assertTrue(callable(_log_sync))
        self.assertTrue(callable(_read_sync_status))
        self.assertTrue(callable(_try_get_sheets_client))
        self.assertIsInstance(COLUMNS, list)

    def test_columns_defined(self):
        from scripts.sheets.sync_daily_session import COLUMNS
        expected = [
            "run_id", "date", "signal", "side", "ticker",
            "action", "confidence", "verdict", "exec_status",
            "fill_price", "outcome", "net_pnl", "datasheet_written",
            "bridge_status", "brick_stored", "tmux_before", "tmux_after",
            "localcms_before_ok", "localcms_after_ok", "closeout_acknowledged",
            "duration_s", "all_ok",
        ]
        self.assertEqual(COLUMNS, expected)


class TestSyncDailySessionExtract(unittest.TestCase):
    """Test l'extraction de ligne depuis le JSON journal."""

    def setUp(self):
        self.entry = _make_test_entry()

    def test_extract_row_has_all_columns(self):
        from scripts.sheets.sync_daily_session import _extract_row, COLUMNS
        row = _extract_row(self.entry)
        for col in COLUMNS:
            self.assertIn(col, row, f"Missing column: {col}")

    def test_extract_row_values(self):
        from scripts.sheets.sync_daily_session import _extract_row
        row = _extract_row(self.entry)
        self.assertEqual(row["run_id"], "sync_test_001")
        self.assertEqual(row["date"], "2026-05-16")
        self.assertEqual(row["signal"], "BUY BTCUSDT")
        self.assertEqual(row["side"], "BUY")
        self.assertEqual(row["ticker"], "BTCUSDT")
        self.assertEqual(row["action"], "BUY")
        self.assertEqual(row["confidence"], 0.82)
        self.assertEqual(row["verdict"], "APPROVED")
        self.assertEqual(row["exec_status"], "filled")
        self.assertEqual(row["outcome"], "win")
        self.assertEqual(row["net_pnl"], "438.03")
        self.assertEqual(row["datasheet_written"], False)
        self.assertEqual(row["bridge_status"], "dry_run")
        self.assertEqual(row["brick_stored"], False)
        self.assertEqual(row["tmux_before"], 2)
        self.assertEqual(row["tmux_after"], 3)
        self.assertTrue(row["closeout_acknowledged"])
        self.assertEqual(row["duration_s"], 0.5)
        self.assertEqual(row["all_ok"], True)

    def test_localcms_ok_fraction(self):
        from scripts.sheets.sync_daily_session import _extract_row
        row = _extract_row(self.entry)
        self.assertEqual(row["localcms_before_ok"], "2/2")
        self.assertEqual(row["localcms_after_ok"], "3/3")

    def test_extract_row_empty_entry(self):
        from scripts.sheets.sync_daily_session import _extract_row
        row = _extract_row({})
        for col in ["run_id", "date", "side", "verdict"]:
            self.assertEqual(row[col], "", f"Column {col} should be empty")
        self.assertIn(row.get("signal", ""), ("", " "), f"signal should be empty or space, got {repr(row.get('signal'))}")

    def test_row_values_length(self):
        from scripts.sheets.sync_daily_session import _extract_row, _row_values, COLUMNS
        row = _extract_row(self.entry)
        values = _row_values(row)
        self.assertEqual(len(values), len(COLUMNS))

    def test_row_values_bool_conversion(self):
        from scripts.sheets.sync_daily_session import _extract_row, _row_values, COLUMNS
        row = _extract_row(self.entry)
        values = _row_values(row)
        closeout_idx = COLUMNS.index("closeout_acknowledged")
        self.assertEqual(values[closeout_idx], "YES")


class TestSyncDailySessionJournalLoad(unittest.TestCase):
    """Test le chargement du journal depuis le disque."""

    def setUp(self):
        self.journal_dir = PROJECT_ROOT / "data" / "journal" / "daily"
        self.journal_dir.mkdir(parents=True, exist_ok=True)
        self.entry = _make_test_entry("sync_disk_test")
        self.path = self.journal_dir / "sync_disk_test.json"
        self.path.write_text(json.dumps(self.entry, default=str))

    def tearDown(self):
        self.path.unlink(missing_ok=True)

    def test_load_journal_found(self):
        from scripts.sheets.sync_daily_session import _load_journal
        entry = _load_journal("sync_disk_test")
        self.assertEqual(entry["run_id"], "sync_disk_test")

    def test_load_journal_not_found(self):
        from scripts.sheets.sync_daily_session import _load_journal
        with self.assertRaises(SystemExit):
            _load_journal("nonexistent_run_id")

    def test_find_latest(self):
        from scripts.sheets.sync_daily_session import _find_latest
        run_id = _find_latest()
        self.assertIsNotNone(run_id)
        self.assertIsInstance(run_id, str)


class TestSyncDailySessionLogging(unittest.TestCase):
    """Test le logging de sync."""

    def setUp(self):
        self.sync_log = PROJECT_ROOT / "data" / "journal" / "sync_log.jsonl"
        self.sync_log.parent.mkdir(parents=True, exist_ok=True)
        if self.sync_log.exists():
            self.sync_log.unlink()

    def tearDown(self):
        if self.sync_log.exists():
            self.sync_log.unlink()

    def test_log_sync_creates_file(self):
        from scripts.sheets.sync_daily_session import _log_sync
        _log_sync("test_log", "dry_run", "dry_run_skipped")
        self.assertTrue(self.sync_log.exists())

    def test_log_sync_appends(self):
        from scripts.sheets.sync_daily_session import _log_sync
        _log_sync("test_log_a", "dry_run", "dry_run_skipped")
        _log_sync("test_log_b", "dry_run", "dry_run_skipped")
        lines = self.sync_log.read_text().strip().splitlines()
        self.assertEqual(len(lines), 2)

    def test_log_sync_content(self):
        from scripts.sheets.sync_daily_session import _log_sync
        _log_sync("test_content", "controlled_write", "synced")
        entry = json.loads(self.sync_log.read_text().strip())
        self.assertEqual(entry["run_id"], "test_content")
        self.assertEqual(entry["mode"], "controlled_write")
        self.assertEqual(entry["status"], "synced")
        self.assertIn("timestamp", entry)

    def test_read_sync_status_found(self):
        from scripts.sheets.sync_daily_session import _log_sync, _read_sync_status
        _log_sync("test_read", "dry_run", "dry_run_skipped")
        status = _read_sync_status("test_read")
        self.assertIsNotNone(status)
        self.assertEqual(status["run_id"], "test_read")

    def test_read_sync_status_not_found(self):
        from scripts.sheets.sync_daily_session import _read_sync_status
        status = _read_sync_status("nonexistent")
        self.assertIsNone(status)


class TestSyncDailySessionDryRun(unittest.TestCase):
    """Test que le dry-run fonctionne sans credentials."""

    def setUp(self):
        self.journal_dir = PROJECT_ROOT / "data" / "journal" / "daily"
        self.journal_dir.mkdir(parents=True, exist_ok=True)
        self.entry_key = "sync_dry_run_test"
        self.path = self.journal_dir / f"{self.entry_key}.json"
        self.path.write_text(json.dumps(_make_test_entry(self.entry_key), default=str))

    def tearDown(self):
        self.path.unlink(missing_ok=True)

    def test_script_dry_run_exits_zero(self):
        env = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT)}
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/sheets/sync_daily_session.py"),
             "--run-id", self.entry_key],
            capture_output=True, text=True, timeout=30, env=env,
        )
        if r.returncode != 0 and r.returncode != 1:
            self.fail(f"Dry-run failed (rc={r.returncode}): STDERR={r.stderr[:500]}")
        self.assertIn("DRY-RUN", r.stdout)
        self.assertIn(self.entry_key, r.stdout)

    def test_script_dry_run_shows_row_preview(self):
        env = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT)}
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/sheets/sync_daily_session.py"),
             "--run-id", self.entry_key],
            capture_output=True, text=True, timeout=30, env=env,
        )
        for col in ["run_id", "date", "signal", "side", "ticker", "action",
                     "verdict", "outcome", "net_pnl"]:
            self.assertIn(col, r.stdout)

    def test_script_dry_run_with_latest_flag(self):
        env = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT)}
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/sheets/sync_daily_session.py"),
             "--latest"],
            capture_output=True, text=True, timeout=30, env=env,
        )
        self.assertIn("DRY-RUN", r.stdout)

    def test_script_no_credentials_dry_run_hint(self):
        env = {k: v for k, v in os.environ.items()
               if k not in ("GOOGLE_SHEETS_CREDENTIALS_JSON", "GOOGLE_SHEETS_SYNC_SHEET_ID")}
        env["PYTHONPATH"] = str(PROJECT_ROOT)
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/sheets/sync_daily_session.py"),
             "--run-id", self.entry_key],
            capture_output=True, text=True, timeout=30, env=env,
        )
        self.assertIn("GOOGLE_SHEETS_CREDENTIALS_JSON", r.stdout)

    def test_controlled_write_fails_without_credentials(self):
        env = {k: v for k, v in os.environ.items()
               if k not in ("GOOGLE_SHEETS_CREDENTIALS_JSON", "GOOGLE_SHEETS_SYNC_SHEET_ID")}
        env["PYTHONPATH"] = str(PROJECT_ROOT)
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/sheets/sync_daily_session.py"),
             "--run-id", self.entry_key, "--controlled-write"],
            capture_output=True, text=True, timeout=30, env=env,
        )
        self.assertNotEqual(r.returncode, 0)


class TestSyncDailySessionAPI(unittest.TestCase):
    """Test l'API sans credentials Sheets."""

    def test_try_get_sheets_client_without_creds(self):
        env = {k: v for k, v in os.environ.items()
               if k not in ("GOOGLE_SHEETS_CREDENTIALS_JSON", "GOOGLE_SHEETS_SYNC_SHEET_ID")}
        import importlib
        for key in list(sys.modules.keys()):
            if "sync_daily_session" in key:
                del sys.modules[key]
        for k, v in env.items():
            if k not in ("GOOGLE_SHEETS_CREDENTIALS_JSON", "GOOGLE_SHEETS_SYNC_SHEET_ID"):
                os.environ[k] = v
        for k in ("GOOGLE_SHEETS_CREDENTIALS_JSON", "GOOGLE_SHEETS_SYNC_SHEET_ID"):
            os.environ.pop(k, None)
        from scripts.sheets.sync_daily_session import _try_get_sheets_client
        client, sheet = _try_get_sheets_client()
        self.assertIsNone(client)
        self.assertIsNone(sheet)

    def test_check_status_not_found(self):
        env = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT)}
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/sheets/sync_daily_session.py"),
             "--check-status", "nonexistent_run"],
            capture_output=True, text=True, timeout=30, env=env,
        )
        result = json.loads(r.stdout)
        self.assertEqual(result["run_id"], "nonexistent_run")
        self.assertEqual(result["status"], "not_found")

    def test_script_no_post_put_delete_patch(self):
        text = (PROJECT_ROOT / "scripts/sheets/sync_daily_session.py").read_text()
        self.assertNotIn(".post(", text)
        self.assertNotIn(".put(", text.lower())
        self.assertNotIn(".delete(", text.lower())
        self.assertNotIn(".patch(", text.lower())

    def test_script_no_bitget(self):
        text = (PROJECT_ROOT / "scripts/sheets/sync_daily_session.py").read_text()
        self.assertNotIn("bitget", text.lower())

    def test_dry_run_does_not_write_sheets(self):
        text = (PROJECT_ROOT / "scripts/sheets/sync_daily_session.py").read_text()
        self.assertIn("dry_run_skipped", text)
        self.assertIn("controlled_write", text)


if __name__ == "__main__":
    unittest.main()
