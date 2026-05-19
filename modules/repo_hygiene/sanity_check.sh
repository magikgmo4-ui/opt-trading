#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT/modules/repo_hygiene/repo_hygiene_lib.sh"

rh_banner
echo "[root] $ROOT"
echo

echo "[1] leading-backslash scan"
lb="$(rh_find_leading_backslash "$ROOT" || true)"
if [[ -n "$lb" ]]; then
  echo "FAIL: found files starting with a leading '\\' line:"
  echo "$lb"
  echo
  echo "Fix (after review): cmd-repo_hygiene fix-leading-backslash --apply"
  exit 2
else
  echo "OK"
fi
echo

echo "[2] sqlite WAL/SHM artifacts scan"
art="$(rh_find_sqlite_artifacts "$ROOT" || true)"
if [[ -n "$art" ]]; then
  echo "FAIL: found SQLite runtime artifacts (should not be committed):"
  echo "$art"
  echo
  echo "Cleanup (after review): cmd-repo_hygiene cleanup-artifacts --apply"
  exit 3
else
  echo "OK"
fi
echo

echo "[3] *.bak_* scan (patch backups)"
bak="$(rh_find_bak_underscore "$ROOT" || true)"
if [[ -n "$bak" ]]; then
  echo "WARN: found *.bak_* files (likely patch backups). Consider removing/moving out of repo:"
  echo "$bak"
else
  echo "OK"
fi
echo

echo "[4] student legacy recursion scan"
if rh_detect_student_legacy_loop "$ROOT"; then
  echo "FAIL: student legacy recursion detected. This can cause menu freeze."
  echo "Plan: remove/rename scripts/student/ legacy directory OR fix shortcuts to point to v2 scripts."
  exit 4
else
  echo "OK"
fi
echo

echo "PASS: repo_hygiene sanity OK"
