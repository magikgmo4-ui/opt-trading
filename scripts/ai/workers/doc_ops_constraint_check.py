#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys

def get_git_changes():
    """Returns a list of modified, staged, and untracked files."""
    try:
        # Get modified and staged files
        diff_cmd = ["git", "diff", "HEAD", "--name-only"]
        diff_output = subprocess.check_output(diff_cmd, stderr=subprocess.STDOUT).decode("utf-8")
        
        # Get untracked files (excluding ignored ones)
        untracked_cmd = ["git", "ls-files", "--others", "--exclude-standard"]
        untracked_output = subprocess.check_output(untracked_cmd, stderr=subprocess.STDOUT).decode("utf-8")
        
        files = set()
        for line in diff_output.splitlines() + untracked_output.splitlines():
            if line.strip():
                files.add(line.strip())
        return sorted(list(files))
    except subprocess.CalledProcessError as e:
        print(f"Error calling git: {e.output.decode('utf-8')}", file=sys.stderr)
        sys.exit(2)

def parse_constraints_from_file(file_path):
    """Parses constraints from the frontmatter of a markdown file."""
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, "r") as f:
            content = f.read()
            
        # Look for frontmatter
        match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if not match:
            return []
            
        frontmatter = match.group(1)
        constraints = []
        if "DOC_ONLY" in frontmatter:
            constraints.append("DOC_ONLY")
        if "READ_ONLY" in frontmatter:
            constraints.append("READ_ONLY")
        return constraints
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return []

def check_constraints(files, mode):
    """Checks if the given files violate the specified mode."""
    violations = []
    
    if mode == "READ_ONLY":
        violations = files
    elif mode == "DOC_ONLY":
        for f in files:
            # Allow only docs/** and docs/index/inbox/**
            if not f.startswith("docs/"):
                violations.append(f)
                
    return violations

def main():
    parser = argparse.ArgumentParser(description="Constraint Checking Lite for Doc Ops")
    parser.add_argument("--go-id", help="GO ID to deduce initial doc path")
    parser.add_argument("--initial-doc", help="Path to 00_INITIAL_PROJECT_DOC.md")
    parser.add_argument("--mode", choices=["DOC_ONLY", "READ_ONLY"], help="Force specific mode")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    
    args = parser.parse_args()
    
    # Determine target file
    target_file = None
    explicitly_requested = False
    
    if args.initial_doc:
        target_file = args.initial_doc
        explicitly_requested = True
    elif args.go_id:
        target_file = f"docs/chantiers/{args.go_id}/00_INITIAL_PROJECT_DOC.md"
        explicitly_requested = True
    elif os.path.exists("./00_INITIAL_PROJECT_DOC.md"):
        target_file = "./00_INITIAL_PROJECT_DOC.md"
        
    # Handle missing file if explicitly requested
    if explicitly_requested and (not target_file or not os.path.exists(target_file)):
        print(f"Error: Initial project doc not found at {target_file}", file=sys.stderr)
        sys.exit(2)
        
    # Determine mode
    mode = args.mode
    if not mode and target_file and os.path.exists(target_file):
        constraints = parse_constraints_from_file(target_file)
        if "READ_ONLY" in constraints:
            mode = "READ_ONLY"
        elif "DOC_ONLY" in constraints:
            mode = "DOC_ONLY"
                
    files = get_git_changes()
    violations = check_constraints(files, mode) if mode else []
    
    result = {
        "status": "PASS" if not violations else "FAIL",
        "mode": mode or "NONE",
        "files_changed": len(files),
        "violations": violations
    }
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if mode:
            print(f"Mode: {mode}")
        print(f"Files changed: {len(files)}")
        if violations:
            print("\nVIOLATIONS DETECTED:")
            for v in violations:
                print(f"  - {v}")
            print("\nResult: FAIL")
        else:
            print("\nResult: PASS")
            
    if violations:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
