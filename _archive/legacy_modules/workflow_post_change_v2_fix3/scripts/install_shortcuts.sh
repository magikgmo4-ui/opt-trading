#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/workflow_post_change_v2_fix3/scripts/menu.sh" "$BIN/menu-workflow_post_change_v2_fix3"
sudo ln -sf "$ROOT/modules/workflow_post_change_v2_fix3/scripts/cmd.sh" "$BIN/cmd-workflow_post_change_v2_fix3"
sudo ln -sf "$ROOT/modules/workflow_post_change_v2_fix3/scripts/sanity_check.sh" "$BIN/sanity-workflow_post_change_v2_fix3"
echo "OK: installed shortcuts for workflow_post_change_v2_fix3"
ls -l "$BIN/menu-workflow_post_change_v2_fix3" "$BIN/cmd-workflow_post_change_v2_fix3" "$BIN/sanity-workflow_post_change_v2_fix3"
