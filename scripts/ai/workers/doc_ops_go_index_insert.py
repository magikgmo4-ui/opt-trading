#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime

GO_ID_REGEX = r"^GO_[A-Z0-9_]+_[0-9]{2}$"
DEFAULT_INDEX = "docs/index/GO_INDEX.md"
CHARTIER_DIR = "docs/chantiers"

ENTRY_TEMPLATE = """### {go_id}
- repo : opt-trading
- type : {entry_type}
- statut : {status}
- titre court : {short_title}
- dernier état connu : {last_known}
- lien utile : `{initial_doc_path}`
"""

def validate_go_id(go_id):
    if not re.match(GO_ID_REGEX, go_id):
        return False, f"Invalid GO_ID format: {go_id}. Must be GO_<UPPERCASE_AND_UNDERSCORES>_<NN>."
    return True, ""

def extract_frontmatter(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm

def extract_section(content, section_name):
    pattern = rf"^##[ \t]*{re.escape(section_name)}[ \t]*\n(.*?)(?=\n##[ \t]|\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def parse_initial_doc(path):
    if not os.path.exists(path):
        return None, f"Initial project doc not found: {path}"
    with open(path, "r") as f:
        content = f.read()
    fm = extract_frontmatter(content)
    master_target = extract_section(content, "1_MASTER_TARGET") or ""
    final_target = extract_section(content, "6_FINAL_TARGET") or ""
    parent_go_id = extract_section(content, "PARENT_GO_ID") or ""
    short_title = master_target.split("\n")[0][:120] if master_target else ""
    entry_type = "chantier technique" if not parent_go_id else "chantier technique / child"
    status = fm.get("status", "OPEN")
    updated_at = fm.get("updated_at", datetime.now().strftime("%Y-%m-%d"))
    return {
        "go_id": fm.get("go_id", ""),
        "master_target": master_target,
        "final_target": final_target,
        "parent_go_id": parent_go_id,
        "short_title": short_title,
        "entry_type": entry_type,
        "status": status,
        "updated_at": updated_at,
    }, None

def generate_entry(data):
    initial_doc_path = f"docs/chantiers/{data['go_id']}/00_INITIAL_PROJECT_DOC.md"
    return ENTRY_TEMPLATE.format(
        go_id=data["go_id"],
        entry_type=data["entry_type"],
        status=data["status"],
        short_title=data["short_title"] or "(no master target defined)",
        last_known=data["master_target"][:120] if data["master_target"] else "(no master target defined)",
        initial_doc_path=initial_doc_path,
    )

def entry_exists_in_index(index_path, go_id):
    if not os.path.exists(index_path):
        return False
    with open(index_path, "r") as f:
        content = f.read()
    pattern = rf"^###\s+{re.escape(go_id)}\s*$"
    return bool(re.search(pattern, content, re.MULTILINE))

def find_section_line(index_path, section_name):
    if not os.path.exists(index_path):
        return None
    with open(index_path, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") and section_name in stripped:
            return i + 1
    return None

def apply_entry(index_path, entry_text, go_id):
    if not os.path.exists(index_path):
        return False, f"Index file not found: {index_path}"
    if entry_exists_in_index(index_path, go_id):
        return False, f"Entry already exists for {go_id}"
    with open(index_path, "r") as f:
        content = f.read()
    section_header = "## Entrées"
    if section_header in content:
        new_content = content.replace(
            section_header,
            section_header + "\n" + entry_text.rstrip("\n"),
            1
        )
    else:
        new_content = content + "\n\n" + section_header + "\n\n" + entry_text
    with open(index_path, "w") as f:
        f.write(new_content)
    return True, "Entry inserted"

def diff_preview(index_path, entry_text, go_id):
    if not os.path.exists(index_path):
        lines = []
    else:
        with open(index_path, "r") as f:
            lines = f.readlines()
    entry_lines = entry_text.rstrip("\n").split("\n")
    section_header = "## Entrées\n"
    header_present = any("## Entrées" in l for l in lines)
    print("--- a/" + index_path)
    print("+++ b/" + index_path)
    if not header_present:
        print("@@ -1,0 +1,@@")
        for l in entry_lines:
            print("+" + l)
    else:
        print("@@ ... @@")
        for l in entry_lines:
            print("+" + l)

def main():
    parser = argparse.ArgumentParser(description="Doc Ops GO Index Insertion Assistant")
    parser.add_argument("--go-id", required=True, help="GO ID to insert into GO_INDEX.md")
    parser.add_argument("--index-path", default=DEFAULT_INDEX, help="Path to GO_INDEX.md")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no write")
    parser.add_argument("--apply", action="store_true", help="Write entry to index")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--entry-status", default="OPEN", help="Status in the entry (e.g., OPEN, ACTIVE, REFERENCE)")
    parser.add_argument("--section", default="Entrées", help="Section in the index to insert under")
    args = parser.parse_args()

    is_valid, err_msg = validate_go_id(args.go_id)
    if not is_valid:
        result = {"status": "FAIL", "go_id": args.go_id, "errors": [err_msg], "exit_code": 1}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {err_msg}", file=sys.stderr)
        sys.exit(1)

    initial_doc_path = os.path.join(CHARTIER_DIR, args.go_id, "00_INITIAL_PROJECT_DOC.md")
    data, error = parse_initial_doc(initial_doc_path)
    if error:
        result = {"status": "FAIL", "go_id": args.go_id, "errors": [error], "exit_code": 2}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)

    data["status"] = args.entry_status
    entry = generate_entry(data)
    would_change = not entry_exists_in_index(args.index_path, args.go_id)
    exists = not would_change

    if args.dry_run or not args.apply:
        if not args.json:
            print("Entry preview:")
            print(entry)
            diff_preview(args.index_path, entry, args.go_id)
        result = {
            "status": "PASS",
            "go_id": args.go_id,
            "index_path": args.index_path,
            "entry": entry,
            "would_change": would_change,
            "duplicate": exists,
            "errors": [],
        }
        if args.json:
            print(json.dumps(result, indent=2))
        sys.exit(0)

    if args.apply:
        success, msg = apply_entry(args.index_path, entry, args.go_id)
        if not success:
            result = {
                "status": "FAIL",
                "go_id": args.go_id,
                "index_path": args.index_path,
                "entry": entry,
                "would_change": False,
                "duplicate": True,
                "errors": [msg],
            }
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Error: {msg}", file=sys.stderr)
            sys.exit(1)
        result = {
            "status": "PASS",
            "go_id": args.go_id,
            "index_path": args.index_path,
            "entry": entry,
            "would_change": True,
            "duplicate": False,
            "errors": [],
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Entry inserted into {args.index_path}")
        sys.exit(0)

if __name__ == "__main__":
    main()
