from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=str(cwd), text=True, capture_output=True, check=True)


def _init_source_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    _run(["git", "init", "-b", "sot/mainline"], cwd=path)
    _run(["git", "config", "user.email", "test@example.com"], cwd=path)
    _run(["git", "config", "user.name", "Test User"], cwd=path)
    (path / "README.md").write_text("hello\n", encoding="utf-8")
    _run(["git", "add", "README.md"], cwd=path)
    _run(["git", "commit", "-m", "init"], cwd=path)


def test_canonical_checkout_script_clones_clean_repo(tmp_path):
    source = tmp_path / "source"
    target = tmp_path / "target"
    _init_source_repo(source)

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_admin_trading_canonical_checkout.py"),
            "--source",
            str(source),
            "--target",
            str(target),
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    report = json.loads(result.stdout)
    assert report["action"] == "cloned"
    assert report["branch"] == "sot/mainline"
    assert report["clean"] is True
    assert (target / "README.md").exists()


def test_canonical_checkout_script_resets_dirty_repo(tmp_path):
    source = tmp_path / "source"
    target = tmp_path / "target"
    _init_source_repo(source)

    script = PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_admin_trading_canonical_checkout.py"
    subprocess.run(
        [sys.executable, str(script), "--source", str(source), "--target", str(target)],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )

    (target / "README.md").write_text("dirty\n", encoding="utf-8")
    (target / "UNTRACKED.txt").write_text("x\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(script), "--source", str(source), "--target", str(target)],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    report = json.loads(result.stdout)
    assert report["action"] == "updated"
    assert report["clean"] is True
    assert (target / "README.md").read_text(encoding="utf-8") == "hello\n"
    assert not (target / "UNTRACKED.txt").exists()
