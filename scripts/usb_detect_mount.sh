\
#!/usr/bin/env bash
set -euo pipefail
echo "=== USB Detect ==="
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,MODEL | sed 's/^/  /'
echo ""
echo "Plug USB, then identify the partition (e.g. /dev/sda1)."
echo "If already mounted, note the mountpoint."
