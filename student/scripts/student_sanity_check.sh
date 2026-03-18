#!/usr/bin/env bash
set -euo pipefail

ROOT="/opt/trading/student"

exec bash "$ROOT/scripts/deepseek_hub/sanity_check_deepseek_hub.sh" "$@"
