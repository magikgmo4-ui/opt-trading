#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/perf/scripts/menu.sh" "$BIN/menu-perf"
sudo ln -sf "$ROOT/modules/perf/scripts/cmd.sh" "$BIN/cmd-perf"
sudo ln -sf "$ROOT/modules/perf/scripts/sanity_check.sh" "$BIN/sanity-perf"
echo "OK: installed shortcuts for perf"
ls -l "$BIN/menu-perf" "$BIN/cmd-perf" "$BIN/sanity-perf"
