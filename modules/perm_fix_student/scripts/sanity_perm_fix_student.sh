#!/usr/bin/env bash
set -euo pipefail

echo "sanity_perm_fix_student — checks"

FAIL=0

if [[ ! -d /opt/trading ]]; then
  echo "FAIL: /opt/trading missing"
  FAIL=1
fi

FOUND=0
for p in /opt/trading/state /opt/trading/tmp /opt/trading/_student_archive; do
  if [[ -d "$p" ]]; then
    FOUND=1
    unreadable="$(find "$p" -type f ! -readable | head -n 1 || true)"
    if [[ -n "$unreadable" ]]; then
      echo "WARN: unreadable runtime files exist (run: sudo cmd-perm_fix_student fix_runtime)"
      echo "Example: $unreadable"
      FAIL=1
    else
      echo "OK: runtime files readable under $p"
    fi
  fi
done

if [[ "$FOUND" -eq 0 ]]; then
  echo "WARN: runtime dirs missing (/opt/trading/state, /opt/trading/tmp, /opt/trading/_student_archive)"
fi

if command -v ollama >/dev/null 2>&1; then
  echo "OK: ollama present"
else
  echo "INFO: ollama not installed (skip)"
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "PASS: perm_fix_student sanity OK"
  exit 0
else
  echo "FAIL: perm_fix_student sanity failed"
  exit 1
fi
