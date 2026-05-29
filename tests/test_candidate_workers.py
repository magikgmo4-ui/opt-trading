"""Tests + smoke for aw_localcms_sync, aw_openclaw_mobile, op_deploy_wrappers.

Goal: validate each candidate is functional, then gate the registry promotion.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKERS_DIR = REPO_ROOT / "scripts" / "ai" / "workers"
if str(WORKERS_DIR) not in sys.path:
    sys.path.insert(0, str(WORKERS_DIR))

import localcms_automation_status_sync as lcs  # noqa: E402
import openclaw_mobile_control as omc           # noqa: E402


# ---------------------------------------------------------------------------
# localcms_automation_status_sync — pure functions
# ---------------------------------------------------------------------------

class TestLocalcmsReadJson(unittest.TestCase):
    def test_existing_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"key": "val"}, f)
            path = Path(f.name)
        self.assertEqual(lcs.read_json(path), {"key": "val"})
        path.unlink()

    def test_missing_file_returns_none(self):
        self.assertIsNone(lcs.read_json(Path("/nonexistent/path.json")))

    def test_invalid_json_returns_none(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not-json{{{")
            path = Path(f.name)
        self.assertIsNone(lcs.read_json(path))
        path.unlink()


class TestLocalcmsLedgerSummary(unittest.TestCase):
    def test_missing_file(self):
        with patch.object(lcs, "LEDGER_FILE", Path("/nonexistent/events.jsonl")):
            summary = lcs.ledger_summary()
        self.assertFalse(summary["exists"])
        self.assertEqual(summary["event_count"], 0)
        self.assertIsNone(summary["last_event"])

    def test_existing_file(self):
        event = {"event_type": "TEST", "status": "PASS", "timestamp": "2026-05-28T00:00:00Z"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            f.write(json.dumps(event) + "\n")
            path = Path(f.name)
        with patch.object(lcs, "LEDGER_FILE", path):
            summary = lcs.ledger_summary()
        path.unlink()
        self.assertTrue(summary["exists"])
        self.assertEqual(summary["event_count"], 1)
        self.assertEqual(summary["last_event"]["event_type"], "TEST")


class TestLocalcmsBuildSnapshot(unittest.TestCase):
    def test_required_keys(self):
        snapshot = lcs.build_snapshot()
        for key in ("generated_at", "git", "menu_loaded", "state_cache_loaded",
                    "ledger", "tmux", "phase", "job_id", "status", "allowed_writes"):
            self.assertIn(key, snapshot)

    def test_phase_and_job_id(self):
        snapshot = lcs.build_snapshot()
        self.assertEqual(snapshot["phase"], "PHASE_01")
        self.assertEqual(snapshot["job_id"], "localcms-automation-status-sync")

    def test_status_pass(self):
        self.assertEqual(lcs.build_snapshot()["status"], "PASS")

    def test_allowed_writes_is_list(self):
        self.assertIsInstance(lcs.build_snapshot()["allowed_writes"], list)


class TestLocalcmsTmuxSessions(unittest.TestCase):
    def test_returns_dict_with_available_key(self):
        result = lcs.tmux_sessions()
        self.assertIn("available", result)
        self.assertIn("sessions", result)
        self.assertIsInstance(result["sessions"], list)


class TestLocalcmsSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.run(
            [sys.executable, str(WORKERS_DIR / "localcms_automation_status_sync.py")],
            capture_output=True, text=True, cwd=str(REPO_ROOT)
        )

    def test_main_exits_zero(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stderr)

    def test_main_writes_valid_snapshot(self):
        snapshot_path = REPO_ROOT / "tmp" / "localcms_latest.json"
        self.assertTrue(snapshot_path.exists())
        data = json.loads(snapshot_path.read_text())
        self.assertEqual(data["status"], "PASS")
        self.assertEqual(data["phase"], "PHASE_01")


# ---------------------------------------------------------------------------
# openclaw_mobile_control — pure functions
# ---------------------------------------------------------------------------

class TestValidatePhase(unittest.TestCase):
    def test_phase_01_pass(self):
        self.assertEqual(omc.validate_phase("PHASE_01"), "PHASE_01")

    def test_phase_01_lowercase_normalised(self):
        self.assertEqual(omc.validate_phase("phase_01"), "PHASE_01")

    def test_phase_02_returns_none(self):
        self.assertIsNone(omc.validate_phase("PHASE_02"))

    def test_none_defaults_to_phase_01(self):
        self.assertEqual(omc.validate_phase(None), "PHASE_01")

    def test_arbitrary_string_returns_none(self):
        self.assertIsNone(omc.validate_phase("LIVE"))


class TestValidateJobForMobile(unittest.TestCase):
    def test_valid_job_returns_none(self):
        job = omc.get_job("repo-status-check")
        self.assertIsNotNone(job)
        self.assertIsNone(omc.validate_job_for_mobile(job))

    def test_none_job_returns_reason(self):
        reason = omc.validate_job_for_mobile(None)
        self.assertIsNotNone(reason)

    def test_forbidden_marker_signal_blocked(self):
        from dataclasses import replace
        job = omc.get_job("repo-status-check")
        bad_job = omc.JobSpec(
            job_id="signal-processor",
            mode="read-only",
            command=None,
            evidence="none",
            allowed_write_scope="none",
            notes="test",
        )
        reason = omc.validate_job_for_mobile(bad_job)
        self.assertIsNotNone(reason)
        self.assertIn("forbidden", reason)

    def test_external_write_scope_blocked(self):
        bad_job = omc.JobSpec(
            job_id="safe-job",
            mode="read-only",
            command=None,
            evidence="none",
            allowed_write_scope="external-s3-bucket",
            notes="test",
        )
        reason = omc.validate_job_for_mobile(bad_job)
        self.assertIsNotNone(reason)


class TestSafeName(unittest.TestCase):
    def test_alphanumeric_unchanged(self):
        self.assertEqual(omc.safe_name("abc123"), "abc123")

    def test_slash_replaced(self):
        self.assertNotIn("/", omc.safe_name("foo/bar"))

    def test_none_returns_all(self):
        self.assertEqual(omc.safe_name(None), "all")

    def test_empty_returns_all(self):
        self.assertEqual(omc.safe_name(""), "all")

    def test_max_length_96(self):
        long = "a" * 200
        self.assertLessEqual(len(omc.safe_name(long)), 96)


class TestGetJob(unittest.TestCase):
    def test_known_job(self):
        job = omc.get_job("repo-status-check")
        self.assertIsNotNone(job)
        self.assertEqual(job.job_id, "repo-status-check")

    def test_unknown_job_returns_none(self):
        self.assertIsNone(omc.get_job("nonexistent-job"))

    def test_none_returns_none(self):
        self.assertIsNone(omc.get_job(None))


class TestSafetyTemplate(unittest.TestCase):
    def test_has_required_fields(self):
        t = omc.safety_template()
        self.assertTrue(t["non_trading_only"])
        self.assertFalse(t["external_write"])
        self.assertFalse(t["signal_trading"])
        self.assertFalse(t["secret_access"])


class TestAllJobs(unittest.TestCase):
    def test_all_phase01_jobs_have_required_attrs(self):
        for job_id, job in omc.PHASE_01_JOBS.items():
            self.assertEqual(job.job_id, job_id)
            self.assertIsInstance(job.mode, str)
            self.assertIsInstance(job.evidence, str)
            self.assertIsInstance(job.allowed_write_scope, str)

    def test_no_job_has_external_write(self):
        for job in omc.PHASE_01_JOBS.values():
            self.assertNotIn("external", job.allowed_write_scope.lower(),
                             f"{job.job_id} has external write scope")


def _omc_run(*args):
    return subprocess.run(
        [sys.executable, str(WORKERS_DIR / "openclaw_mobile_control.py"), *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT)
    )


class TestOpenclawtMobileSmoke(unittest.TestCase):
    def test_status_exits_zero(self):
        proc = _omc_run("status")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_status_valid_json(self):
        proc = _omc_run("status")
        data = json.loads(proc.stdout)
        self.assertEqual(data["status"], "PASS")
        self.assertTrue(data["ok"])

    def test_list_jobs_exits_zero(self):
        proc = _omc_run("list-jobs")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_list_jobs_count(self):
        proc = _omc_run("list-jobs")
        data = json.loads(proc.stdout)
        self.assertEqual(len(data["jobs"]), len(omc.PHASE_01_JOBS))

    def test_preflight_valid_job(self):
        proc = _omc_run("preflight", "--job", "repo-status-check")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["status"], "PASS")


# ---------------------------------------------------------------------------
# deploy_wrappers_ot_wrap_01.sh — bash structure + syntax
# ---------------------------------------------------------------------------

DEPLOY_SCRIPT = REPO_ROOT / "scripts" / "deploy_wrappers_ot_wrap_01.sh"


class TestDeployWrappers(unittest.TestCase):
    def test_script_exists(self):
        self.assertTrue(DEPLOY_SCRIPT.exists())

    def test_bash_syntax_valid(self):
        result = subprocess.run(
            ["bash", "-n", str(DEPLOY_SCRIPT)],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_has_error_handling(self):
        content = DEPLOY_SCRIPT.read_text()
        self.assertIn("set -euo pipefail", content)

    def test_references_validated_prompt_factory(self):
        self.assertIn("validated_prompt_factory", DEPLOY_SCRIPT.read_text())

    def test_references_trae_module_validator(self):
        self.assertIn("trae_module_validator", DEPLOY_SCRIPT.read_text())

    def test_uses_symlink_pattern(self):
        self.assertIn("ln -sf", DEPLOY_SCRIPT.read_text())


if __name__ == "__main__":
    unittest.main()
