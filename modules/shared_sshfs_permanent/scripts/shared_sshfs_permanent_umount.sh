#!/usr/bin/env bash
set -euo pipefail
ENV_FILE="/etc/opt-trading/shared_sshfs_permanent.env"
mp="/shared"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  mp="${MOUNT_POINT:-/shared}"
fi

if mountpoint -q "$mp"; then
  echo "Unmounting $mp"
  if command -v fusermount3 >/dev/null 2>&1; then
    fusermount3 -u "$mp" || umount "$mp" || true
  else
    fusermount -u "$mp" || umount "$mp" || true
  fi
else
  echo "Not mounted: $mp"
fi
