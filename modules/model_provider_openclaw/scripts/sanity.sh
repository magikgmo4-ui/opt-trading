#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[sanity] bash syntax"
bash -n "$BASE_DIR/scripts/cmd.sh"
bash -n "$BASE_DIR/scripts/menu.sh"
bash -n "$BASE_DIR/scripts/sanity.sh"

echo "[sanity] python module"
python3 "$BASE_DIR/app/model_provider_openclaw.py" sanity
