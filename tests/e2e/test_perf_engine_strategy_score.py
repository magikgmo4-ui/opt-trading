from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestPerfEngineStrategyScore(unittest.TestCase):
    def test_strategy_score_computes_metrics_and_gate(self):
        base_ts = datetime(2026, 5, 19, 12, 0, 0, tzinfo=timezone.utc).isoformat()
        events = [
            {
                "strategy": {"strategy_id": "S1", "strategy_version": "0.1.0"},
                "produced_at": base_ts,
                "verdict": "PASS",
                "outcome": "win",
                "pnl_net": 10.0,
                "run_id": "20260519_001",
            },
            {
                "strategy_id": "S1",
                "strategy_version": "0.1.0",
                "timestamp": base_ts,
                "verdict": "APPROVED",
                "outcome": "loss",
                "pnl_paper": {"net_pnl": -5.0},
                "run_id": "20260519_001",
            },
            {
                "strategy_id": "S1",
                "strategy_version": "0.1.0",
                "timestamp": base_ts,
                "verdict": "FAIL",
                "run_id": "20260519_001",
            },
        ]

        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "events.jsonl"
            with open(path, "w", encoding="utf-8") as f:
                for e in events:
                    f.write(json.dumps(e) + "\n")

            env = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT)}
            r = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "modules.perf_engine.app.perf_engine",
                    "strategy-score",
                    "--input",
                    str(path),
                    "--strategy-id",
                    "S1",
                    "--strategy-version",
                    "0.1.0",
                    "--min-sample-size",
                    "10",
                    "--min-observation-days",
                    "1",
                    "--min-pass-rate",
                    "0.5",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                env=env,
            )
            self.assertEqual(r.returncode, 0, msg=r.stderr)
            pack = json.loads(r.stdout)

            self.assertEqual(pack["strategy_id"], "S1")
            self.assertEqual(pack["sample_size"], 3)
            self.assertEqual(pack["observation_days"], 1)
            self.assertAlmostEqual(pack["metrics"]["pass_rate"], 2 / 3)
            self.assertAlmostEqual(pack["metrics"]["pnl_cumulative"], 5.0)
            self.assertEqual(pack["promotion_gate"]["verdict"], "INSUFFICIENT_SAMPLE")
