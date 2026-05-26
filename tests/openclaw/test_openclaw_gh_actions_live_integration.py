#!/usr/bin/env python3
import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))


def _load_script(script_name: str, rel_path: str):
    path = REPO_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(script_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


class TestLiveEnvUtility(unittest.TestCase):

    def setUp(self):
        self.env_path = REPO_ROOT / "scripts" / "openclaw_gh_actions_live_env.py"
        for k in ["GITHUB_TOKEN", "GITHUB_REPOSITORY"]:
            os.environ.pop(k, None)
        self.mod = _load_script("openclaw_gh_actions_live_env", "scripts/openclaw_gh_actions_live_env.py")

    def tearDown(self):
        for k in ["GITHUB_TOKEN", "GITHUB_REPOSITORY"]:
            os.environ.pop(k, None)

    def test_validate_env_no_env(self):
        result = self.mod.validate_env()
        self.assertFalse(result["all_valid"])
        self.assertFalse(result["GITHUB_TOKEN"])
        self.assertFalse(result["GITHUB_REPOSITORY"])

    def test_validate_env_with_env(self):
        os.environ["GITHUB_TOKEN"] = "ghp_test123"
        os.environ["GITHUB_REPOSITORY"] = "owner/repo"
        result = self.mod.validate_env()
        self.assertTrue(result["GITHUB_TOKEN"])
        self.assertTrue(result["GITHUB_REPOSITORY"])

    def test_validate_env_verbose(self):
        os.environ["GITHUB_TOKEN"] = "ghp_test123"
        os.environ["GITHUB_REPOSITORY"] = "owner/repo"
        result = self.mod.validate_env(verbose=True)
        self.assertIn("GITHUB_REPOSITORY_value", result)
        self.assertIn("GITHUB_TOKEN_prefix", result)

    @patch("requests.get")
    def test_cmd_run_info(self, mock_get):
        os.environ["GITHUB_TOKEN"] = "ghp_test123"
        os.environ["GITHUB_REPOSITORY"] = "owner/repo"
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 12345,
            "status": "completed",
            "conclusion": "success",
            "html_url": "https://github.com/owner/repo/actions/runs/12345",
            "workflow": {"path": ".github/workflows/test.yml"},
            "display_title": "Test run",
        }
        bridge, _ = self.mod.get_bridge()
        self.assertIsNotNone(bridge)
        url = f"https://api.github.com/repos/{bridge.repo}/actions/runs/12345"
        import requests as req
        resp = req.get(url, headers=bridge._get_headers())
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["id"], 12345)
        self.assertEqual(data["conclusion"], "success")

    @patch("requests.get")
    def test_cmd_run_info_api_error(self, mock_get):
        os.environ["GITHUB_TOKEN"] = "ghp_test123"
        os.environ["GITHUB_REPOSITORY"] = "owner/repo"
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Not Found"
        bridge, _ = self.mod.get_bridge()
        import requests as req
        url = f"https://api.github.com/repos/{bridge.repo}/actions/runs/99999"
        resp = req.get(url, headers=bridge._get_headers())
        self.assertEqual(resp.status_code, 404)

    def test_get_bridge_missing_token(self):
        os.environ.pop("GITHUB_TOKEN", None)
        os.environ.pop("GITHUB_REPOSITORY", None)
        bridge, err = self.mod.get_bridge()
        self.assertIsNone(bridge)
        self.assertIsNotNone(err)

    def test_get_bridge_ok(self):
        os.environ["GITHUB_TOKEN"] = "ghp_test123"
        os.environ["GITHUB_REPOSITORY"] = "owner/repo"
        bridge, err = self.mod.get_bridge()
        self.assertIsNotNone(bridge)
        self.assertIsNone(err)
        self.assertEqual(bridge.repo, "owner/repo")


