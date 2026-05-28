"""Tests for aw_signal_processor, aw_signal_stats, gha_strict_workers_schedule.

Covers:
- signal_processor: validate, cross_check, dry_run_guard, process_signal
- signal_stats: compute_stats, load_journal
- strict-workers-schedule.yml: YAML structure, packet reference, permissions
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKERS_DIR = REPO_ROOT / "scripts" / "ai" / "workers"
if str(WORKERS_DIR) not in sys.path:
    sys.path.insert(0, str(WORKERS_DIR))

import signal_processor  # noqa: E402
import signal_stats  # noqa: E402


# ---------------------------------------------------------------------------
# signal_processor — validate
# ---------------------------------------------------------------------------

class TestValidate(unittest.TestCase):
    def _signal(self, **overrides):
        s = signal_processor.make_signal(
            source="tv", signal_type="entry", symbol="BTCUSD",
            direction="buy", confidence=0.80, price=10000.0
        )
        for k, v in overrides.items():
            if k in s["payload"]:
                s["payload"][k] = v
            elif k == "signal_type":
                s["signal_type"] = v
        return s

    def test_valid(self):
        ok, reason = signal_processor.validate(self._signal())
        self.assertTrue(ok)
        self.assertEqual(reason, "valid")

    def test_low_confidence(self):
        ok, reason = signal_processor.validate(self._signal(confidence=0.59))
        self.assertFalse(ok)
        self.assertEqual(reason, "confidence_below_threshold")

    def test_confidence_at_threshold(self):
        ok, _ = signal_processor.validate(self._signal(confidence=0.6))
        self.assertTrue(ok)

    def test_unknown_signal_type(self):
        s = self._signal()
        s["signal_type"] = "unknown_type"
        ok, reason = signal_processor.validate(s)
        self.assertFalse(ok)
        self.assertEqual(reason, "unknown_signal_type")

    def test_missing_direction(self):
        ok, reason = signal_processor.validate(self._signal(direction=""))
        self.assertFalse(ok)
        self.assertEqual(reason, "missing_direction")

    def test_invalid_price(self):
        ok, reason = signal_processor.validate(self._signal(price=-1.0))
        self.assertFalse(ok)
        self.assertEqual(reason, "invalid_price")

    def test_zero_price_invalid(self):
        ok, reason = signal_processor.validate(self._signal(price=0.0))
        self.assertFalse(ok)
        self.assertEqual(reason, "invalid_price")

    def test_none_price_ok(self):
        ok, _ = signal_processor.validate(self._signal(price=None))
        self.assertTrue(ok)

    def test_all_valid_signal_types(self):
        for st in ("entry", "exit", "alert", "heartbeat", "anomaly"):
            s = self._signal()
            s["signal_type"] = st
            ok, _ = signal_processor.validate(s)
            self.assertTrue(ok, f"signal_type={st} should be valid")


# ---------------------------------------------------------------------------
# signal_processor — cross_check
# ---------------------------------------------------------------------------

class TestCrossCheck(unittest.TestCase):
    def _signal(self):
        return signal_processor.make_signal(
            source="tv", signal_type="entry", symbol="BTCUSD",
            direction="buy", confidence=0.80
        )

    def test_confirmed_two_sources(self):
        s = signal_processor.cross_check(self._signal(), ["tv", "telegram"])
        self.assertEqual(s["cross_validation"]["status"], "confirmed")

    def test_confirmed_three_sources(self):
        s = signal_processor.cross_check(self._signal(), ["tv", "tg", "collector"])
        self.assertEqual(s["cross_validation"]["status"], "confirmed")

    def test_pending_one_source(self):
        s = signal_processor.cross_check(self._signal(), ["tv"])
        self.assertEqual(s["cross_validation"]["status"], "pending")

    def test_conflicting_zero_sources(self):
        s = signal_processor.cross_check(self._signal(), [])
        self.assertEqual(s["cross_validation"]["status"], "conflicting")

    def test_matched_sources_recorded(self):
        sources = ["tv", "telegram"]
        s = signal_processor.cross_check(self._signal(), sources)
        self.assertEqual(s["cross_validation"]["matched_sources"], sources)


# ---------------------------------------------------------------------------
# signal_processor — dry_run_guard
# ---------------------------------------------------------------------------

class TestDryRunGuard(unittest.TestCase):
    def _confirmed_signal(self):
        s = signal_processor.make_signal(
            source="tv", signal_type="entry", symbol="BTCUSD",
            direction="buy", confidence=0.80, price=10000.0
        )
        s["cross_validation"]["status"] = "confirmed"
        return s

    def _pending_signal(self):
        s = signal_processor.make_signal(
            source="tv", signal_type="entry", symbol="BTCUSD",
            direction="buy", confidence=0.80
        )
        s["cross_validation"]["status"] = "pending"
        return s

    def test_confirmed_generates_blocked_order(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(signal_processor, "DRY_RUN_ORDERS_DIR", Path(tmpdir)):
                s, generated = signal_processor.dry_run_guard(self._confirmed_signal())
        self.assertTrue(generated)
        self.assertTrue(s["dry_run"]["order_generated"])
        self.assertTrue(s["dry_run"]["order_blocked"])
        self.assertIsNotNone(s["dry_run"]["order_json"])
        self.assertEqual(s["dry_run"]["order_json"]["status"], "BLOCKED_BY_DRY_RUN_GUARD")

    def test_confirmed_writes_order_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(signal_processor, "DRY_RUN_ORDERS_DIR", Path(tmpdir)):
                signal_processor.dry_run_guard(self._confirmed_signal())
            files = list(Path(tmpdir).glob("order_*.json"))
            self.assertEqual(len(files), 1)
            order = json.loads(files[0].read_text())
            self.assertEqual(order["status"], "BLOCKED_BY_DRY_RUN_GUARD")

    def test_not_confirmed_no_order(self):
        s, generated = signal_processor.dry_run_guard(self._pending_signal())
        self.assertFalse(generated)
        self.assertFalse(s["dry_run"]["order_generated"])
        self.assertFalse(s["dry_run"]["order_blocked"])

    def test_conflicting_no_order(self):
        s = self._pending_signal()
        s["cross_validation"]["status"] = "conflicting"
        _, generated = signal_processor.dry_run_guard(s)
        self.assertFalse(generated)


# ---------------------------------------------------------------------------
# signal_stats — compute_stats
# ---------------------------------------------------------------------------

def _make_event(source="tv", symbol="BTCUSD", cv_status="confirmed",
                journal_status="logged", order_blocked=True, processing_ms=100):
    return {
        "source": source,
        "payload": {"symbol": symbol},
        "cross_validation": {"status": cv_status},
        "journal": {"status": journal_status, "processing_time_ms": processing_ms},
        "dry_run": {"order_blocked": order_blocked},
    }


class TestComputeStats(unittest.TestCase):
    def test_empty(self):
        stats = signal_stats.compute_stats([])
        self.assertEqual(stats["total_signals"], 0)
        self.assertIn("note", stats)

    def test_single_confirmed(self):
        events = [_make_event()]
        stats = signal_stats.compute_stats(events)
        self.assertEqual(stats["total_signals"], 1)
        self.assertEqual(stats["confirmed"], 1)
        self.assertEqual(stats["confirmation_rate"], 100.0)
        self.assertEqual(stats["orders_blocked"], 1)

    def test_mixed_signals(self):
        events = [
            _make_event(cv_status="confirmed", order_blocked=True),
            _make_event(cv_status="pending", order_blocked=False),
            _make_event(cv_status="conflicting", order_blocked=False),
        ]
        stats = signal_stats.compute_stats(events)
        self.assertEqual(stats["total_signals"], 3)
        self.assertEqual(stats["confirmed"], 1)
        self.assertEqual(stats["pending"], 1)
        self.assertEqual(stats["orders_blocked"], 1)

    def test_top_sources(self):
        events = [
            _make_event(source="tv"),
            _make_event(source="tv"),
            _make_event(source="telegram"),
        ]
        stats = signal_stats.compute_stats(events)
        self.assertEqual(stats["top_sources"][0][0], "tv")
        self.assertEqual(stats["top_sources"][0][1], 2)

    def test_avg_processing_ms(self):
        events = [
            _make_event(processing_ms=100),
            _make_event(processing_ms=200),
        ]
        stats = signal_stats.compute_stats(events)
        self.assertEqual(stats["avg_processing_ms"], 150)


# ---------------------------------------------------------------------------
# signal_stats — load_journal
# ---------------------------------------------------------------------------

class TestLoadJournal(unittest.TestCase):
    def test_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            events = signal_stats.load_journal(Path(tmpdir))
        self.assertEqual(events, [])

    def test_reads_jsonl_file(self):
        e1 = _make_event(source="tv")
        e2 = _make_event(source="telegram")
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "2026-05-28.jsonl"
            p.write_text(json.dumps(e1) + "\n" + json.dumps(e2) + "\n")
            events = signal_stats.load_journal(Path(tmpdir))
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["source"], "tv")
        self.assertEqual(events[1]["source"], "telegram")

    def test_skips_empty_lines(self):
        e = _make_event()
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "2026-05-28.jsonl"
            p.write_text(json.dumps(e) + "\n\n")
            events = signal_stats.load_journal(Path(tmpdir))
        self.assertEqual(len(events), 1)

    def test_reads_multiple_files_sorted(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "2026-05-27.jsonl").write_text(json.dumps(_make_event(source="a")) + "\n")
            (Path(tmpdir) / "2026-05-28.jsonl").write_text(json.dumps(_make_event(source="b")) + "\n")
            events = signal_stats.load_journal(Path(tmpdir))
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["source"], "a")
        self.assertEqual(events[1]["source"], "b")


# ---------------------------------------------------------------------------
# gha_strict_workers_schedule.yml — structure validation
# ---------------------------------------------------------------------------

class TestScheduleWorkflow(unittest.TestCase):
    WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "strict-workers-schedule.yml"

    def _load(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        return yaml.safe_load(self.WORKFLOW_PATH.read_text())

    def _triggers(self, wf):
        # PyYAML parses YAML 1.1 `on:` as boolean True in some versions
        return wf.get("on") or wf.get(True) or {}

    def test_file_exists(self):
        self.assertTrue(self.WORKFLOW_PATH.exists())

    def test_valid_yaml(self):
        wf = self._load()
        self.assertIsInstance(wf, dict)

    def test_has_schedule_trigger(self):
        triggers = self._triggers(self._load())
        self.assertIn("schedule", triggers)
        crons = [item["cron"] for item in triggers["schedule"]]
        self.assertTrue(any(crons), "no cron entries")

    def test_has_workflow_dispatch(self):
        triggers = self._triggers(self._load())
        self.assertIn("workflow_dispatch", triggers)

    def test_permissions_read_only(self):
        wf = self._load()
        self.assertEqual(wf.get("permissions", {}).get("contents"), "read")

    def test_references_readonly_smoke_packet(self):
        content = self.WORKFLOW_PATH.read_text()
        self.assertIn("GO_STRICT_WORKERS_READONLY_SMOKE_01.json", content)

    def test_referenced_packet_exists_and_is_candidate(self):
        packet_path = REPO_ROOT / "scripts" / "ai" / "workers" / "job_packets" / "GO_STRICT_WORKERS_READONLY_SMOKE_01.json"
        self.assertTrue(packet_path.exists())
        packet = json.loads(packet_path.read_text())
        self.assertEqual(packet["status"], "candidate")


if __name__ == "__main__":
    unittest.main()
