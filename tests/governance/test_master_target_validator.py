"""Tests for validate_master_target_continuity.py"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOL_PATH = Path(__file__).resolve().parents[2] / "tools" / "governance" / "validate_master_target_continuity.py"
REPO_ROOT = Path(__file__).resolve().parents[2]


def test_tool_runs_without_error():
    """Smoke: tool exits 0 (warning-only)."""
    result = subprocess.run(
        [sys.executable, str(TOOL_PATH)],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"


def test_registry_loaded():
    """Check the registry is parsed into expected known targets."""
    from tools.governance.validate_master_target_continuity import load_registry, REGISTRY_PATH

    assert REGISTRY_PATH.exists()
    reg = load_registry(REGISTRY_PATH)
    required = {
        "MT_SIGNAL_CHAIN_PRODUCT",
        "MT_STRICT_WORKERS_RUNNER",
        "MT_DCA_ON_FEAR",
        "MT_STRATEGY_FRAMEWORK",
        "MT_DESKPRO_UI",
        "MT_PRODUCT_GOVERNANCE",
    }
    for mt in required:
        assert mt in reg, f"Missing registered target: {mt}"
    for mt, info in reg.items():
        assert info["status"] in ("ACTIVE", "RETIRED"), f"Unexpected status for {mt}"
        assert info["first_go"], f"Missing first_go for {mt}"
        assert info["current_go"], f"Missing current_go for {mt}"


def test_no_duplicate_ids_in_chantiers():
    """No two chantier files share the same master_target_id."""
    from tools.governance.validate_master_target_continuity import scan_chantiers, CHANTIERS_DIR

    findings = scan_chantiers(CHANTIERS_DIR)
    mt_ids = [c["master_target_id"] for c in findings if c["master_target_id"]]
    duplicates = {id_ for id_ in mt_ids if mt_ids.count(id_) > 1}
    assert not duplicates, f"Duplicate master_target_id in chantiers: {duplicates}"


def test_output_contains_warning_or_clean(capsys):
    """Console output mentions WARNINGS or CLEAN."""
    from tools.governance.validate_master_target_continuity import main
    main()
    captured = capsys.readouterr()
    assert "WARNINGS" in captured.out or "CLEAN" in captured.out
