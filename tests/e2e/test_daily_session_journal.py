"""Daily Session Journal tests — prouve le journal quotidien traçable."""
from __future__ import annotations
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestDailySessionJournalImport(unittest.TestCase):
    """Test que le module s'importe et que ses fonctions existent."""

    def test_module_importable(self):
        from scripts.e2e.daily_session_journal import (
            _resolve_run_id, _tmux_snapshot, _localcms_snapshot,
            _run_pipeline, _extract_metrics, _build_human_summary,
            _save_json, _save_csv, main,
        )
        self.assertTrue(callable(_resolve_run_id))
        self.assertTrue(callable(_tmux_snapshot))
        self.assertTrue(callable(_localcms_snapshot))
        self.assertTrue(callable(_run_pipeline))
        self.assertTrue(callable(_extract_metrics))
        self.assertTrue(callable(_build_human_summary))
        self.assertTrue(callable(_save_json))
        self.assertTrue(callable(_save_csv))
        self.assertTrue(callable(main))

    def test_resolve_run_id_format(self):
        from scripts.e2e.daily_session_journal import _resolve_run_id
        run_id = _resolve_run_id()
        parts = run_id.split("_")
        self.assertEqual(len(parts), 2)
        self.assertEqual(len(parts[0]), 8)
        self.assertTrue(parts[0].isdigit())
        self.assertTrue(parts[1].isdigit())

    def test_tmux_snapshot_structure(self):
        from scripts.e2e.daily_session_journal import _tmux_snapshot
        snap = _tmux_snapshot()
        self.assertIn("active", snap)
        self.assertIsInstance(snap.get("active"), list)
        if "error" not in snap:
            self.assertIn("timestamp", snap)
            self.assertIsInstance(snap.get("count"), int)
        else:
            self.assertEqual(snap.get("active"), [])

    def test_localcms_snapshot_unreachable(self):
        from scripts.e2e.daily_session_journal import _localcms_snapshot
        snap = _localcms_snapshot()
        for ep in ["/health", "/menu", "/menu/state", "/runtime/tmux"]:
            self.assertIn(ep, snap)
            self.assertIn("status", snap[ep])
            self.assertIn("ok", snap[ep])

    def test_extract_metrics_from_empty_report(self):
        from scripts.e2e.daily_session_journal import _extract_metrics
        report = {"steps": []}
        metrics = _extract_metrics(report)
        self.assertIn("signal_side", metrics)
        self.assertIn("validation_verdict", metrics)
        self.assertIn("tracker_outcome", metrics)
        self.assertEqual(metrics.get("signal_side"), "N/A")

    def test_build_human_summary(self):
        from scripts.e2e.daily_session_journal import _extract_metrics, _build_human_summary
        report = {
            "run_id": "20260516_001",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "duration_s": 1.5,
            "all_ok": True,
            "steps": [],
            "tmux_before": {"count": 5},
            "tmux_after": {"count": 5},
            "localcms": {"/health": {"ok": True}},
            "localcms_ok": True,
            "closeout_acknowledged": True,
        }
        metrics = _extract_metrics(report)
        summary = _build_human_summary(metrics, report)
        self.assertIn("DAILY SESSION JOURNAL", summary)
        self.assertIn("20260516_001", summary)
        self.assertIn("CLOSEOUT ACKNOWLEDGED", summary)

    def test_save_json_and_read_back(self):
        from scripts.e2e.daily_session_journal import _save_json
        tmp_dir = PROJECT_ROOT / "tmp" / "test_journal"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        path = tmp_dir / "test_001.json"
        data = {"run_id": "test_001", "all_ok": True}
        _save_json(data, path)
        self.assertTrue(path.exists())
        loaded = json.loads(path.read_text())
        self.assertEqual(loaded["run_id"], "test_001")
        self.assertTrue(loaded["all_ok"])
        path.unlink(missing_ok=True)
        tmp_dir.rmdir()

    def test_save_csv_and_read_back(self):
        from scripts.e2e.daily_session_journal import _save_csv, _extract_metrics
        tmp_dir = PROJECT_ROOT / "tmp" / "test_journal"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        report = {
            "run_id": "test_csv_001",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "duration_s": 2.0,
            "all_ok": True,
            "steps": [],
            "tmux_before": {"count": 5},
            "tmux_after": {"count": 5},
            "localcms_ok": True,
            "closeout_acknowledged": True,
            "localcms": {},
        }
        metrics = _extract_metrics(report)
        path = tmp_dir / "test_csv_001.csv"
        _save_csv(metrics, report, path)
        self.assertTrue(path.exists())
        with open(path) as f:
            import csv
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["run_id"], "test_csv_001")
        path.unlink(missing_ok=True)
        tmp_dir.rmdir()


