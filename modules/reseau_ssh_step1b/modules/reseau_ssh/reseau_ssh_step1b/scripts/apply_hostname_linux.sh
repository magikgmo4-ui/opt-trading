\
#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: $(basename "$0") <target-hostname>"
  exit 1
fi

echo "=== reseau_ssh hostname apply ==="
echo "Current: $(hostname)"
echo "Target : $TARGET"

if [[ "$(hostname)" == "$TARGET" ]]; then
  echo "OK: already set"
  exit 0
fi

sudo hostnamectl set-hostname "$TARGET"
echo "OK: now $(hostname)"
