import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = PROJECT_ROOT / "scripts" / "validate_runtime_execution_contracts.py"
REGISTRY_PATH = PROJECT_ROOT / "registry" / "runtime_execution_contracts.yaml"


def test_tool_exists():
    assert TOOL_PATH.exists()


def test_registry_exists():
    assert REGISTRY_PATH.exists()


def test_tool_runs_clean():
    result = subprocess.run(
        [sys.executable, str(TOOL_PATH)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr


def test_output_contains_pass_marker():
    result = subprocess.run(
        [sys.executable, str(TOOL_PATH)],
        capture_output=True,
        text=True,
    )
    assert "[PASS] runtime_execution_contracts registry validation" in result.stdout