class TestDailySessionJournalPipeline(unittest.TestCase):
    """Test que le pipeline journalier s'exécute en dry-run."""

    def test_journal_script_runs_dry(self):
        env = {**os.environ, "DRY_RUN": "1", "PAPER_MODE": "1",
               "PYTHONPATH": str(PROJECT_ROOT)}
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/e2e/daily_session_journal.py"),
             "--no-closeout"],
            capture_output=True, text=True, timeout=60, env=env,
        )
        if r.returncode != 0 and r.returncode != 1:
            self.fail(f"Journal failed (rc={r.returncode}): STDERR={r.stderr[:500]}")
        self.assertIn("DAILY SESSION JOURNAL", r.stdout)

    def test_journal_all_sections_present(self):
        env = {**os.environ, "DRY_RUN": "1", "PAPER_MODE": "1",
               "PYTHONPATH": str(PROJECT_ROOT)}
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/e2e/daily_session_journal.py"),
             "--no-closeout"],
            capture_output=True, text=True, timeout=60, env=env,
        )
        stdout = r.stdout
        self.assertIn("Signal", stdout)
        self.assertIn("Proposition", stdout)
        self.assertIn("Validation", stdout)
        self.assertIn("Execution", stdout)
        self.assertIn("Result", stdout)
        self.assertIn("Datasheet", stdout)
        self.assertIn("Learning", stdout)
        self.assertIn("Telegram", stdout)
        self.assertIn("signal_received", stdout)
        self.assertIn("TMUX", stdout)
        self.assertIn("LocalCMS", stdout)

    def test_journal_json_file_created(self):
        journal_dir = PROJECT_ROOT / "data" / "journal" / "daily"
        before = sorted(journal_dir.glob("*.json"))
        env = {**os.environ, "DRY_RUN": "1", "PAPER_MODE": "1",
               "PYTHONPATH": str(PROJECT_ROOT)}
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/e2e/daily_session_journal.py"),
             "--no-closeout"],
            capture_output=True, text=True, timeout=60, env=env,
        )
        after = sorted(journal_dir.glob("*.json"))
        self.assertGreater(len(after), 0)
        self.assertTrue(any(f.stem.startswith(datetime.now(timezone.utc).strftime("%Y%m%d"))
                            for f in after))

    def test_journal_csv_file_created(self):
        journal_dir = PROJECT_ROOT / "data" / "journal" / "daily"
        before = sorted(journal_dir.glob("*.csv"))
        env = {**os.environ, "DRY_RUN": "1", "PAPER_MODE": "1",
               "PYTHONPATH": str(PROJECT_ROOT)}
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/e2e/daily_session_journal.py"),
             "--no-closeout"],
            capture_output=True, text=True, timeout=60, env=env,
        )
        after = sorted(journal_dir.glob("*.csv"))
        self.assertGreater(len(after), 0)
        self.assertTrue(any(f.stem.startswith(datetime.now(timezone.utc).strftime("%Y%m%d"))
                            for f in after))

    def test_journal_no_post_put_delete_patch(self):
        text = (PROJECT_ROOT / "scripts" / "e2e" / "daily_session_journal.py").read_text()
        self.assertNotIn(".post(", text)
        self.assertNotIn(".put(", text.lower())
        self.assertNotIn(".delete(", text.lower())
        self.assertNotIn(".patch(", text.lower())

    def test_journal_dry_run_by_default(self):
        env = {k: v for k, v in os.environ.items()
               if k not in ("DRY_RUN", "PAPER_MODE")}
        env["PYTHONPATH"] = str(PROJECT_ROOT)
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/e2e/daily_session_journal.py"),
             "--no-closeout"],
            capture_output=True, text=True, timeout=60, env=env,
        )
        stdout = r.stdout
        lines = stdout.splitlines()
        dry_run_lines = [l for l in lines if "dry" in l.lower()]
        self.assertGreater(len(dry_run_lines), 0)

    def test_journal_7_worker_steps_present_in_output(self):
        env = {**os.environ, "DRY_RUN": "1", "PAPER_MODE": "1",
               "PYTHONPATH": str(PROJECT_ROOT)}
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/e2e/daily_session_journal.py"),
             "--no-closeout"],
            capture_output=True, text=True, timeout=60, env=env,
        )
        self.assertIn("signal_router", r.stderr)
        self.assertIn("proposition_engine", r.stderr)
        self.assertIn("validation_gate", r.stderr)
        self.assertIn("trade_executor", r.stderr)
        self.assertIn("result_tracker", r.stderr)
        self.assertIn("datasheet_writer", r.stderr)
        self.assertIn("learning_feeder", r.stderr)
        self.assertIn("notification_dispatcher", r.stderr)

    def test_journal_with_sheets_sync_prints_section(self):
        env = {**os.environ, "DRY_RUN": "1", "PAPER_MODE": "1",
               "PYTHONPATH": str(PROJECT_ROOT)}
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/e2e/daily_session_journal.py"),
             "--no-closeout", "--sync-sheets"],
            capture_output=True, text=True, timeout=90, env=env,
        )
        if r.returncode != 0 and r.returncode != 1:
            self.fail(f"Journal failed (rc={r.returncode}): STDERR={r.stderr[:500]}")
        self.assertIn("Sheets", r.stdout)


class TestLocalCMSJournalEndpoint(unittest.TestCase):
    """Test que l'endpoint /journal/daily existe dans LocalCMS."""

    def test_journal_endpoint_registered(self):
        from modules.localcms.app.main import app
        routes = [r.path for r in app.routes]
        self.assertIn("/journal/daily", routes)
        self.assertIn("/journal/daily/{run_id}", routes)

    def test_journal_response_structure(self):
        from modules.localcms.app.main import _list_journal_entries
        entries = _list_journal_entries()
        self.assertIsInstance(entries, list)
        for entry in entries:
            self.assertIn("run_id", entry)
            self.assertIn("started_at", entry)
            self.assertIn("all_ok", entry)


if __name__ == "__main__":
    unittest.main()
