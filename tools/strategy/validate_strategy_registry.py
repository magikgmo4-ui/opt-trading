#!/usr/bin/env python3
"""
Validate strategy_id occurrences across pipeline surfaces
against the canonical 95_STRATEGY_REGISTRY.md.

Mode: WARNING_ONLY — no hard fail on unknown IDs.
"""

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = (
    REPO_ROOT
    / "docs"
    / "chantiers"
    / "GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01"
    / "95_STRATEGY_REGISTRY.md"
)

TARGET_FILES = [
    "modules/signal_router/app/schema.py",
    "modules/signal_router/app/router.py",
    "modules/signal_router/tests/test_router.py",
    "modules/proposition_engine/app/schema.py",
    "modules/proposition_engine/app/builder_prompt.py",
    "modules/proposition_engine/app/__main__.py",
    "modules/proposition_engine/tests/test_proposition.py",
    "modules/notification_dispatcher/app/events.py",
    "modules/notification_dispatcher/tests/test_dispatcher.py",
    "modules/trading_realtime_v1/app/runtime_loop_v1.py",
    "modules/trading_realtime_v1/app/event_bridge_v1.py",
    "modules/trading_lab_v1/app/trading_lab_v1.py",
    "tests/e2e/test_e2e_dry_run_pipeline.py",
]

TEST_PATTERNS = [re.compile(r"tests?/"), re.compile(r"/tests?/")]

STRATEGY_RE = re.compile(
    r"""strategy_id\s*=\s*["']([^"']+)["']"""
    r"""|STRATEGY_ID\s*=\s*["']([^"']+)["']"""
    r"""|"strategy_id"\s*:\s*["']([^"']+)["']"""
)


def load_registry(path: Path) -> set[str]:
    registered = set()
    table_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("| # |"):
            table_section = True
            continue
        if stripped.startswith("|---"):
            continue
        if stripped.startswith("|") and table_section:
            parts = [p.strip() for p in stripped.split("|")]
            if len(parts) >= 3 and parts[2].startswith("`") and parts[2].endswith("`"):
                sid = parts[2].strip("`")
                registered.add(sid)
        elif not stripped.startswith("|"):
            table_section = False
    return registered


def is_test_path(rel: str) -> bool:
    return any(p.search(rel) for p in TEST_PATTERNS)


def scan_file(path: Path, rel: str, registered: set[str]) -> list[dict]:
    findings = []
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return findings

    for match in STRATEGY_RE.finditer(text):
        value = match.group(1) or match.group(2) or match.group(3)
        if value:
            in_test = is_test_path(rel)
            known = value in registered
            findings.append({
                "file": rel,
                "value": value,
                "known": known,
                "test_context": in_test,
                "line": text[: match.start()].count("\n") + 1,
            })
    return findings


def main() -> int:
    print("=== Strategy ID Registry Validation ===")
    print(f"Registry: {REGISTRY_PATH.relative_to(REPO_ROOT)}")

    if not REGISTRY_PATH.exists():
        print(f"ERROR: Registry not found at {REGISTRY_PATH}")
        return 1

    registered = load_registry(REGISTRY_PATH)
    print(f"Registered ({len(registered)}): {', '.join(sorted(registered))}")
    print()

    all_findings = []
    for rel in TARGET_FILES:
        abspath = REPO_ROOT / rel
        hits = scan_file(abspath, rel, registered)
        all_findings.extend(hits)

    known_count = 0
    unknown_count = 0
    test_known = 0
    test_unknown = 0

    for f in all_findings:
        if f["known"]:
            if f["test_context"]:
                tag = "TEST_REGISTERED"
                test_known += 1
            else:
                tag = "REGISTERED"
                known_count += 1
            status = "OK"
        else:
            if f["test_context"]:
                tag = "TEST_UNREGISTERED"
                test_unknown += 1
            else:
                tag = "UNREGISTERED"
                unknown_count += 1
            status = "WARNING"

        print(f"  [{status:7s}] Ln {f['line']:4d}  {f['file']}")
        print(f"           -> {f['value']!r} ({tag})")

    print()
    print("=== Summary ===")
    print(f"  REGISTERED:         {known_count}")
    print(f"  UNREGISTERED:       {unknown_count}")
    print(f"  TEST_REGISTERED:    {test_known}")
    print(f"  TEST_UNREGISTERED:  {test_unknown}")
    print(f"  TOTAL:              {len(all_findings)}")

    result = "WARNINGS" if (unknown_count + test_unknown) > 0 else "CLEAN"
    print(f"\n=== Result: {result} ===")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