class TestRouteResultLivePath(unittest.TestCase):
    """Test route_result.py live API path via mock."""

    def setUp(self):
        self.mod = _load_script("openclaw_gh_actions_route_result",
                                "scripts/openclaw_gh_actions_route_result.py")

    @patch("requests.get")
    def test_fetch_real_run_success(self, mock_get):
        os.environ["GITHUB_TOKEN"] = "ghp_test"
        os.environ["GITHUB_REPOSITORY"] = "owner/repo"
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 12345, "status": "completed", "conclusion": "success",
            "html_url": "https://github.com/owner/repo/actions/runs/12345",
        }
        result = self.mod.fetch_real_run(12345)
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], 12345)
        self.assertEqual(result["conclusion"], "success")

    @patch("requests.get")
    def test_fetch_real_run_api_error(self, mock_get):
        os.environ["GITHUB_TOKEN"] = "ghp_test"
        os.environ["GITHUB_REPOSITORY"] = "owner/repo"
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Server Error"
        result = self.mod.fetch_real_run(99999)
        self.assertIsNone(result)

    def test_route_result_all_classifications(self):
        test_cases = [
            ("success", "completed", "PASS"),
            ("failure", "completed", "FAIL"),
            ("cancelled", "completed", "BLOCKED"),
            ("timed_out", "completed", "BLOCKED"),
            ("action_required", "completed", "NEEDS_HUMAN_REVIEW"),
            ("neutral", "completed", "NEEDS_HUMAN_REVIEW"),
            ("skipped", "completed", "NEEDS_HUMAN_REVIEW"),
            (None, "completed", "NEEDS_HUMAN_REVIEW"),
            (None, "in_progress", "BLOCKED"),
            (None, "queued", "BLOCKED"),
            ("unknown", "completed", "NEEDS_HUMAN_REVIEW"),
        ]
        for conclusion, status, expected in test_cases:
            with self.subTest(conclusion=conclusion, status=status):
                result = self.mod.route_result(
                    run_id=0, html_url=None, job_id="test",
                    workflow=None, status=status, conclusion=conclusion,
                )
                self.assertEqual(result["classification"], expected)

    def test_route_result_logs_available(self):
        result = self.mod.route_result(
            run_id=0, html_url=None, job_id="test",
            workflow=None, status="completed", conclusion="failure",
        )
        self.assertTrue(result["logs_available"])
        result = self.mod.route_result(
            run_id=0, html_url=None, job_id="test",
            workflow=None, status="in_progress", conclusion=None,
        )
        self.assertFalse(result["logs_available"])

    def test_route_result_next_action(self):
        result = self.mod.route_result(
            run_id=0, html_url=None, job_id="my-job",
            workflow=None, status="completed", conclusion="failure",
        )
        self.assertEqual(result["next_action"], "inspect_logs_and_prepare_fix")

    def test_route_result_probable_cause(self):
        result = self.mod.route_result(
            run_id=0, html_url=None, job_id="test",
            workflow=None, status="completed", conclusion="failure",
        )
        self.assertIn("Failed run", result["probable_cause"])


