#!/usr/bin/env python3
"""G04 — Validate bridge contracts: forbidden actions + link to capability matrix.

Checks each contract for:
1. All required fields present
2. forbidden_actions non-empty
3. evidence_ref present
4. Maps to capability matrix (G01 M21-M30)
"""

import json
import sys
import yaml  # may not be available, fallback to regex
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTRACTS_FILE = REPO_ROOT / "docs" / "chantiers" / "GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01" / "20_BRIDGE_CONTRACTS.md"
EVIDENCE_DIR = REPO_ROOT / "docs" / "chantiers" / "GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01"
RESULT_DIR = EVIDENCE_DIR / "validation_result"
RESULT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FIELDS = [
    "app_id", "purpose", "source_of_truth_rank", "allowed_reads",
    "allowed_writes", "forbidden_actions", "required_env_vars",
    "dry_run_mode", "approval_gate", "audit_log",
    "rollback_or_compensating_action", "evidence_ref"
]

# Mapping app_id → capability matrix rows
MATRIX_MAP = {
    "airtable": "M21",
    "clickup": "M22",
    "botpress": "M23",
    "google_sheets": "M24",
    "telegram": "M25",
    "gmail": "M26",
    "google_calendar": "M27",
    "google_drive": "M28",
    "figma": "M29",
    "localcms": "M30",
    "local_cms": "M30",
}


def extract_yaml_blocks(md_content):
    """Extract yaml blocks from markdown (between ```yaml and ```)."""
    blocks = []
    lines = md_content.splitlines()
    in_yaml = False
    current = []
    for line in lines:
        if line.strip().startswith("```yaml"):
            in_yaml = True
            current = []
        elif line.strip() == "```" and in_yaml:
            in_yaml = False
            blocks.append("\n".join(current))
        elif in_yaml:
            current.append(line)
    return blocks


def parse_yaml_safe(text):
    """Parse yaml, fallback to json.loads, then to manual dict."""
    # Try yaml first
    try:
        import yaml as _yaml
        return _yaml.safe_load(text)
    except ImportError:
        pass
    # Try json
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Manual key: value extraction (simplified)
    result = {}
    for line in text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val.startswith("[") or val.startswith("-"):
                val = [v.strip("- ").strip() for v in val.splitlines()] if "\n" in val else val
            result[key] = val
    return result


def validate_contract(name, data):
    errors = []
    warnings = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] is None:
            errors.append(f"Missing field: {field}")

    # Check forbidden_actions non-empty
    forbidden = data.get("forbidden_actions", [])
    if isinstance(forbidden, str):
        if not forbidden.strip():
            errors.append("forbidden_actions is empty")
    elif isinstance(forbidden, list):
        if len(forbidden) == 0:
            errors.append("forbidden_actions list is empty")
    else:
        errors.append(f"forbidden_actions has unexpected type: {type(forbidden)}")

    # Check evidence_ref
    evidence = data.get("evidence_ref", "")
    if not evidence or evidence == "N/A":
        warnings.append("evidence_ref is N/A or empty")

    # Check matrix mapping
    matrix_row = MATRIX_MAP.get(name)
    if matrix_row:
        data["matrix_row"] = matrix_row
    else:
        warnings.append(f"No matrix mapping for app_id: {name}")

    return errors, warnings


def main():
    content = CONTRACTS_FILE.read_text(encoding="utf-8")
    blocks = extract_yaml_blocks(content)
    print(f"Found {len(blocks)} YAML blocks")

    results = {}
    all_pass = True

    for block in blocks:
        data = parse_yaml_safe(block)
        if not data:
            print("  WARN: Could not parse block, skipping")
            continue
        name = data.get("app_id", "unknown")

        print(f"\n[{name}]")
        errors, warnings = validate_contract(name, data)
        results[name] = {"errors": errors, "warnings": warnings}

        if errors:
            all_pass = False
            for e in errors:
                print(f"  ✗ ERROR: {e}")
        else:
            print(f"  ✓ All required fields present")

        if warnings:
            for w in warnings:
                print(f"  ⚠ WARNING: {w}")

        if not errors and not warnings:
            print(f"  ✓ Contract valid")

        if "matrix_row" in data:
            print(f"  → Capability matrix: {data['matrix_row']}")

    # Summary
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    valid_count = sum(1 for r in results.values() if not r["errors"])
    total = len(results)
    print(f"  Valid: {valid_count}/{total}")
    for name, r in results.items():
        status = "✓ PASS" if not r["errors"] else "✗ FAIL"
        print(f"  [{status}] {name}")

    # Write result
    result = {
        "validated_at": __import__("datetime").datetime.now().isoformat(),
        "contracts_validated": total,
        "valid": valid_count,
        "all_pass": all_pass,
        "results": results,
    }
    result_path = RESULT_DIR / "validation_summary.json"
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult: {result_path}")

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
