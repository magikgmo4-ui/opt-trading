#!/usr/bin/env bash
# Install Tasker-callable scripts to ~/.termux/tasker/
# Run from Termux after bootstrap
set -Eeuo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/tasker"
DST="$HOME/.termux/tasker"

mkdir -p "$DST"

for script in health_summary.sh sessions_list.sh log_tail.sh attach_hint.sh; do
    cp "$SRC/$script" "$DST/$script"
    chmod +x "$DST/$script"
    echo "  Installed: $DST/$script"
done

echo ""
echo "=== Tasker scripts installed ==="
echo "  $DST/"
echo ""
echo "Configure Tasker actions:"
echo "  Plugin → Termux:Tasker"
echo "  Executable: bash"
echo "  Argument: ~/.termux/tasker/<script>"
echo "  Timeout: 30s"
