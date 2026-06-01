#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=str(cwd) if cwd else None, text=True, capture_output=True, check=True)


def _git_output(repo: Path, *args: str) -> str:
    result = _run(["git", *args], cwd=repo)
    return result.stdout.strip()


def ensure_canonical_checkout(source: str, target: Path, branch: str) -> dict[str, object]:
    target_parent = target.parent
    target_parent.mkdir(parents=True, exist_ok=True)

    action = "updated"
    if not (target / ".git").exists():
        if target.exists() and any(target.iterdir()):
            raise RuntimeError(f"Target exists and is not an empty git checkout: {target}")
        if target.exists() and not any(target.iterdir()):
            target.rmdir()
        _run(["git", "clone", "--branch", branch, "--single-branch", source, str(target)])
        action = "cloned"
    else:
        _run(["git", "remote", "set-url", "origin", source], cwd=target)
        _run(["git", "fetch", "origin", branch], cwd=target)
        _run(["git", "checkout", branch], cwd=target)
        _run(["git", "reset", "--hard", f"origin/{branch}"], cwd=target)
        _run(["git", "clean", "-fd"], cwd=target)

    branch_name = _git_output(target, "branch", "--show-current")
    head = _git_output(target, "rev-parse", "--short", "HEAD")
    remote_head = _git_output(target, "rev-parse", "--short", f"origin/{branch}")
    status = _git_output(target, "status", "-sb")

    return {
        "ts": _utc_now_iso(),
        "action": action,
        "target": str(target),
        "source": source,
        "branch": branch_name,
        "head": head,
        "remote_head": remote_head,
        "clean": status == f"## {branch}...origin/{branch}",
        "status": status,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Clone or reset a clean canonical checkout on sot/mainline")
    ap.add_argument("--source", default="https://github.com/magikgmo4-ui/opt-trading.git")
    ap.add_argument("--target", default="/home/ghost/opt-trading-mainline-clean")
    ap.add_argument("--branch", default="sot/mainline")
    args = ap.parse_args()

    report = ensure_canonical_checkout(args.source, Path(args.target), args.branch)
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
