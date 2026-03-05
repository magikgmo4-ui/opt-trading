\
#!/usr/bin/env bash
set -euo pipefail

echo "sanity_perm_fix_student — checks"

FAIL=0

if [[ ! -d /opt/trading ]]; then
  echo "FAIL: /opt/trading missing"
  FAIL=1
fi

if [[ -d /opt/trading/journal ]]; then
  unreadable="$(find /opt/trading/journal -type f ! -readable | head -n 1 || true)"
  if [[ -n "$unreadable" ]]; then
    echo "WARN: unreadable journal files exist (run: sudo cmd-perm_fix_student fix_journal)"
    echo "Example: $unreadable"
    FAIL=1
  else
    echo "OK: journal files readable"
  fi
else
  echo "WARN: /opt/trading/journal missing"
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
