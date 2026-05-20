from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestTelegramLatencyBacktest(unittest.TestCase):
    def test_latency_backtest_summarizes_by_source(self):
        with tempfile.TemporaryDirectory() as d:
            log_path = Path(d) / "telegram_send.jsonl"

            base_ts = datetime(2026, 5, 19, 12, 0, 0, tzinfo=timezone.utc).isoformat()
            records = [
                {"timestamp": base_ts, "source": "a", "ok": True, "duration_ms": 100, "tags": {"strategy_id": "S1"}},
                {"timestamp": base_ts, "source": "a", "ok": True, "duration_ms": 300, "tags": {"strategy_id": "S1"}},
                {"timestamp": base_ts, "source": "b", "ok": False, "duration_ms": 500, "tags": {"strategy_id": "S2"}},
                {"timestamp": base_ts, "source": "b", "ok": True, "duration_ms": 700, "tags": {"strategy_id": "S2"}},
            ]
            with open(log_path, "w", encoding="utf-8") as f:
                for rec in records:
                    f.write(json.dumps(rec) + "\n")

            env = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT), "TELEGRAM_LATENCY_LOG_PATH": str(log_path)}
            r = subprocess.run(
                [sys.executable, str(PROJECT_ROOT / "scripts/telegram/latency_backtest.py")],
                capture_output=True,
                text=True,
                timeout=30,
                env=env,
            )
            self.assertEqual(r.returncode, 0, msg=r.stderr)
            out = json.loads(r.stdout)
            summary = out["summary"]
            self.assertEqual(summary["count"], 4)
            self.assertEqual(summary["ok_count"], 3)
            self.assertIn("a", summary["by_source"])
            self.assertIn("b", summary["by_source"])
            self.assertEqual(summary["by_source"]["a"]["latency_ms"]["p50_ms"], 200)
            self.assertIn("by_strategy_id", summary)
            self.assertEqual(summary["by_strategy_id"]["S1"]["latency_ms"]["p50_ms"], 200)
