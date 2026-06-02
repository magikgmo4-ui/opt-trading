#!/usr/bin/env bash
# Creates gitignored runtime state files required by worker scripts.
# Safe to re-run: never overwrites existing state.
set -euo pipefail

mkdir -p data/runtime_health data/logs/cron tmp

if [ ! -f data/runtime_health/kill_switch.state ]; then
    echo "OK" > data/runtime_health/kill_switch.state
    echo "INFO: created kill_switch.state=OK"
else
    echo "INFO: kill_switch.state already exists ($(cat data/runtime_health/kill_switch.state))"
fi

echo "OK: runtime state ready."
