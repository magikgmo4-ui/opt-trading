#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$ROOT"

echo "=== data_center: initializing layout ==="
python3 -c "
from modules.data_center.layout import ensure_data_center_dirs
base = ensure_data_center_dirs()
print(f'Layout initialized: {base}')
"
