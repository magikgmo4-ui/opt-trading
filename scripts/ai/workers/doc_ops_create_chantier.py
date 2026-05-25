#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from datetime import datetime

# Canonical structure for Doc Ops chantiers
CHARTIER_DIR = "docs/chantiers"
INBOX_DIR = "docs/index/inbox"

# GO_ID Regex: starts with GO_, uppercase, underscores, ends with _NN
GO_ID_REGEX = r"^GO_[A-Z0-9_]+_[0-9]{2}$"

INITIAL_DOC_TEMPLATE = """---
go_id: {go_id}
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: {updated_at}
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
{summary}

## 2_INITIAL_PROJECT_DOC
This document.

## 3_INITIAL_NEED
(Document the initial need here)

## 4_MASTER_PROJECT_PLAN
- [ ] Task 1
- [ ] Task 2

## 6_FINAL_TARGET
(Define the final target result)

## 7_CANONICAL_STATE
(Define what the final successful state looks like)

## 12_INVARIANTS
- No modification of global indexes.
- No modification of CI workflows.
- No modification of trading/runtime modules.

## 16_TODO
- [x] Initiation
- [ ] Implementation
- [ ] Validation
- [ ] Close Gate

## 17_RESUME_POINT
(Define the current resume point)
"""

INBOX_TEMPLATE = """# INBOX: {go_id}

- **ID**: {go_id}
- **PURPOSE**: {summary}
- **LINK**: [Chantier Docs](../chantiers/{go_id}/00_INITIAL_PROJECT_DOC.md)
"""

def validate_go_id(go_id):
    if not re.match(GO_ID_REGEX, go_id):
        return False, f"Invalid GO_ID format: {go_id}. Must be GO_<UPPERCASE_AND_UNDERSCORES>_<NN>."
    return True, ""

def create_chantier(go_id, summary, doc_only=False, create_inbox=False, dry_run=False, force=False):
    created_files = []
    skipped_files = []
    errors = []

    # 1. Validate GO_ID
    is_valid, err_msg = validate_go_id(go_id)
    if not is_valid:
        return False, {"errors": [err_msg]}

    # 2. Paths
    chantier_path = os.path.join(CHARTIER_DIR, go_id)
    initial_doc_path = os.path.join(chantier_path, "00_INITIAL_PROJECT_DOC.md")
    inbox_path = os.path.join(INBOX_DIR, f"{go_id}.md")

    # 3. Create directory
    if not dry_run:
        if not os.path.exists(chantier_path):
            os.makedirs(chantier_path, exist_ok=True)
            print(f"Created directory: {chantier_path}")
        else:
            print(f"Directory already exists: {chantier_path}")
    else:
        print(f"[DRY-RUN] Would create directory: {chantier_path}")

    # 4. Create Initial Doc
    updated_at = datetime.now().strftime("%Y-%m-%d")
    initial_doc_content = INITIAL_DOC_TEMPLATE.format(
        go_id=go_id,
        updated_at=updated_at,
        summary=summary or "(Define the master target here)"
    )

    if os.path.exists(initial_doc_path) and not force:
        errors.append(f"Conflict: File already exists: {initial_doc_path}")
        print(f"File already exists: {initial_doc_path}")
    else:
        if not dry_run:
            with open(initial_doc_path, "w") as f:
                f.write(initial_doc_content)
            created_files.append(initial_doc_path)
            print(f"Created file: {initial_doc_path}")
        else:
            print(f"[DRY-RUN] Would create file: {initial_doc_path}")

    # 5. Create Inbox entry
    if create_inbox:
        inbox_content = INBOX_TEMPLATE.format(
            go_id=go_id,
            summary=summary or "(Define the purpose here)"
        )
        if os.path.exists(inbox_path) and not force:
            errors.append(f"Conflict: File already exists: {inbox_path}")
            print(f"File already exists: {inbox_path}")
        else:
            if not dry_run:
                with open(inbox_path, "w") as f:
                    f.write(inbox_content)
                created_files.append(inbox_path)
                print(f"Created file: {inbox_path}")
            else:
                print(f"[DRY-RUN] Would create file: {inbox_path}")

    status = "PASS" if not errors else "FAIL"
    result = {
        "status": status,
        "go_id": go_id,
        "created_files": created_files,
        "skipped_files": skipped_files,
        "errors": errors
    }
    return (not errors), result

def main():
    parser = argparse.ArgumentParser(description="Doc Ops Chantier Creation Assistant")
    parser.add_argument("--go-id", required=True, help="GO ID (e.g., GO_MY_PROJECT_01)")
    parser.add_argument("--summary", help="Short description of the project")
    parser.add_argument("--doc-only", action="store_true", help="Documentation only mode")
    parser.add_argument("--create-inbox", action="store_true", help="Create inbox entry")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without writing")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")

    args = parser.parse_args()

    success, result = create_chantier(
        args.go_id,
        args.summary,
        args.doc_only,
        args.create_inbox,
        args.dry_run,
        args.force
    )

    if args.json:
        print(json.dumps(result, indent=2))
    elif not success:
        for err in result.get("errors", []):
            print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
