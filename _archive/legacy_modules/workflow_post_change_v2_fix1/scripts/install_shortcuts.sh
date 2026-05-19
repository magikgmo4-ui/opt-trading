#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/workflow_post_change_v2_fix1/scripts/menu.sh" "$BIN/menu-workflow_post_change_v2_fix1"
sudo ln -sf "$ROOT/modules/workflow_post_change_v2_fix1/scripts/cmd.sh" "$BIN/cmd-workflow_post_change_v2_fix1"
sudo ln -sf "$ROOT/modules/workflow_post_change_v2_fix1/scripts/sanity_check.sh" "$BIN/sanity-workflow_post_change_v2_fix1"
echo "OK: installed shortcuts for workflow_post_change_v2_fix1"
ls -l "$BIN/menu-workflow_post_change_v2_fix1" "$BIN/cmd-workflow_post_change_v2_fix1" "$BIN/sanity-workflow_post_change_v2_fix1"
