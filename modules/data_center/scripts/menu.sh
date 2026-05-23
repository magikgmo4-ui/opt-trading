#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$ROOT"

echo "=== data_center menu ==="
echo "1) Initialize layout (ensure_data_center_dirs)"
echo "2) Show producers registry"
echo "3) Show consumers registry"
echo "4) Run sanity check"
echo "q) Quit"
echo ""
read -rp "Choice: " choice
case "$choice" in
  1) bash "$SCRIPT_DIR/cmd.sh" ;;
  2) python3 -c "from modules.data_center.layout import load_producers_registry; import json; print(json.dumps(load_producers_registry(), indent=2))" ;;
  3) python3 -c "from modules.data_center.layout import load_consumers_registry; import json; print(json.dumps(load_consumers_registry(), indent=2))" ;;
  4) bash "$SCRIPT_DIR/sanity_check.sh" ;;
  q) exit 0 ;;
  *) echo "Unknown choice"; exit 1 ;;
esac
