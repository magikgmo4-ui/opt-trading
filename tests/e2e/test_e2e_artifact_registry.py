"""
Tests for scripts/e2e/register_e2e_bundle.py

Coverage:
  - manifest validation (dry_run, live_trade, gate_status, run_id, go_id)
  - duplicate detection
  - entry building (all fields present, hashes computed)
  - registry write (JSONL append, parseable, deduplication)
  - registry list
  - CLI subprocess (register command, list command, refused cases)
  - integration: full bundle + register via subprocess
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
_REG_SCRIPT = REPO_ROOT / "scripts" / "e2e" / "register_e2e_bundle.py"
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

def _env(**overrides):
    env = {**_BASE_ENV}
    env.update(overrides)
    return {k: v for k, v in env.items() if v != ""}


def _run_register(bundle_dir: str, registry: str, timeout: int = 15) -> tuple[dict, str, int]:
    cmd = [sys.executable, str(_REG_SCRIPT), "register",
           "--bundle-dir", bundle_dir, "--registry", registry]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                            cwd=str(REPO_ROOT), env=_env())
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        data = {}
    return data, result.stderr, result.returncode


def _run_list(registry: str, timeout: int = 5) -> tuple[list, str, int]:
    cmd = [sys.executable, str(_REG_SCRIPT), "list", "--registry", registry]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                            cwd=str(REPO_ROOT), env=_env())
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        data = []
    return data, result.stderr, result.returncode


def _good_manifest(run_id: str = "test_run_001") -> dict:
    return {
        "bundle_version": "1.0",
        "run_id": run_id,
        "go_id": "GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01",
        "pf_id": "PF_OPENCLAW_ORCHESTRATOR_FULL",
        "parent_go": "GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01",
        "created_at": "2026-05-26T12:00:00+00:00",
        "pipeline_started_at": "2026-05-26T12:00:00+00:00",
        "pipeline_completed_at": "2026-05-26T12:00:05+00:00",
        "duration_s": 5.0,
        "verdict": "PASS",
        "gate_status": "APPROVED_PAPER",
        "dry_run": True,
        "live_trade": False,
        "sheets_mode": "fake",
        "telegram_mode": "dry_run",
        "localcms_gate": "WARN_SKIPPED",
        "modules": {m: "PASS" for m in [
            "signal_router", "proposition_engine", "validation_gate",
            "trade_executor", "result_tracker", "datasheet_writer", "learning_feeder",
        ]},
    }


def _make_bundle_dir(tmpdir: Path, run_id: str = "test_run_001",
                     manifest_overrides: dict | None = None) -> Path:
    bundle_dir = tmpdir / run_id
    bundle_dir.mkdir(parents=True, exist_ok=True)
    manifest = _good_manifest(run_id)
    if manifest_overrides:
        manifest.update(manifest_overrides)
    (bundle_dir / "manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    (bundle_dir / "summary.md").write_text(
        f"# E2E Bundle\n\nRun: {run_id}\nVerdict: PASS\n", encoding="utf-8"
    )
    (bundle_dir / "e2e_report.json").write_text("{}", encoding="utf-8")
    (bundle_dir / "environment_flags.json").write_text("{}", encoding="utf-8")
    (bundle_dir / "payload_refs.json").write_text("{}", encoding="utf-8")
    return bundle_dir


# ── Unit tests — module import ────────────────────────────────────────────────

class TestModuleImport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import scripts.e2e.register_e2e_bundle as mod
        cls.mod = mod

    def test_registry_refused_is_exception(self):
        self.assertTrue(issubclass(self.mod.RegistryRefused, Exception))

    def test_default_registry_path_in_artifacts(self):
        self.assertIn("artifacts", str(self.mod.DEFAULT_REGISTRY))
        self.assertIn("e2e_artifact_registry", str(self.mod.DEFAULT_REGISTRY))
        self.assertTrue(str(self.mod.DEFAULT_REGISTRY).endswith(".jsonl"))


# ── Unit tests — _validate_manifest ──────────────────────────────────────────

class TestValidateManifest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import scripts.e2e.register_e2e_bundle as mod
        cls.mod = mod

    def test_valid_manifest_passes(self):
        self.mod._validate_manifest(_good_manifest())

    def test_dry_run_false_raises(self):
        m = _good_manifest()
        m["dry_run"] = False
        with self.assertRaises(self.mod.RegistryRefused) as ctx:
            self.mod._validate_manifest(m)
        self.assertIn("dry_run", str(ctx.exception))

    def test_dry_run_none_raises(self):
        m = _good_manifest()
        m["dry_run"] = None
        with self.assertRaises(self.mod.RegistryRefused):
            self.mod._validate_manifest(m)

    def test_live_trade_true_raises(self):
        m = _good_manifest()
        m["live_trade"] = True
        with self.assertRaises(self.mod.RegistryRefused) as ctx:
            self.mod._validate_manifest(m)
        self.assertIn("live_trade", str(ctx.exception))

    def test_wrong_gate_status_raises(self):
        m = _good_manifest()
        m["gate_status"] = "REJECTED"
        with self.assertRaises(self.mod.RegistryRefused) as ctx:
            self.mod._validate_manifest(m)
        self.assertIn("gate_status", str(ctx.exception))

    def test_none_gate_status_raises(self):
        m = _good_manifest()
        m["gate_status"] = None
        with self.assertRaises(self.mod.RegistryRefused):
            self.mod._validate_manifest(m)

    def test_missing_run_id_raises(self):
        m = _good_manifest()
        del m["run_id"]
        with self.assertRaises(self.mod.RegistryRefused) as ctx:
            self.mod._validate_manifest(m)
        self.assertIn("run_id", str(ctx.exception))

    def test_empty_run_id_raises(self):
        m = _good_manifest()
        m["run_id"] = ""
        with self.assertRaises(self.mod.RegistryRefused):
            self.mod._validate_manifest(m)

    def test_missing_go_id_raises(self):
        m = _good_manifest()
        del m["go_id"]
        with self.assertRaises(self.mod.RegistryRefused) as ctx:
            self.mod._validate_manifest(m)
        self.assertIn("go_id", str(ctx.exception))


# ── Unit tests — duplicate detection ─────────────────────────────────────────

class TestDuplicateDetection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import scripts.e2e.register_e2e_bundle as mod
        cls.mod = mod

    def test_no_registry_no_duplicate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = Path(tmpdir) / "reg.jsonl"
            self.mod._check_duplicate("new_run_001", registry)

    def test_empty_registry_no_duplicate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = Path(tmpdir) / "reg.jsonl"
            registry.write_text("", encoding="utf-8")
            self.mod._check_duplicate("new_run_001", registry)

    def test_existing_run_id_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = Path(tmpdir) / "reg.jsonl"
            registry.write_text(
                json.dumps({"run_id": "existing_run"}) + "\n", encoding="utf-8"
            )
            with self.assertRaises(self.mod.RegistryRefused) as ctx:
                self.mod._check_duplicate("existing_run", registry)
            self.assertIn("already registered", str(ctx.exception))

    def test_different_run_id_no_duplicate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = Path(tmpdir) / "reg.jsonl"
            registry.write_text(
                json.dumps({"run_id": "existing_run"}) + "\n", encoding="utf-8"
            )
            self.mod._check_duplicate("different_run", registry)

    def test_malformed_lines_skipped(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = Path(tmpdir) / "reg.jsonl"
            registry.write_text("not json\n{invalid}\n", encoding="utf-8")
            self.mod._check_duplicate("new_run", registry)


# ── Unit tests — hash computation ────────────────────────────────────────────

class TestHashComputation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import scripts.e2e.register_e2e_bundle as mod
        cls.mod = mod

    def test_hash_starts_with_sha256(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            f.write(b'{"test": true}')
            path = Path(f.name)
        try:
            h = self.mod._sha256_file(path)
            self.assertTrue(h.startswith("sha256:"))
        finally:
            path.unlink()

    def test_hash_deterministic(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            f.write(b'{"test": true}')
            path = Path(f.name)
        try:
            h1 = self.mod._sha256_file(path)
            h2 = self.mod._sha256_file(path)
            self.assertEqual(h1, h2)
        finally:
            path.unlink()

    def test_different_content_different_hash(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p1 = Path(tmpdir) / "a.json"
            p2 = Path(tmpdir) / "b.json"
            p1.write_bytes(b'{"a": 1}')
            p2.write_bytes(b'{"b": 2}')
            self.assertNotEqual(self.mod._sha256_file(p1), self.mod._sha256_file(p2))


# ── Unit tests — entry building ───────────────────────────────────────────────

class TestBuildEntry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import scripts.e2e.register_e2e_bundle as mod
        cls.mod = mod

    def test_entry_has_all_required_fields(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            manifest = _good_manifest()
            registry = Path(tmpdir) / "reg.jsonl"
            entry = self.mod._build_entry(bundle_dir, manifest, registry)
            for field in ["run_id", "created_at", "registered_at", "verdict",
                           "e2e_status", "gate_status", "dry_run", "live_trade",
                           "go_id", "pf_id", "bundle_path", "manifest_hash",
                           "summary_hash", "git_sha", "modules"]:
                self.assertIn(field, entry, f"Missing field: {field}")

    def test_entry_dry_run_true(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            entry = self.mod._build_entry(bundle_dir, _good_manifest(), Path(tmpdir) / "r.jsonl")
            self.assertIs(entry["dry_run"], True)

    def test_entry_live_trade_false(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            entry = self.mod._build_entry(bundle_dir, _good_manifest(), Path(tmpdir) / "r.jsonl")
            self.assertIs(entry["live_trade"], False)

    def test_entry_gate_status_approved_paper(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            entry = self.mod._build_entry(bundle_dir, _good_manifest(), Path(tmpdir) / "r.jsonl")
            self.assertEqual(entry["gate_status"], "APPROVED_PAPER")

    def test_entry_manifest_hash_present(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            entry = self.mod._build_entry(bundle_dir, _good_manifest(), Path(tmpdir) / "r.jsonl")
            self.assertTrue(entry["manifest_hash"].startswith("sha256:"))

    def test_entry_summary_hash_present(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            entry = self.mod._build_entry(bundle_dir, _good_manifest(), Path(tmpdir) / "r.jsonl")
            self.assertIsNotNone(entry["summary_hash"])
            self.assertTrue(entry["summary_hash"].startswith("sha256:"))

    def test_entry_bundle_path_is_absolute(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            entry = self.mod._build_entry(bundle_dir, _good_manifest(), Path(tmpdir) / "r.jsonl")
            self.assertTrue(Path(entry["bundle_path"]).is_absolute())

    def test_entry_7_modules(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            entry = self.mod._build_entry(bundle_dir, _good_manifest(), Path(tmpdir) / "r.jsonl")
            self.assertEqual(len(entry["modules"]), 7)

    def test_entry_registry_version(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            entry = self.mod._build_entry(bundle_dir, _good_manifest(), Path(tmpdir) / "r.jsonl")
            self.assertEqual(entry["registry_version"], "1.0")


# ── Unit tests — register_bundle ─────────────────────────────────────────────

class TestRegisterBundle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import scripts.e2e.register_e2e_bundle as mod
        cls.mod = mod

    def test_register_returns_registered_status(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = Path(tmpdir) / "reg.jsonl"
            result = self.mod.register_bundle(bundle_dir, registry)
            self.assertEqual(result["status"], "REGISTERED")

    def test_register_creates_registry_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = Path(tmpdir) / "reg.jsonl"
            self.mod.register_bundle(bundle_dir, registry)
            self.assertTrue(registry.exists())

    def test_register_appends_one_line(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = Path(tmpdir) / "reg.jsonl"
            self.mod.register_bundle(bundle_dir, registry)
            lines = [l for l in registry.read_text().splitlines() if l.strip()]
            self.assertEqual(len(lines), 1)

    def test_register_line_is_valid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = Path(tmpdir) / "reg.jsonl"
            self.mod.register_bundle(bundle_dir, registry)
            entry = json.loads(registry.read_text().strip())
            self.assertEqual(entry["run_id"], "test_run_001")

    def test_register_result_run_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = Path(tmpdir) / "reg.jsonl"
            result = self.mod.register_bundle(bundle_dir, registry)
            self.assertEqual(result["run_id"], "test_run_001")

    def test_register_result_verdict(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = Path(tmpdir) / "reg.jsonl"
            result = self.mod.register_bundle(bundle_dir, registry)
            self.assertEqual(result["verdict"], "PASS")

    def test_register_result_manifest_hash(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = Path(tmpdir) / "reg.jsonl"
            result = self.mod.register_bundle(bundle_dir, registry)
            self.assertTrue(result["manifest_hash"].startswith("sha256:"))

    def test_register_two_bundles_appends_two_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            b1 = _make_bundle_dir(Path(tmpdir), run_id="run_001")
            b2 = _make_bundle_dir(Path(tmpdir), run_id="run_002")
            registry = Path(tmpdir) / "reg.jsonl"
            self.mod.register_bundle(b1, registry)
            self.mod.register_bundle(b2, registry)
            lines = [l for l in registry.read_text().splitlines() if l.strip()]
            self.assertEqual(len(lines), 2)

    def test_register_duplicate_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = Path(tmpdir) / "reg.jsonl"
            self.mod.register_bundle(bundle_dir, registry)
            with self.assertRaises(self.mod.RegistryRefused) as ctx:
                self.mod.register_bundle(bundle_dir, registry)
            self.assertIn("already registered", str(ctx.exception))

    def test_register_missing_bundle_dir_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = Path(tmpdir) / "reg.jsonl"
            with self.assertRaises(self.mod.RegistryRefused) as ctx:
                self.mod.register_bundle(Path(tmpdir) / "nonexistent", registry)
            self.assertIn("does not exist", str(ctx.exception))

    def test_register_missing_manifest_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = Path(tmpdir) / "empty_bundle"
            bundle_dir.mkdir()
            registry = Path(tmpdir) / "reg.jsonl"
            with self.assertRaises(self.mod.RegistryRefused) as ctx:
                self.mod.register_bundle(bundle_dir, registry)
            self.assertIn("manifest.json", str(ctx.exception))

    def test_register_live_trade_true_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir), manifest_overrides={"live_trade": True})
            registry = Path(tmpdir) / "reg.jsonl"
            with self.assertRaises(self.mod.RegistryRefused):
                self.mod.register_bundle(bundle_dir, registry)

    def test_register_wrong_gate_status_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir), manifest_overrides={"gate_status": "REJECTED"})
            registry = Path(tmpdir) / "reg.jsonl"
            with self.assertRaises(self.mod.RegistryRefused):
                self.mod.register_bundle(bundle_dir, registry)


# ── Unit tests — list_registry ────────────────────────────────────────────────

class TestListRegistry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(REPO_ROOT))
        import scripts.e2e.register_e2e_bundle as mod
        cls.mod = mod

    def test_list_empty_registry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.mod.list_registry(Path(tmpdir) / "nonexistent.jsonl")
            self.assertEqual(result, [])

    def test_list_after_register(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = Path(tmpdir) / "reg.jsonl"
            self.mod.register_bundle(bundle_dir, registry)
            entries = self.mod.list_registry(registry)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["run_id"], "test_run_001")

    def test_list_two_entries(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            b1 = _make_bundle_dir(Path(tmpdir), run_id="run_001")
            b2 = _make_bundle_dir(Path(tmpdir), run_id="run_002")
            registry = Path(tmpdir) / "reg.jsonl"
            self.mod.register_bundle(b1, registry)
            self.mod.register_bundle(b2, registry)
            entries = self.mod.list_registry(registry)
            self.assertEqual(len(entries), 2)
            run_ids = {e["run_id"] for e in entries}
            self.assertEqual(run_ids, {"run_001", "run_002"})


# ── Subprocess tests — CLI ────────────────────────────────────────────────────

class TestCLIRegister(unittest.TestCase):

    def test_register_exits_0(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = str(Path(tmpdir) / "reg.jsonl")
            data, stderr, rc = _run_register(str(bundle_dir), registry)
            self.assertEqual(rc, 0, f"rc={rc}, stderr={stderr}")
            self.assertEqual(data.get("status"), "REGISTERED")

    def test_register_result_has_run_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = str(Path(tmpdir) / "reg.jsonl")
            data, _, rc = _run_register(str(bundle_dir), registry)
            self.assertEqual(rc, 0)
            self.assertIsNotNone(data.get("run_id"))

    def test_register_nonexistent_dir_exits_1(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = str(Path(tmpdir) / "reg.jsonl")
            data, _, rc = _run_register("/nonexistent/bundle", registry)
            self.assertEqual(rc, 1)
            self.assertEqual(data.get("status"), "REFUSED")

    def test_register_duplicate_exits_1(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = str(Path(tmpdir) / "reg.jsonl")
            _run_register(str(bundle_dir), registry)
            data, _, rc = _run_register(str(bundle_dir), registry)
            self.assertEqual(rc, 1)
            self.assertEqual(data.get("status"), "REFUSED")
            self.assertIn("already registered", data.get("reason", ""))

    def test_list_empty_registry_exits_0(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = str(Path(tmpdir) / "reg.jsonl")
            entries, _, rc = _run_list(registry)
            self.assertEqual(rc, 0)
            self.assertEqual(entries, [])

    def test_list_after_register_shows_entry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = _make_bundle_dir(Path(tmpdir))
            registry = str(Path(tmpdir) / "reg.jsonl")
            _run_register(str(bundle_dir), registry)
            entries, _, rc = _run_list(registry)
            self.assertEqual(rc, 0)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["run_id"], "test_run_001")


# ── Integration test — build bundle + register ────────────────────────────────

class TestBuildAndRegisterIntegration(unittest.TestCase):
    """Full pipeline: build bundle then register it. setUpClass runs once."""

    _bundle_result: dict = {}
    _reg_result: dict = {}
    _bundle_dir_path: Path | None = None
    _registry_path: Path | None = None
    _tmpdir_obj = None

    @classmethod
    def setUpClass(cls):
        cls._tmpdir_obj = tempfile.TemporaryDirectory()
        tmpdir = cls._tmpdir_obj.name
        bundle_output = str(Path(tmpdir) / "bundles")
        registry_file = str(Path(tmpdir) / "reg.jsonl")
        run_id = "integ_reg_test"

        env = {k: v for k, v in _env().items()}
        # Step 1: build bundle
        build_result = subprocess.run(
            [sys.executable, str(_BUNDLE_SCRIPT),
             "--output-root", bundle_output, "--run-id", run_id],
            capture_output=True, text=True, timeout=90,
            cwd=str(REPO_ROOT), env=env,
        )
        try:
            cls._bundle_result = json.loads(build_result.stdout)
        except json.JSONDecodeError:
            cls._bundle_result = {}
        cls._build_rc = build_result.returncode

        # Step 2: register bundle
        if cls._bundle_result.get("bundle_dir"):
            cls._bundle_dir_path = Path(cls._bundle_result["bundle_dir"])
            cls._registry_path = Path(registry_file)
            reg_result = subprocess.run(
                [sys.executable, str(_REG_SCRIPT), "register",
                 "--bundle-dir", str(cls._bundle_dir_path),
                 "--registry", registry_file],
                capture_output=True, text=True, timeout=15,
                cwd=str(REPO_ROOT), env=env,
            )
            try:
                cls._reg_result = json.loads(reg_result.stdout)
            except json.JSONDecodeError:
                cls._reg_result = {}
            cls._reg_rc = reg_result.returncode
        else:
            cls._reg_rc = -1

    @classmethod
    def tearDownClass(cls):
        if cls._tmpdir_obj:
            cls._tmpdir_obj.cleanup()

    def test_bundle_built_successfully(self):
        self.assertEqual(self._build_rc, 0, f"Bundle build failed: {self._bundle_result}")
        self.assertEqual(self._bundle_result.get("status"), "BUNDLED")

    def test_register_exits_0(self):
        self.assertEqual(self._reg_rc, 0, f"Register failed: {self._reg_result}")

    def test_register_status_registered(self):
        self.assertEqual(self._reg_result.get("status"), "REGISTERED")

    def test_register_run_id_matches(self):
        self.assertEqual(self._reg_result.get("run_id"), "integ_reg_test")

    def test_register_manifest_hash_present(self):
        self.assertIsNotNone(self._reg_result.get("manifest_hash"))
        self.assertTrue(self._reg_result["manifest_hash"].startswith("sha256:"))

    def test_register_verdict_pass(self):
        self.assertEqual(self._reg_result.get("verdict"), "PASS")

    def test_register_gate_status_approved_paper(self):
        self.assertEqual(self._reg_result.get("gate_status"), "APPROVED_PAPER")

    def test_registry_file_exists(self):
        if self._registry_path is None:
            self.skipTest("registry_path not set")
        self.assertTrue(self._registry_path.exists())

    def test_registry_has_one_entry(self):
        if self._registry_path is None:
            self.skipTest("registry_path not set")
        lines = [l for l in self._registry_path.read_text().splitlines() if l.strip()]
        self.assertEqual(len(lines), 1)

    def test_registry_entry_parseable(self):
        if self._registry_path is None:
            self.skipTest("registry_path not set")
        entry = json.loads(self._registry_path.read_text().strip())
        self.assertEqual(entry["run_id"], "integ_reg_test")
        self.assertIs(entry["dry_run"], True)
        self.assertIs(entry["live_trade"], False)

    def test_registry_entry_7_modules(self):
        if self._registry_path is None:
            self.skipTest("registry_path not set")
        entry = json.loads(self._registry_path.read_text().strip())
        self.assertEqual(len(entry.get("modules", {})), 7)

    def test_list_command_returns_entry(self):
        if self._registry_path is None:
            self.skipTest("registry_path not set")
        entries, _, rc = _run_list(str(self._registry_path))
        self.assertEqual(rc, 0)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["run_id"], "integ_reg_test")

    def test_duplicate_register_refused(self):
        if self._registry_path is None or self._bundle_dir_path is None:
            self.skipTest("prerequisites not set")
        data, _, rc = _run_register(
            str(self._bundle_dir_path), str(self._registry_path)
        )
        self.assertEqual(rc, 1)
        self.assertEqual(data.get("status"), "REFUSED")
        self.assertIn("already registered", data.get("reason", ""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
