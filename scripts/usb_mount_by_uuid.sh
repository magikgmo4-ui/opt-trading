\
#!/usr/bin/env bash
set -euo pipefail
UUID="${1:-}"
if [[ -z "$UUID" ]]; then
  echo "Usage: $0 <UUID>"
  echo "Find UUID with: lsblk -f"
  exit 1
fi
MNT="/mnt/usb"
sudo mkdir -p "$MNT"
sudo mount -U "$UUID" "$MNT"
echo "Mounted at $MNT"
df -h "$MNT"
