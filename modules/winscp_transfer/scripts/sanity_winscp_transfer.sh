\
#!/usr/bin/env bash
set -euo pipefail

SHARE_BASE="${SHARE_BASE:-/srv/sftp/shared_files/shared}"
INBOX="${SHARE_BASE}/inbox"
OUTBOX="${SHARE_BASE}/outbox"

echo "sanity_winscp_transfer — checks"

FAIL=0

if [[ ! -d /opt/trading ]]; then
  echo "FAIL: /opt/trading missing"
  FAIL=1
fi

if [[ ! -d "$SHARE_BASE" ]]; then
  echo "FAIL: share base missing: $SHARE_BASE"
  FAIL=1
else
  echo "OK: share base exists: $SHARE_BASE"
fi

if [[ -d "$INBOX" ]]; then
  echo "OK: inbox exists: $INBOX"
else
  echo "WARN: inbox missing (run: sudo cmd-winscp_transfer init)"
fi

if [[ -d "$OUTBOX" ]]; then
  echo "OK: outbox exists: $OUTBOX"
else
  echo "WARN: outbox missing (run: sudo cmd-winscp_transfer init)"
fi

if command -v scp >/dev/null 2>&1 && command -v ssh >/dev/null 2>&1; then
  echo "OK: ssh/scp present"
else
  echo "FAIL: ssh/scp missing"
  FAIL=1
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "PASS: winscp_transfer sanity OK"
  exit 0
else
  echo "FAIL: winscp_transfer sanity failed"
  exit 1
fi
