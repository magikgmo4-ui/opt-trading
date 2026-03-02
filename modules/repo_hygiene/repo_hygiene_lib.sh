#!/usr/bin/env bash
set -euo pipefail

# repo_hygiene_lib.sh — shared helpers

rh_root() {
  cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd
}

rh_banner() {
  echo "=== repo_hygiene ==="
  date -Iseconds
  echo
}

rh_find_leading_backslash() {
  local root="$1"
  # Find files whose first non-empty line is exactly a single backslash
  # We scan text-like files only (exclude large/binary by simple heuristic).
  python3 - <<'PY' "$root"
import os, sys
root = sys.argv[1]
hits = []
for dirpath, dirnames, filenames in os.walk(root):
    # skip .git if present
    dirnames[:] = [d for d in dirnames if d not in {'.git', '.venv', '__pycache__'}]
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, root)
        # skip known noisy dirs
        if rel.startswith(('_student_archive/', 'tmp/', 'logs/', '.pytest_cache/')):
            continue
        # skip very large files
        try:
            if os.path.getsize(p) > 2_000_000:
                continue
        except OSError:
            continue
        # quick binary heuristic
        try:
            with open(p, 'rb') as f:
                chunk = f.read(4096)
            if b'\x00' in chunk:
                continue
        except Exception:
            continue
        try:
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
        except Exception:
            continue
        # find first non-empty line
        first = None
        for line in lines[:10]:
            s = line.rstrip('\n').rstrip('\r')
            if s.strip() == '':
                continue
            first = s
            break
        if first == '\\':
            hits.append(rel)
if hits:
    print("\n".join(sorted(hits)))
PY
}

rh_fix_leading_backslash() {
  local root="$1"
  local apply="${2:-}"
  local list
  list="$(rh_find_leading_backslash "$root" || true)"
  if [[ -z "${list}" ]]; then
    echo "OK: no leading-backslash files found."
    return 0
  fi
  echo "FOUND leading-backslash files:"
  echo "$list"
  echo
  if [[ "$apply" != "--apply" ]]; then
    echo "DRY-RUN: pass --apply to remove the first '\\' line from each file listed."
    return 0
  fi

  # apply safely using python (edit in-place)
  python3 - <<'PY' "$root" "$list"
import os, sys
root = sys.argv[1]
files = sys.argv[2].splitlines()
for rel in files:
    p = os.path.join(root, rel)
    try:
        with open(p, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        # remove first non-empty line if it is exactly "\"
        out = []
        removed = False
        for i, line in enumerate(lines):
            s = line.rstrip('\n').rstrip('\r')
            if not removed:
                if s.strip() == '':
                    out.append(line)
                    continue
                if s == '\\':
                    removed = True
                    continue
            out.append(line)
        if removed:
            with open(p, 'w', encoding='utf-8') as f:
                f.writelines(out)
            print("FIXED", rel)
        else:
            print("SKIP", rel)
    except Exception as e:
        print("ERR", rel, e)
PY
}

rh_find_sqlite_artifacts() {
  local root="$1"
  find "$root" -type f \( -name "*.db-wal" -o -name "*.db-shm" -o -name "*.sqlite-wal" -o -name "*.sqlite-shm" \)     -not -path "*/.git/*" -print | sed "s|^$root/||" | sort
}

rh_find_bak_underscore() {
  local root="$1"
  find "$root" -type f -name "*.bak_*" -not -path "*/.git/*" -print | sed "s|^$root/||" | sort
}

rh_detect_student_legacy_loop() {
  local root="$1"
  local p="$root/scripts/student/student_cmd.sh"
  if [[ -f "$p" ]]; then
    if grep -qE '^exec\s+/opt/trading/scripts/student/student_cmd\.sh' "$p"; then
      echo "FOUND legacy student_cmd recursion: scripts/student/student_cmd.sh"
      return 0
    fi
  fi
  return 1
}
