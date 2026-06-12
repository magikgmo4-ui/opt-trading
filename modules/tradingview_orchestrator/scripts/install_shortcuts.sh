#!/usr/bin/env bash
set -euo pipefail

MOD="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="/usr/local/bin"

install_wrapper() {
  local name="$1"; local args="${2:-}"
  sudo tee "$BIN/$name" > /dev/null <<EOF
#!/usr/bin/env bash
exec bash "$MOD/scripts/cmd.sh" $args "\$@"
EOF
  sudo chmod +x "$BIN/$name"
  echo "  installed $BIN/$name"
}

echo "=== Installing tradingview_orchestrator shortcuts ==="
install_wrapper "tv-orchestrator"
install_wrapper "tv-snapshot"    "snapshot"
install_wrapper "tv-alert-list"  "alert-list"
install_wrapper "tv-job"         "run"
echo "Done."
