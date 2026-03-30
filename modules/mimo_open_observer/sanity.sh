#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

# --- doc pack files ---
required=(
  "$SCRIPT_DIR/README.md"
  "$SCRIPT_DIR/docs/00_SESSION_INDEX_MIMO_OPEN_OBSERVER_V0.txt"
  "$SCRIPT_DIR/docs/06_PSEUDOCODE_PACK_MIMO_OPEN_OBSERVER_V0.md"
  "$SCRIPT_DIR/config/mimo_open_observer.yaml"
  "$SCRIPT_DIR/registry_patch/modules_registry.entry.yaml"
  "$SCRIPT_DIR/registry_patch/wrappers_registry.entries.yaml"
)

for p in "${required[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing: $p" >&2; exit 1; }
done

# --- K1 app package ---
k1_files=(
  "$SCRIPT_DIR/app/__init__.py"
  "$SCRIPT_DIR/app/config.py"
  "$SCRIPT_DIR/app/models.py"
)

for p in "${k1_files[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing K1: $p" >&2; exit 1; }
done

# --- python import + config load ---
python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from app.config import load_config
from app.models import Bar, RawEvent, EnrichedEvent
cfg = load_config()
assert cfg['symbol'] == 'XAUUSD', f\"symbol={cfg['symbol']}\"
assert cfg['scope']['type'] == 'M1x5', f\"scope={cfg['scope']['type']}\"
print('PASS: python imports + config load OK')
" || { echo "FAIL: python sanity" >&2; exit 1; }

echo "PASS: mimo_open_observer K1 sanity OK"
