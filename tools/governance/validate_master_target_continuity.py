#!/usr/bin/env python3
"""
Validate master_target_id continuity across docs/chantiers/
against PRODUCT_FINAL_TARGET_REGISTRY_01.md.

Mode: WARNING_ONLY — no hard fail.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "docs" / "governance" / "PRODUCT_FINAL_TARGET_REGISTRY_01.md"
CHANTIERS_DIR = REPO_ROOT / "docs" / "chantiers"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
MT_ID_RE = re.compile(r"^\s*master_target_id\s*:\s*(.+)\s*$", re.MULTILINE)
GO_ID_RE = re.compile(r"^\s*go_id\s*:\s*(.+)\s*$", re.MULTILINE)
TABLE_ROW_RE = re.compile(r"^\|\s*\d+\s*\|")


def load_registry(path: Path) -> dict:
    entries = {}
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("| # |"):
            in_table = True
            continue
        if stripped.startswith("|---"):
            continue
        if stripped.startswith("|") and in_table:
            parts = [p.strip().strip("`") for p in stripped.strip("|").split("|")]
            if len(parts) >= 6:
                mt_id = parts[1]
                status = parts[3]
                first_go = parts[4]
                current_go = parts[5]
                if mt_id:
                    entries[mt_id] = {"status": status, "first_go": first_go, "current_go": current_go}
        elif in_table and not stripped.startswith("|"):
            in_table = False
    return entries


def scan_chantiers(base: Path) -> list[dict]:
    findings = []
    for md_file in sorted(base.rglob("*.md")):
        rel = md_file.relative_to(REPO_ROOT)
        text = md_file.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.search(text)
        if not m:
            continue
        front = m.group(1)
        go_id = GO_ID_RE.search(front)
        mt_id = MT_ID_RE.search(front)
        findings.append({
            "file": str(rel),
            "go_id": go_id.group(1).strip() if go_id else None,
            "master_target_id": mt_id.group(1).strip() if mt_id else None,
        })
    return findings


def main() -> int:
    print("=== Master Target Continuity Validator ===")
    print(f"Registry: {REGISTRY_PATH.relative_to(REPO_ROOT)}")
    print(f"Scanning: {CHANTIERS_DIR.relative_to(REPO_ROOT)}/**/*.md\n")

    if not REGISTRY_PATH.exists():
        print(f"ERROR: Registry not found at {REGISTRY_PATH}")
        return 1

    registered = load_registry(REGISTRY_PATH)
    print(f"Registered targets ({len(registered)}):")
    for mt_id, info in sorted(registered.items()):
        print(f"  {mt_id}  [{info['status']}]  first={info['first_go']}  current={info['current_go']}")
    print()

    chantiers = scan_chantiers(CHANTIERS_DIR)
    print(f"Chantier files with frontmatter: {len(chantiers)}\n")

    warnings = []
    seen_ids = set()

    for c in chantiers:
        go_id = c["go_id"]
        mt_id = c["master_target_id"]

        if mt_id:
            if mt_id in seen_ids:
                warnings.append(f"DUPLICATE_MT_ID: {mt_id} appears in {c['file']} (also seen elsewhere)")
            seen_ids.add(mt_id)

            if mt_id not in registered:
                warnings.append(f"UNREGISTERED_MT_ID: {mt_id} in {c['file']} (go_id={go_id})")

    for mt_id in registered:
        chantier_refs = [c for c in chantiers if c["master_target_id"] == mt_id]
        if not chantier_refs:
            warnings.append(f"ORPHAN_MT_ID: {mt_id} is registered but referenced by 0 chantier files")

    checked_go_target = set()
    for c in chantiers:
        go_id = c["go_id"]
        mt_id = c["master_target_id"]
        if not go_id:
            continue
        for reg_id, info in registered.items():
            key = (go_id, reg_id)
            if info["current_go"] == go_id and mt_id != reg_id and key not in checked_go_target:
                checked_go_target.add(key)
                go_has_target = any(
                    x["go_id"] == go_id and x["master_target_id"] == reg_id
                    for x in chantiers
                )
                if not go_has_target:
                    warnings.append(
                        f"CURRENT_GO_MISMATCH: GO {go_id} is current_go of {reg_id} "
                        f"but has no file referencing {reg_id}"
                    )

    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  WARNING: {w}")
    else:
        print("No warnings.")

    print(f"\n=== Result: {'WARNINGS' if warnings else 'CLEAN'} ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
