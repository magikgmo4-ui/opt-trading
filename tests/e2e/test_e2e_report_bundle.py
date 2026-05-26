"""
Tests for scripts/e2e/build_e2e_report_bundle.py

Coverage:
  - env validation (required flags, forbidden flags)
  - report validation (live_trade, gate_status, dry_run, missing post_gate)
  - bundle writing (all 5 files, contents, no secrets)
  - payload_refs structure
  - summary.md content
  - full integration via subprocess (setUpClass)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_BUNDLE_SCRIPT = REPO_ROOT / "scripts" / "e2e" / "build_e2e_report_bundle.py"

_BASE_ENV = {
    **os.environ,
    "ALLOW_E2E_LIVE_DRY_RUN": "1",
    "DRY_RUN": "1",
    "PAPER_MODE": "1",
    "ALLOW_LIVE_TRADE": "",
    "ALLOW_GOOGLE_SHEETS_API_WRITE": "",
    "ALLOW_TELEGRAM_SEND": "",
}

# ── helpers ───────────────────────────────────────────────────────────────────

def _run_bundle(extra: dict | None = None, drop: list | None = None,
                timeout: int = 90, extra_args: list | None = None) -> tuple[dict, str, int]:
    """Run build_e2e_report_bundle.py and return (parsed_json, stderr, rc)."""
    env = {**_BASE_ENV}
    if extra:
        env.update(extra)
    for k in (drop or []):
        env.pop(k, None)
    env = {k: v for k, v in env.items() if v != ""}

    cmd = [sys.executable, str(_BUNDLE_SCRIPT)] + (extra_args or [])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                            cwd=str(REPO_ROOT), env=env)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        data = {}
    return data, result.stderr, result.returncode


# ── Unit tests — env validation ───────────────────────────────────────────────

class TestEnvValidation(unittest.TestCase):
    """Import-level tests against _validate_env() directly."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import importlib
        import scripts.e2e.build_e2e_report_bundle as mod
        cls.mod = mod

    def _with_env(self, env: dict):
        old = {k: os.environ.get(k) for k in env}
        for k, v in env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        return old

    def _restore(self, saved: dict):
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_valid_env_returns_dict(self):
        saved = self._with_env({"ALLOW_E2E_LIVE_DRY_RUN": "1", "DRY_RUN": "1",
                                 "ALLOW_LIVE_TRADE": None, "ALLOW_GOOGLE_SHEETS_API_WRITE": None,
                                 "ALLOW_TELEGRAM_SEND": None})
        try:
            flags = self.mod._validate_env()
            self.assertIsInstance(flags, dict)
            self.assertEqual(flags.get("ALLOW_E2E_LIVE_DRY_RUN"), "1")
            self.assertEqual(flags.get("DRY_RUN"), "1")
        finally:
            self._restore(saved)

    def test_missing_allow_e2e_raises(self):
        saved = self._with_env({"ALLOW_E2E_LIVE_DRY_RUN": None, "DRY_RUN": "1"})
        try:
            with self.assertRaises(self.mod.BundleRefused) as ctx:
                self.mod._validate_env()
            self.assertIn("ALLOW_E2E_LIVE_DRY_RUN", str(ctx.exception))
        finally:
            self._restore(saved)

    def test_missing_dry_run_raises(self):
        saved = self._with_env({"ALLOW_E2E_LIVE_DRY_RUN": "1", "DRY_RUN": None})
        try:
            with self.assertRaises(self.mod.BundleRefused) as ctx:
                self.mod._validate_env()
            self.assertIn("DRY_RUN", str(ctx.exception))
        finally:
            self._restore(saved)

    def test_allow_live_trade_raises(self):
        saved = self._with_env({"ALLOW_E2E_LIVE_DRY_RUN": "1", "DRY_RUN": "1",
                                 "ALLOW_LIVE_TRADE": "1"})
        try:
            with self.assertRaises(self.mod.BundleRefused) as ctx:
                self.mod._validate_env()
            self.assertIn("ALLOW_LIVE_TRADE", str(ctx.exception))
        finally:
            self._restore(saved)

    def test_allow_sheets_api_write_raises(self):
        saved = self._with_env({"ALLOW_E2E_LIVE_DRY_RUN": "1", "DRY_RUN": "1",
                                 "ALLOW_GOOGLE_SHEETS_API_WRITE": "1",
                                 "ALLOW_LIVE_TRADE": None})
        try:
            with self.assertRaises(self.mod.BundleRefused) as ctx:
                self.mod._validate_env()
            self.assertIn("ALLOW_GOOGLE_SHEETS_API_WRITE", str(ctx.exception))
        finally:
            self._restore(saved)

    def test_allow_telegram_send_raises(self):
        saved = self._with_env({"ALLOW_E2E_LIVE_DRY_RUN": "1", "DRY_RUN": "1",
                                 "ALLOW_TELEGRAM_SEND": "1",
                                 "ALLOW_LIVE_TRADE": None,
                                 "ALLOW_GOOGLE_SHEETS_API_WRITE": None})
        try:
            with self.assertRaises(self.mod.BundleRefused) as ctx:
                self.mod._validate_env()
            self.assertIn("ALLOW_TELEGRAM_SEND", str(ctx.exception))
        finally:
            self._restore(saved)


