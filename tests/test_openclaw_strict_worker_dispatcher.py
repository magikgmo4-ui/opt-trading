"""Tests for openclaw_strict_worker_dispatcher.py — deterministic dispatcher."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DISPATCHER = REPO_ROOT / "scripts/ai/workers/openclaw_strict_worker_dispatcher.py"
JOB_PACKETS_DIR = REPO_ROOT / "scripts/ai/workers/job_packets"

PACKET_READONLY = str(JOB_PACKETS_DIR / "DISPATCHER_SMOKE_READONLY_01.json")
PACKET_WRITEGATED = str(JOB_PACKETS_DIR / "DISPATCHER_SMOKE_WRITEGATED_01.json")
PACKET_REFUSED = str(JOB_PACKETS_DIR / "DISPATCHER_SMOKE_REFUSED_01.json")


def _run(args: list[str], env_extra: dict | None = None) -> tuple[int, dict]:
    import os
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(
        [sys.executable, str(DISPATCHER)] + args,
        capture_output=True, text=True, timeout=60, cwd=REPO_ROOT, env=env,
    )
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        result = {"raw": proc.stdout[:300], "stderr": proc.stderr[:300]}
    return proc.returncode, result


class TestDispatcherStructure(unittest.TestCase):

    def test_dispatcher_is_executable(self):
        self.assertTrue(DISPATCHER.exists(), f"dispatcher not found: {DISPATCHER}")

    def test_no_args_exits_invalid(self):
        rc, out = _run([])
        self.assertEqual(out.get("status"), "INVALID_INPUT")
        self.assertEqual(rc, 1)

    def test_missing_packet_exits_invalid(self):
        rc, out = _run(["--packet", "/nonexistent/path.json"])
        self.assertEqual(out.get("status"), "INVALID_INPUT")
        self.assertEqual(rc, 1)

    def test_missing_packet_id_exits_invalid(self):
        rc, out = _run(["--packet-id", "DOES_NOT_EXIST_PACKET"])
        self.assertEqual(out.get("status"), "INVALID_INPUT")
        self.assertEqual(rc, 1)


class TestDispatcherReadonly(unittest.TestCase):

    def test_readonly_dry_run_pass(self):
        rc, out = _run(["--packet", PACKET_READONLY, "--dry-run"])
        self.assertEqual(out.get("status"), "DRY_RUN_PASS", out)
        self.assertEqual(out.get("dispatcher"), "openclaw_strict_worker_dispatcher")
        self.assertEqual(out.get("task_type"), "READ_INVENTORY")
        self.assertEqual(out.get("runner_called"), "runner_readonly.py")
        self.assertTrue(out.get("dry_run"))
        self.assertFalse(out.get("gate_approved"))
        self.assertEqual(rc, 0)

    def test_readonly_by_packet_id_dry_run(self):
        rc, out = _run(["--packet-id", "DISPATCHER_SMOKE_READONLY_01", "--dry-run"])
        self.assertEqual(out.get("status"), "DRY_RUN_PASS", out)
        self.assertEqual(out.get("runner_called"), "runner_readonly.py")
        self.assertEqual(rc, 0)

    def test_readonly_result_has_required_format3_keys(self):
        rc, out = _run(["--packet", PACKET_READONLY, "--dry-run"])
        for key in ("dispatcher", "status", "job_packet_id", "task_type",
                    "runner_called", "dry_run", "gate_approved",
                    "runner_result", "dispatched_at", "completed_at"):
            self.assertIn(key, out, f"missing key: {key}")

    def test_readonly_job_packet_id_in_output(self):
        rc, out = _run(["--packet", PACKET_READONLY, "--dry-run"])
        self.assertEqual(out.get("job_packet_id"), "DISPATCHER_SMOKE_READONLY_01")


class TestDispatcherWritegated(unittest.TestCase):

    def test_writegated_without_gate_refused(self):
        rc, out = _run(["--packet", PACKET_WRITEGATED])
        self.assertEqual(out.get("status"), "REFUSED", out)
        self.assertEqual(rc, 4)

    def test_writegated_dry_run_pass(self):
        rc, out = _run(["--packet", PACKET_WRITEGATED, "--dry-run"])
        self.assertEqual(out.get("status"), "DRY_RUN_PASS", out)
        self.assertEqual(out.get("runner_called"), "runner_writegated.py")
        self.assertTrue(out.get("dry_run"))
        self.assertEqual(rc, 0)

    def test_writegated_routes_to_writegated_runner(self):
        rc, out = _run(["--packet", PACKET_WRITEGATED, "--dry-run"])
        self.assertEqual(out.get("runner_called"), "runner_writegated.py")

    def test_readonly_packet_does_not_route_to_writegated(self):
        rc, out = _run(["--packet", PACKET_READONLY, "--dry-run"])
        self.assertEqual(out.get("runner_called"), "runner_readonly.py")


class TestDispatcherRefused(unittest.TestCase):

    def test_unknown_task_type_refused(self):
        rc, out = _run(["--packet", PACKET_REFUSED, "--dry-run"])
        self.assertEqual(out.get("status"), "REFUSED", out)
        self.assertEqual(rc, 4)

    def test_unknown_task_type_refused_includes_job_id(self):
        rc, out = _run(["--packet", PACKET_REFUSED, "--dry-run"])
        self.assertEqual(out.get("job_packet_id"), "DISPATCHER_SMOKE_REFUSED_01")

    def test_inline_json_unknown_worker_refused(self):
        packet = {
            "job_packet_id": "INLINE_UNKNOWN_WORKER",
            "task_type": "READ_INVENTORY",
            "default_worker": "nonexistent-model-xyz",
            "scope": {"allowed_inputs": [], "allowed_outputs": []},
        }
        rc, out = _run(["--packet-json", json.dumps(packet), "--dry-run"])
        self.assertEqual(out.get("status"), "REFUSED", out)
        self.assertEqual(rc, 4)

    def test_inline_json_valid_readonly(self):
        packet = {
            "job_packet_id": "INLINE_VALID_READONLY",
            "task_type": "READ_INVENTORY",
            "worker_candidates": ["big-pickle"],
            "default_worker": "big-pickle",
            "scope": {
                "allowed_inputs": ["docs/openclaw/INDEX.md"],
                "allowed_outputs": ["reports/ai/workers/INLINE_VALID_READONLY.md"],
            },
        }
        rc, out = _run(["--packet-json", json.dumps(packet), "--dry-run"])
        self.assertEqual(out.get("status"), "DRY_RUN_PASS", out)
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
