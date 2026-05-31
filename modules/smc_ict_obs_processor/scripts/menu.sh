#!/usr/bin/env bash
# Interactive menu — smc_ict_obs_processor
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO_ROOT"
echo "=== smc_ict_obs_processor ==="
echo "1) Post ObservationEvent (manual fields)"
echo "2) Post from summary.json (bot_vision_step2)"
echo "3) Dry-run (build only, no POST)"
echo "q) Quit"
read -rp "Choice: " choice
case "$choice" in
  1) bash modules/smc_ict_obs_processor/scripts/cmd.sh post --help ;;
  2) bash modules/smc_ict_obs_processor/scripts/cmd.sh from-summary --help ;;
  3) echo "Add --dry-run to any cmd.sh call." ;;
  q) exit 0 ;;
  *) echo "Unknown choice"; exit 1 ;;
esac