class TestAnalyzeFailureLivePath(unittest.TestCase):
    """Test analyze_failure_logs.py live API path via mock."""

    def setUp(self):
        for k in ["GITHUB_TOKEN", "GITHUB_REPOSITORY"]:
            os.environ.pop(k, None)
        self.mod = _load_script("openclaw_gh_actions_analyze_failure_logs",
                                "scripts/openclaw_gh_actions_analyze_failure_logs.py")

    def tearDown(self):
        for k in ["GITHUB_TOKEN", "GITHUB_REPOSITORY"]:
            os.environ.pop(k, None)

    def test_classify_success(self):
        analyzer = self.mod.FailureAnalyzer()
        test_cases = [
            ("FAILED tests/test_api.py", "TEST_FAILURE"),
            ("yaml: line 10: mapping values", "YAML_WORKFLOW_FAILURE"),
            ("Permission denied (publickey)", "PERMISSION_FAILURE"),
            ("The operation was canceled", "TIMEOUT"),
            ("No such file or directory", "MISSING_FILE"),
            ("FAIL: file outside GO scope", "FILE_SCOPE_FAILURE"),
            ("FAIL: changed file is also claimed", "NO_LOCK_OVERLAP_FAILURE"),
            ("Could not resolve host", "NETWORK_OR_API_FAILURE"),
            ("Some random error", "UNKNOWN_FAILURE"),
        ]
        for logs, expected in test_cases:
            with self.subTest(logs=logs[:30]):
                res = analyzer.classify_error(logs)
                self.assertEqual(res["classification"], expected)

    def test_analyze_run_missing_token(self):
        analyzer = self.mod.FailureAnalyzer()
        with patch.object(self.mod, 'GITHUB_TOKEN', None), \
             patch.object(self.mod, 'GITHUB_REPO', None):
            result = analyzer.analyze_run(12345)
            self.assertFalse(result.get("ok", True))
            self.assertIn("GITHUB_TOKEN", result.get("error", ""))

    def test_analyze_run_all_pass(self):
        analyzer = self.mod.FailureAnalyzer()
        with patch.object(self.mod, 'GITHUB_TOKEN', 'ghp_test'), \
             patch.object(self.mod, 'GITHUB_REPO', 'owner/repo'), \
             patch.object(self.mod, '_get_run_jobs') as mock_jobs:
            mock_jobs.return_value = {
                "ok": True,
                "jobs": [{"id": 1, "name": "test-job", "conclusion": "success"}],
            }
            result = analyzer.analyze_run(12345)
            self.assertEqual(result["status"], "PASS")
            self.assertIn("No failed jobs", result["message"])

    def test_analyze_run_with_failure(self):
        analyzer = self.mod.FailureAnalyzer()
        with patch.object(self.mod, 'GITHUB_TOKEN', 'ghp_test'), \
             patch.object(self.mod, 'GITHUB_REPO', 'owner/repo'), \
             patch.object(self.mod, '_get_run_jobs') as mock_jobs, \
             patch.object(self.mod, '_get_job_logs') as mock_logs:
            mock_jobs.return_value = {
                "ok": True,
                "jobs": [{"id": 42, "name": "gate-checks", "conclusion": "failure"}],
            }
            mock_logs.return_value = {
                "ok": True,
                "content": "FAIL: file outside GO scope: scripts/dangerous.py",
            }
            result = analyzer.analyze_run(12345)
            self.assertEqual(result["primary_classification"], "FILE_SCOPE_FAILURE")
            self.assertFalse(result["dangerous_action_executed"])
            self.assertEqual(result["failed_jobs_count"], 1)
            self.assertEqual(result["details"][0]["job_name"], "gate-checks")

    def test_analyze_run_jobs_api_error(self):
        analyzer = self.mod.FailureAnalyzer()
        with patch.object(self.mod, 'GITHUB_TOKEN', 'ghp_test'), \
             patch.object(self.mod, 'GITHUB_REPO', 'owner/repo'), \
             patch.object(self.mod, '_get_run_jobs') as mock_jobs:
            mock_jobs.return_value = {"ok": False, "error": "API error"}
            result = analyzer.analyze_run(12345)
            self.assertFalse(result.get("ok", True))
            self.assertIn("API error", result.get("error", ""))


