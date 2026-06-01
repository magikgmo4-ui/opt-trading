from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
HEADLESS_REL = Path("modules/bot_vision/headless_capture")


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _prepare_source_tree(root: Path) -> None:
    base = root / HEADLESS_REL
    _write(base / "capture_headless.js", "capture-v2\n")
    _write(base / "README.md", "readme\n")
    _write(base / "package.json", "{}\n")
    _write(base / "capture_map.json", "{}\n")
    _write(base / "screen_types.json", "{}\n")
    _write(base / "trigger_config.json", "{}\n")
    _write(base / "profiles.production.json", "[]\n")
    _write(base / "scripts/run_vision_pipeline.py", "print('pipeline')\n")
    _write(base / "scripts/run_orchestrator.sh", "#!/bin/bash\n")
    _write(base / "systemd/bot-vision-orchestrator.service", "[Unit]\n")


def test_runtime_stabilize_plan_reports_items(tmp_path):
    source = tmp_path / "source"
    runtime = tmp_path / "runtime"
    backup = tmp_path / "backup"
    _prepare_source_tree(source)

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_admin_trading_runtime_stabilize.py"),
            "--source-root",
            str(source),
            "--runtime-root",
            str(runtime),
            "--backup-root",
            str(backup),
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    report = json.loads(result.stdout)
    assert report["headless_source"].endswith(str(HEADLESS_REL))
    assert report["headless_runtime"].endswith(str(HEADLESS_REL))
    rels = {item["relative"] for item in report["runtime_items"]}
    assert "capture_headless.js" in rels
    assert "scripts" in rels
    assert report["systemd_plan"]["enable_timer"] == "bot-vision-orchestrator.timer"


def test_runtime_stabilize_apply_copies_and_backs_up(tmp_path):
    source = tmp_path / "source"
    runtime = tmp_path / "runtime"
    backup = tmp_path / "backup"
    _prepare_source_tree(source)

    runtime_base = runtime / HEADLESS_REL
    _write(runtime_base / "capture_headless.js", "old-capture\n")
    _write(runtime_base / "scripts/run_vision_pipeline.py", "old-pipeline\n")

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_admin_trading_runtime_stabilize.py"),
            "--source-root",
            str(source),
            "--runtime-root",
            str(runtime),
            "--backup-root",
            str(backup),
            "--apply",
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    report = json.loads(result.stdout)
    assert report["applied"] is True
    assert "capture_headless.js" in report["copied"]
    assert "capture_headless.js" in report["backed_up"]
    assert (runtime_base / "capture_headless.js").read_text(encoding="utf-8") == "capture-v2\n"
    backup_dir = Path(report["backup_dir"])
    assert (backup_dir / "capture_headless.js").exists()
