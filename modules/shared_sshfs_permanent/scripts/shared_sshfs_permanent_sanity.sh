#!/usr/bin/env bash
set -euo pipefail

MODULE="shared_sshfs_permanent"
ENV_FILE="/etc/opt-trading/shared_sshfs_permanent.env"
SERVICE="shared-sshfs.service"
PASS=0
FAIL=0

ok(){ echo "PASS: $*"; PASS=$((PASS+1)); }
bad(){ echo "FAIL: $*"; FAIL=$((FAIL+1)); }

if command -v sshfs >/dev/null 2>&1; then ok "sshfs present"; else bad "sshfs missing (sudo apt-get install -y sshfs)"; fi
if command -v fusermount3 >/dev/null 2>&1 || command -v fusermount >/dev/null 2>&1; then ok "fusermount present"; else bad "fusermount missing"; fi

if [[ -f "$ENV_FILE" ]]; then ok "env file exists: $ENV_FILE"; 
  # shellcheck disable=SC1090
  source "$ENV_FILE"
else
  bad "env file missing: $ENV_FILE (run INSTALL.sh)"
fi

if systemctl list-unit-files | grep -q "^${SERVICE}"; then ok "systemd unit exists: $SERVICE"; else bad "systemd unit missing: $SERVICE"; fi

mp="${MOUNT_POINT:-/shared}"
if [[ -d "$mp" ]]; then ok "mount point dir exists: $mp"; else bad "mount point missing: $mp"; fi

if mountpoint -q "$mp"; then ok "mounted: $mp"; else bad "not mounted: $mp (cmd-${MODULE} mount)"; fi

echo
echo "Summary: PASS=$PASS FAIL=$FAIL"
if [[ "$FAIL" -gt 0 ]]; then exit 1; fi