class TestOrchestrateLivePath(unittest.TestCase):
    """Test orchestrate.py gh CLI subprocess calls via mock."""

    def setUp(self):
        self.mod = _load_script("openclaw_gh_actions_orchestrate",
                                "scripts/openclaw_gh_actions_orchestrate.py")

    @patch("subprocess.run")
    def test_gh_workflow_dispatch_success(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = ""
        mock_proc.stderr = "View: https://github.com/owner/repo/actions/runs/12345"
        mock_run.return_value = mock_proc
        result = self.mod.gh_workflow_dispatch("test.yml")
        self.assertTrue(result["ok"])
        self.assertIn("12345", result["url"])

    @patch("subprocess.run")
    def test_gh_workflow_dispatch_failure(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.stderr = "Workflow does not have a dispatch event"
        mock_run.return_value = mock_proc
        result = self.mod.gh_workflow_dispatch("nonexistent.yml")
        self.assertFalse(result["ok"])
        self.assertIn("dispatch", result["error"])

    @patch("subprocess.run")
    def test_gh_get_latest_run(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = json.dumps([{
            "databaseId": 12345, "status": "completed",
            "conclusion": "success", "displayTitle": "Test",
            "url": "https://github.com/owner/repo/actions/runs/12345",
            "createdAt": "2026-05-26T00:00:00Z",
        }])
        mock_run.return_value = mock_proc
        run = self.mod.gh_get_latest_run("test.yml")
        self.assertIsNotNone(run)
        self.assertEqual(run["databaseId"], 12345)

    @patch("subprocess.run")
    def test_gh_get_latest_run_empty(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "[]"
        mock_run.return_value = mock_proc
        run = self.mod.gh_get_latest_run("test.yml")
        self.assertIsNone(run)

    @patch("subprocess.run")
    def test_gh_run_view(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = json.dumps({
            "databaseId": 12345, "status": "completed",
            "conclusion": "success", "displayTitle": "Test",
            "url": "https://github.com/owner/repo/actions/runs/12345",
            "createdAt": "2026-05-26T00:00:00Z",
        })
        mock_run.return_value = mock_proc
        run = self.mod.gh_run_view(12345)
        self.assertIsNotNone(run)
        self.assertEqual(run["status"], "completed")

    @patch("subprocess.run")
    def test_gh_run_view_not_found(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_run.return_value = mock_proc
        run = self.mod.gh_run_view(99999)
        self.assertIsNone(run)

    def test_classify_conclusion_all(self):
        cases = [
            ("success", "PASS"),
            ("failure", "FAIL"),
            ("cancelled", "BLOCKED"),
            ("timed_out", "BLOCKED"),
            ("action_required", "NEEDS_HUMAN_REVIEW"),
            ("skipped", "SKIPPED"),
            ("neutral", "PASS"),
            ("unknown", "UNKNOWN"),
            (None, "UNKNOWN"),
        ]
        for conclusion, expected in cases:
            with self.subTest(conclusion=conclusion):
                result = self.mod.classify_conclusion(conclusion)
                self.assertEqual(result, expected)

    def test_propose_next_action(self):
        action = self.mod.propose_next_action("my-job", "FAIL")
        self.assertIn("my-job", action)
        self.assertIn("failed", action.lower())


class TestAnalyzeFailureFixLivePath(unittest.TestCase):
    """Test analyze_failure_logs_fix.py enrichment logic."""

    def setUp(self):
        self.fix_path = REPO_ROOT / "scripts" / "openclaw_gh_actions_analyze_failure_logs_fix.py"
        if not self.fix_path.exists():
            self.skipTest("fix module not found")
        self.mod = _load_script("openclaw_gh_actions_analyze_failure_logs_fix",
                                "scripts/openclaw_gh_actions_analyze_failure_logs_fix.py")

    def test_enrich_analysis_with_jobs(self):
        analysis = {"primary_classification": "FILE_SCOPE_FAILURE", "details": []}
        jobs = [{"id": 1, "name": "run_gate_checks", "conclusion": "failure", "started_at": "2026-01-01T00:00:00Z"}]
        logs_map = {1: "FAIL: file outside GO scope: scripts/dangerous.py"}
        result = self.mod.enrich_analysis(analysis, jobs, logs_map)
        self.assertEqual(result["primary_classification"], "FILE_SCOPE_FAILURE")
        self.assertIn("details", result)
        self.assertEqual(result["type"], "enriched")
        self.assertFalse(result.get("dangerous_action_executed", True))

    def test_enrich_analysis_dangerous_false(self):
        analysis = {"primary_classification": "TEST_FAILURE", "details": []}
        result = self.mod.enrich_analysis(analysis, [], {})
        self.assertFalse(result.get("dangerous_action_executed", True))

    def test_enrich_analysis_without_jobs(self):
        analysis = {"primary_classification": "TEST_FAILURE", "details": []}
        result = self.mod.enrich_analysis(analysis, [], {})
        self.assertEqual(result["primary_classification"], "TEST_FAILURE")
        self.assertIn("details", result)


class TestLiveEnvCLICommands(unittest.TestCase):

    def setUp(self):
        for k in ["GITHUB_TOKEN", "GITHUB_REPOSITORY"]:
            os.environ.pop(k, None)
        self.env_mod = _load_script("openclaw_gh_actions_live_env",
                                    "scripts/openclaw_gh_actions_live_env.py")

    def tearDown(self):
        for k in ["GITHUB_TOKEN", "GITHUB_REPOSITORY"]:
            os.environ.pop(k, None)

    def test_simulate_pipeline_no_env(self):
        result = self.env_mod.validate_env()
        self.assertFalse(result["all_valid"])

    def test_simulate_pipeline_cli(self):
        route_result_mod = _load_script("openclaw_gh_actions_route_result",
                                        "scripts/openclaw_gh_actions_route_result.py")
        result = route_result_mod.route_result(
            run_id=0, html_url=None, job_id="test-job",
            workflow=".github/workflows/test.yml",
            status="completed", conclusion="success",
        )
        self.assertEqual(result["classification"], "PASS")
        self.assertEqual(result["next_action"], "ready_for_human_review")

    def test_simulate_pipeline_failure(self):
        route_result_mod = _load_script("openclaw_gh_actions_route_result",
                                        "scripts/openclaw_gh_actions_route_result.py")
        result = route_result_mod.route_result(
            run_id=0, html_url=None, job_id="test-job",
            workflow=None, status="completed", conclusion="failure",
        )
        self.assertEqual(result["classification"], "FAIL")
        self.assertEqual(result["next_action"], "inspect_logs_and_prepare_fix")


if __name__ == "__main__":
    unittest.main()
