#!/usr/bin/env bash
set -euo pipefail
ROOT="${ROOT:-/opt/trading}"
bash "$ROOT/modules/deepseek_hub/scripts/sanity_check_deepseek_hub.sh"