# ── Unit tests — report validation ────────────────────────────────────────────

class TestReportValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import scripts.e2e.build_e2e_report_bundle as mod
        cls.mod = mod

    def _good_report(self) -> dict:
        return {
            "dry_run": True,
            "e2e_post_gate_status": {
                "status": "PASS",
                "dry_run": True,
                "live_trade": False,
                "gate_status": "APPROVED_PAPER",
                "localcms_gate": "WARN_SKIPPED",
                "sheets_mode": "fake",
                "telegram_mode": "dry_run",
                "modules": {m: "PASS" for m in [
                    "signal_router", "proposition_engine", "validation_gate",
                    "trade_executor", "result_tracker", "datasheet_writer", "learning_feeder",
                ]},
            },
        }

    def test_valid_report_passes(self):
        self.mod._validate_report(self._good_report())

    def test_missing_post_gate_status_raises(self):
        report = self._good_report()
        del report["e2e_post_gate_status"]
        with self.assertRaises(self.mod.BundleRefused) as ctx:
            self.mod._validate_report(report)
        self.assertIn("e2e_post_gate_status missing", str(ctx.exception))

    def test_blocked_status_raises(self):
        report = self._good_report()
        report["e2e_post_gate_status"]["status"] = "BLOCKED"
        report["e2e_post_gate_status"]["reason"] = "DRY_RUN=1 required"
        with self.assertRaises(self.mod.BundleRefused) as ctx:
            self.mod._validate_report(report)
        self.assertIn("BLOCKED", str(ctx.exception))

    def test_live_trade_true_raises(self):
        report = self._good_report()
        report["e2e_post_gate_status"]["live_trade"] = True
        with self.assertRaises(self.mod.BundleRefused) as ctx:
            self.mod._validate_report(report)
        self.assertIn("live_trade=True", str(ctx.exception))

    def test_wrong_gate_status_raises(self):
        report = self._good_report()
        report["e2e_post_gate_status"]["gate_status"] = "REJECTED"
        with self.assertRaises(self.mod.BundleRefused) as ctx:
            self.mod._validate_report(report)
        self.assertIn("gate_status", str(ctx.exception))

    def test_dry_run_false_raises(self):
        report = self._good_report()
        report["dry_run"] = False
        with self.assertRaises(self.mod.BundleRefused) as ctx:
            self.mod._validate_report(report)
        self.assertIn("dry_run", str(ctx.exception))

    def test_localcms_warn_skipped_accepted(self):
        report = self._good_report()
        report["e2e_post_gate_status"]["localcms_gate"] = "WARN_SKIPPED"
        self.mod._validate_report(report)

    def test_gate_status_none_raises(self):
        report = self._good_report()
        report["e2e_post_gate_status"]["gate_status"] = None
        with self.assertRaises(self.mod.BundleRefused):
            self.mod._validate_report(report)


