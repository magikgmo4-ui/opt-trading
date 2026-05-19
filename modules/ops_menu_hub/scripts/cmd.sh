#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"

show_msi() {
    echo "=== Desk Pro - MSI Operator Hub Structure (V1) ==="
    echo
    echo "[ Operator Tools ]"
    echo "  - cmd-desk_pro_runner"
    echo "  - cmd-desk_capture_inputs"
    echo "  - cmd-desk_analyze"
    echo "  - cmd-desk_pro_dashboard"
    echo
    echo "[ Analysis Engines ]"
    echo "  - cmd-derivatives_collector"
    echo "  - cmd-derivatives_analyzer"
    echo "  - cmd-probability_engine"
    echo "  - cmd-market_scanner"
    echo "  - cmd-opportunity_ranker"
    echo "  - cmd-liquidation_analyzer"
    echo "  - cmd-decision_engine"
    echo "  - cmd-risk_engine"
    echo
    echo "[ Monitoring ]"
    echo "  - menu-perf"
    echo "  - cmd-desk_state"
    echo "  - menu-vision_bot"
    echo "  - cmd-desk_retention"
    echo
    echo "[ Maintenance ]"
    echo "  - sanity-*"
    echo "  - cmd-ops_wrappers"
}

usage() {
  cat <<'EOF'
Usage: cmd.sh <command>

Commands:
  msi (or show-msi) : Show MSI Hub structure
  list              : List detected modules
  shortcuts         : List installed shortcuts
  run <module>      : Run module menu
EOF
}

CMD="${1:-}"
[ -z "$CMD" ] && { usage; exit 1; }

# Legacy logic support + New MSI
H="$BASE/ops_menu_hub.sh"

case "$CMD" in
  msi|show-msi) show_msi ;;
  list) bash "$H" list ;;
  shortcuts) bash "$H" shortcuts ;;
  bootstrap_shortcuts) bash "$H" bootstrap_shortcuts ;;
  run) bash "$H" run "${2:-}" ;;
  *) echo "Unknown: $CMD"; usage; exit 1 ;;
esac
