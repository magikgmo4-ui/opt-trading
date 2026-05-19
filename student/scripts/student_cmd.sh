#!/usr/bin/env bash
set -euo pipefail

ROOT="/opt/trading/student"

exec bash "$ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh" "$@"