# ── Unit tests — bundle writers ───────────────────────────────────────────────

class TestBundleWriters(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import scripts.e2e.build_e2e_report_bundle as mod
        cls.mod = mod

    def _good_report(self) -> dict:
        return {
            "pipeline_name": "E2E post-gate live/dry-run",
            "dry_run": True,
            "started_at": "2026-05-26T10:00:00+00:00",
            "completed_at": "2026-05-26T10:00:05+00:00",
            "duration_s": 5.0,
            "steps": [
                {"step": "1_signal_router", "result": {
                    "signal_id": "sig-001", "ticker": "BTCUSDT",
                    "side": "BUY", "price": 67000.0, "strategy_id": "ST_DCA_01",
                }},
                {"step": "2_proposition_engine", "result": {
                    "request_id": "req-001", "action": "BUY", "confidence": 0.9,
                }},
                {"step": "3_validation_gate", "result": {
                    "request_id": "req-001", "verdict": "APPROVED", "risk_status": "OK",
                }},
                {"step": "4_trade_executor", "result": {
                    "trade_id": "trade-001", "status": "FILLED",
                    "fill_price": 67010.0, "fill_qty": 0.01, "dry_run": True,
                }},
                {"step": "5_result_tracker", "result": {
                    "trade_id": "trade-001", "outcome": "WIN",
                    "gross_pnl": 10.0, "net_pnl": 9.5, "fees": 0.5,
                    "opened_at": "2026-05-26T10:00:01+00:00",
                    "closed_at": "2026-05-26T10:00:04+00:00",
                }},
                {"step": "6_datasheet_writer", "result": {
                    "dry_run": True, "written": True,
                    "jsonl_path": None, "csv_path": None,
                }},
                {"step": "7_learning_feeder", "result": {
                    "request_id": "req-001", "bridge_status": "SKIPPED",
                    "brick_stored": False, "brick_id": None,
                }},
            ],
            "e2e_post_gate_status": {
                "status": "PASS",
                "dry_run": True,
                "live_trade": False,
                "gate_status": "APPROVED_PAPER",
                "localcms_gate": "WARN_SKIPPED",
                "sheets_mode": "fake",
                "telegram_mode": "dry_run",
                "modules": {m: "PASS" for m in [
                    "signal_router", "proposition_engine", "validation_gate",
                    "trade_executor", "result_tracker", "datasheet_writer", "learning_feeder",
                ]},
            },
        }

    def _env_flags(self) -> dict:
        return {
            "ALLOW_E2E_LIVE_DRY_RUN": "1",
            "DRY_RUN": "1",
            "ALLOW_LIVE_TRADE": None,
            "ALLOW_GOOGLE_SHEETS_API_WRITE": None,
            "ALLOW_TELEGRAM_SEND": None,
            "PAPER_MODE": "1",
            "REQUIRE_LOCALCMS_E2E": "0",
            "SKIP_LOCALCMS_E2E": "0",
            "LOCALCMS_URL": "http://127.0.0.1:8700",
        }

    def test_manifest_go_pf_fields(self):
        manifest = self.mod._build_manifest("test_run_001", self._good_report(), self._env_flags())
        self.assertEqual(manifest["go_id"], self.mod.GO_ID)
        self.assertEqual(manifest["pf_id"], self.mod.PF_ID)
        self.assertEqual(manifest["parent_go"], self.mod.PARENT_GO)

    def test_manifest_run_id_present(self):
        manifest = self.mod._build_manifest("run_20260526_120000", self._good_report(), self._env_flags())
        self.assertEqual(manifest["run_id"], "run_20260526_120000")

    def test_manifest_verdict_pass(self):
        manifest = self.mod._build_manifest("r1", self._good_report(), self._env_flags())
        self.assertEqual(manifest["verdict"], "PASS")

    def test_manifest_gate_status_approved_paper(self):
        manifest = self.mod._build_manifest("r1", self._good_report(), self._env_flags())
        self.assertEqual(manifest["gate_status"], "APPROVED_PAPER")

    def test_manifest_dry_run_true(self):
        manifest = self.mod._build_manifest("r1", self._good_report(), self._env_flags())
        self.assertIs(manifest["dry_run"], True)

    def test_manifest_live_trade_false(self):
        manifest = self.mod._build_manifest("r1", self._good_report(), self._env_flags())
        self.assertFalse(manifest["live_trade"])

    def test_manifest_has_7_modules(self):
        manifest = self.mod._build_manifest("r1", self._good_report(), self._env_flags())
        self.assertEqual(len(manifest["modules"]), 7)

    def test_manifest_all_modules_pass(self):
        manifest = self.mod._build_manifest("r1", self._good_report(), self._env_flags())
        for mod_name, status in manifest["modules"].items():
            self.assertEqual(status, "PASS", f"{mod_name} expected PASS")

    def test_payload_refs_signal_fields(self):
        refs = self.mod._build_payload_refs(self._good_report())
        sig = refs["signal"]
        self.assertEqual(sig["signal_id"], "sig-001")
        self.assertEqual(sig["ticker"], "BTCUSDT")
        self.assertEqual(sig["side"], "BUY")

    def test_payload_refs_trade_dry_run(self):
        refs = self.mod._build_payload_refs(self._good_report())
        self.assertIs(refs["trade"]["dry_run"], True)

    def test_payload_refs_all_7_keys(self):
        refs = self.mod._build_payload_refs(self._good_report())
        self.assertIn("signal", refs)
        self.assertIn("proposition", refs)
        self.assertIn("gate", refs)
        self.assertIn("trade", refs)
        self.assertIn("result", refs)
        self.assertIn("datasheet", refs)
        self.assertIn("learning", refs)

    def test_payload_refs_result_outcome(self):
        refs = self.mod._build_payload_refs(self._good_report())
        self.assertEqual(refs["result"]["outcome"], "WIN")
        self.assertEqual(refs["result"]["net_pnl"], 9.5)

    def test_summary_md_contains_verdict(self):
        report = self._good_report()
        manifest = self.mod._build_manifest("r1", report, self._env_flags())
        refs = self.mod._build_payload_refs(report)
        md = self.mod._build_summary_md("r1", manifest, refs)
        self.assertIn("PASS", md)

    def test_summary_md_contains_run_id(self):
        report = self._good_report()
        manifest = self.mod._build_manifest("r1", report, self._env_flags())
        refs = self.mod._build_payload_refs(report)
        md = self.mod._build_summary_md("r1", manifest, refs)
        self.assertIn("r1", md)

    def test_summary_md_contains_gate_status(self):
        report = self._good_report()
        manifest = self.mod._build_manifest("r1", report, self._env_flags())
        refs = self.mod._build_payload_refs(report)
        md = self.mod._build_summary_md("r1", manifest, refs)
        self.assertIn("APPROVED_PAPER", md)

    def test_summary_md_contains_dry_run_true(self):
        report = self._good_report()
        manifest = self.mod._build_manifest("r1", report, self._env_flags())
        refs = self.mod._build_payload_refs(report)
        md = self.mod._build_summary_md("r1", manifest, refs)
        self.assertIn("True", md)

    def test_write_bundle_creates_5_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = self.mod.write_bundle(
                self._good_report(), self._env_flags(),
                Path(tmpdir), run_id="test_bundle_001",
            )
            files = {f.name for f in bundle_dir.iterdir()}
            self.assertIn("manifest.json", files)
            self.assertIn("e2e_report.json", files)
            self.assertIn("environment_flags.json", files)
            self.assertIn("payload_refs.json", files)
            self.assertIn("summary.md", files)

    def test_write_bundle_no_secrets_in_manifest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = self.mod.write_bundle(
                self._good_report(), self._env_flags(),
                Path(tmpdir), run_id="secret_test",
            )
            manifest_text = (bundle_dir / "manifest.json").read_text()
            for secret_key in ["TELEGRAM_BOT_TOKEN", "TV_WEBHOOK_KEY", "OPS_ADMIN_KEY"]:
                self.assertNotIn(secret_key, manifest_text)

    def test_write_bundle_no_secrets_in_env_flags(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = self.mod.write_bundle(
                self._good_report(), self._env_flags(),
                Path(tmpdir), run_id="env_secret_test",
            )
            env_text = (bundle_dir / "environment_flags.json").read_text()
            for secret_key in ["TELEGRAM_BOT_TOKEN", "TV_WEBHOOK_KEY", "OPS_ADMIN_KEY"]:
                self.assertNotIn(secret_key, env_text)

    def test_write_bundle_manifest_parseable_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = self.mod.write_bundle(
                self._good_report(), self._env_flags(),
                Path(tmpdir), run_id="json_test",
            )
            manifest = json.loads((bundle_dir / "manifest.json").read_text())
            self.assertEqual(manifest["bundle_version"], "1.0")

    def test_write_bundle_payload_refs_parseable(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = self.mod.write_bundle(
                self._good_report(), self._env_flags(),
                Path(tmpdir), run_id="refs_test",
            )
            refs = json.loads((bundle_dir / "payload_refs.json").read_text())
            self.assertIn("signal", refs)
            self.assertIn("trade", refs)


# ── Unit tests — build_bundle with mocked pipeline ───────────────────────────

class TestBuildBundleUnit(unittest.TestCase):
    """Test build_bundle() using --pipeline-output to skip live pipeline call."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import scripts.e2e.build_e2e_report_bundle as mod
        cls.mod = mod

    def _good_report(self) -> dict:
        return {
            "pipeline_name": "E2E post-gate live/dry-run",
            "dry_run": True,
            "started_at": "2026-05-26T10:00:00+00:00",
            "completed_at": "2026-05-26T10:00:05+00:00",
            "duration_s": 5.0,
            "steps": [],
            "e2e_post_gate_status": {
                "status": "PASS",
                "dry_run": True,
                "live_trade": False,
                "gate_status": "APPROVED_PAPER",
                "localcms_gate": "WARN_SKIPPED",
                "sheets_mode": "fake",
                "telegram_mode": "dry_run",
                "modules": {m: "PASS" for m in [
                    "signal_router", "proposition_engine", "validation_gate",
                    "trade_executor", "result_tracker", "datasheet_writer", "learning_feeder",
                ]},
            },
        }

    def test_build_bundle_from_file_status_bundled(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "report.json"
            report_path.write_text(json.dumps(self._good_report()), encoding="utf-8")

            saved = {}
            for k, v in {"ALLOW_E2E_LIVE_DRY_RUN": "1", "DRY_RUN": "1"}.items():
                saved[k] = os.environ.get(k)
                os.environ[k] = v
            for k in ["ALLOW_LIVE_TRADE", "ALLOW_GOOGLE_SHEETS_API_WRITE", "ALLOW_TELEGRAM_SEND"]:
                saved[k] = os.environ.get(k)
                os.environ.pop(k, None)
            try:
                result = self.mod.build_bundle(
                    pipeline_output_path=str(report_path),
                    output_root=Path(tmpdir) / "bundles",
                )
                self.assertEqual(result["status"], "BUNDLED")
                self.assertEqual(result["verdict"], "PASS")
                self.assertEqual(result["gate_status"], "APPROVED_PAPER")
                self.assertFalse(result["live_trade"])
            finally:
                for k, v in saved.items():
                    if v is None:
                        os.environ.pop(k, None)
                    else:
                        os.environ[k] = v

    def test_build_bundle_live_trade_refused(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bad = self._good_report()
            bad["e2e_post_gate_status"]["live_trade"] = True
            report_path = Path(tmpdir) / "bad_report.json"
            report_path.write_text(json.dumps(bad), encoding="utf-8")

            saved = {}
            for k, v in {"ALLOW_E2E_LIVE_DRY_RUN": "1", "DRY_RUN": "1"}.items():
                saved[k] = os.environ.get(k)
                os.environ[k] = v
            for k in ["ALLOW_LIVE_TRADE", "ALLOW_GOOGLE_SHEETS_API_WRITE", "ALLOW_TELEGRAM_SEND"]:
                saved[k] = os.environ.get(k)
                os.environ.pop(k, None)
            try:
                result = self.mod.build_bundle(
                    pipeline_output_path=str(report_path),
                    output_root=Path(tmpdir) / "bundles",
                )
                self.assertEqual(result["status"], "REFUSED")
                self.assertIn("live_trade", result["reason"])
            finally:
                for k, v in saved.items():
                    if v is None:
                        os.environ.pop(k, None)
                    else:
                        os.environ[k] = v

    def test_build_bundle_wrong_gate_status_refused(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bad = self._good_report()
            bad["e2e_post_gate_status"]["gate_status"] = "REJECTED"
            report_path = Path(tmpdir) / "bad_report.json"
            report_path.write_text(json.dumps(bad), encoding="utf-8")

            saved = {}
            for k, v in {"ALLOW_E2E_LIVE_DRY_RUN": "1", "DRY_RUN": "1"}.items():
                saved[k] = os.environ.get(k)
                os.environ[k] = v
            for k in ["ALLOW_LIVE_TRADE", "ALLOW_GOOGLE_SHEETS_API_WRITE", "ALLOW_TELEGRAM_SEND"]:
                saved[k] = os.environ.get(k)
                os.environ.pop(k, None)
            try:
                result = self.mod.build_bundle(
                    pipeline_output_path=str(report_path),
                    output_root=Path(tmpdir) / "bundles",
                )
                self.assertEqual(result["status"], "REFUSED")
                self.assertIn("gate_status", result["reason"])
            finally:
                for k, v in saved.items():
                    if v is None:
                        os.environ.pop(k, None)
                    else:
                        os.environ[k] = v


# ── Subprocess tests — CLI ────────────────────────────────────────────────────

class TestCLIEnvRefused(unittest.TestCase):
    """Fast subprocess tests — verify CLI exits 1 on bad env."""

    def test_no_allow_e2e_flag_exits_1(self):
        data, stderr, rc = _run_bundle(drop=["ALLOW_E2E_LIVE_DRY_RUN"], timeout=10)
        self.assertEqual(rc, 1, f"Expected exit 1, got {rc}. stdout={data}")
        self.assertEqual(data.get("status"), "REFUSED")

    def test_no_dry_run_flag_exits_1(self):
        data, stderr, rc = _run_bundle(drop=["DRY_RUN"], timeout=10)
        self.assertEqual(rc, 1, f"Expected exit 1, got {rc}. stdout={data}")
        self.assertEqual(data.get("status"), "REFUSED")

    def test_allow_live_trade_exits_1(self):
        data, stderr, rc = _run_bundle(extra={"ALLOW_LIVE_TRADE": "1"}, timeout=10)
        self.assertEqual(rc, 1)
        self.assertEqual(data.get("status"), "REFUSED")
        self.assertIn("ALLOW_LIVE_TRADE", data.get("reason", ""))

    def test_allow_sheets_write_exits_1(self):
        data, stderr, rc = _run_bundle(extra={"ALLOW_GOOGLE_SHEETS_API_WRITE": "1"}, timeout=10)
        self.assertEqual(rc, 1)
        self.assertEqual(data.get("status"), "REFUSED")

    def test_allow_telegram_send_exits_1(self):
        data, stderr, rc = _run_bundle(extra={"ALLOW_TELEGRAM_SEND": "1"}, timeout=10)
        self.assertEqual(rc, 1)
        self.assertEqual(data.get("status"), "REFUSED")


# ── Integration test — full pipeline + bundle via subprocess ──────────────────

class TestBundleIntegration(unittest.TestCase):
    """Full pipeline run + bundle. Expensive — setUpClass runs once."""

    _result: dict = {}
    _bundle_dir: Path | None = None
    _tmpdir_obj = None

    @classmethod
    def setUpClass(cls):
        cls._tmpdir_obj = tempfile.TemporaryDirectory()
        tmpdir = cls._tmpdir_obj.name
        data, stderr, rc = _run_bundle(
            extra_args=["--output-root", tmpdir, "--run-id", "integration_test_run"],
            timeout=90,
        )
        cls._result = data
        cls._rc = rc
        if data.get("bundle_dir"):
            cls._bundle_dir = Path(data["bundle_dir"])

    @classmethod
    def tearDownClass(cls):
        if cls._tmpdir_obj:
            cls._tmpdir_obj.cleanup()

    def test_script_exits_0(self):
        self.assertEqual(self._rc, 0, f"Expected exit 0, got {self._rc}. result={self._result}")

    def test_result_status_bundled(self):
        self.assertEqual(self._result.get("status"), "BUNDLED")

    def test_result_verdict_pass(self):
        self.assertEqual(self._result.get("verdict"), "PASS")

    def test_result_gate_status_approved_paper(self):
        self.assertEqual(self._result.get("gate_status"), "APPROVED_PAPER")

    def test_result_live_trade_false(self):
        self.assertFalse(self._result.get("live_trade"))

    def test_result_dry_run_true(self):
        self.assertIs(self._result.get("dry_run"), True)

    def test_result_run_id_present(self):
        self.assertIsNotNone(self._result.get("run_id"))

    def test_result_bundle_dir_present(self):
        self.assertIsNotNone(self._result.get("bundle_dir"))

    def test_bundle_dir_exists(self):
        if self._bundle_dir is None:
            self.skipTest("bundle_dir not set (script may have failed)")
        self.assertTrue(self._bundle_dir.exists(), f"Bundle dir not found: {self._bundle_dir}")

    def test_manifest_json_present(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        self.assertTrue((self._bundle_dir / "manifest.json").exists())

    def test_e2e_report_json_present(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        self.assertTrue((self._bundle_dir / "e2e_report.json").exists())

    def test_environment_flags_json_present(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        self.assertTrue((self._bundle_dir / "environment_flags.json").exists())

    def test_payload_refs_json_present(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        self.assertTrue((self._bundle_dir / "payload_refs.json").exists())

    def test_summary_md_present(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        self.assertTrue((self._bundle_dir / "summary.md").exists())

    def test_manifest_go_id(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        manifest = json.loads((self._bundle_dir / "manifest.json").read_text())
        self.assertIn("GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01",
                      manifest["go_id"])

    def test_manifest_pf_id(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        manifest = json.loads((self._bundle_dir / "manifest.json").read_text())
        self.assertEqual(manifest["pf_id"], "PF_OPENCLAW_ORCHESTRATOR_FULL")

    def test_manifest_7_modules(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        manifest = json.loads((self._bundle_dir / "manifest.json").read_text())
        self.assertEqual(len(manifest["modules"]), 7)

    def test_result_7_modules(self):
        modules = self._result.get("modules", {})
        self.assertEqual(len(modules), 7)

    def test_payload_refs_has_signal(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        refs = json.loads((self._bundle_dir / "payload_refs.json").read_text())
        self.assertIn("signal", refs)
        self.assertIn("trade", refs)
        self.assertIn("result", refs)

    def test_summary_md_contains_verdict(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        md = (self._bundle_dir / "summary.md").read_text()
        self.assertIn("PASS", md)

    def test_summary_md_contains_approved_paper(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        md = (self._bundle_dir / "summary.md").read_text()
        self.assertIn("APPROVED_PAPER", md)

    def test_no_secrets_in_bundle_dir(self):
        if not self._bundle_dir:
            self.skipTest("bundle_dir not set")
        all_text = ""
        for f in self._bundle_dir.iterdir():
            all_text += f.read_text(encoding="utf-8", errors="ignore")
        for secret in ["TELEGRAM_BOT_TOKEN", "TV_WEBHOOK_KEY", "OPS_ADMIN_KEY"]:
            self.assertNotIn(secret, all_text, f"Secret key {secret} found in bundle")


if __name__ == "__main__":
    unittest.main(verbosity=2)
