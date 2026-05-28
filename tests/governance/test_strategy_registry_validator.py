"""Tests for validate_strategy_registry.py — A05 test lock."""
import subprocess
import sys
from pathlib import Path

TOOL_PATH = Path(__file__).resolve().parents[2] / "tools" / "strategy" / "validate_strategy_registry.py"
REGISTRY_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "chantiers"
    / "GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01"
    / "95_STRATEGY_REGISTRY.md"
)


def test_tool_exists():
    assert TOOL_PATH.exists()


def test_registry_exists():
    assert REGISTRY_PATH.exists()


def test_tool_runs_without_crash():
    result = subprocess.run(
        [sys.executable, str(TOOL_PATH)],
        capture_output=True,
        text=True,
    )
    # WARNING_ONLY mode — exit 0 (clean) or 1 (warnings), never crash
    assert result.returncode in (0, 1)


def test_output_contains_summary():
    result = subprocess.run(
        [sys.executable, str(TOOL_PATH)],
        capture_output=True,
        text=True,
    )
    assert "=== Summary ===" in result.stdout


def test_output_contains_registered_count():
    result = subprocess.run(
        [sys.executable, str(TOOL_PATH)],
        capture_output=True,
        text=True,
    )
    assert "REGISTERED:" in result.stdout
