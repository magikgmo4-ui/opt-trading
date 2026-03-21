#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REQUIRED=(
  "$BASE_DIR/spec/00_hf_free_platform_spec_v1.md"
  "$BASE_DIR/spec/01_hf_free_platform_scope_v1.md"
  "$BASE_DIR/kanban/00_hf_free_platform_master_kanban.md"
  "$BASE_DIR/handoff/00_hf_free_platform_recovery_pack.md"
  "$BASE_DIR/spaces/portal_static/index.html"
  "$BASE_DIR/spaces/tools_private/app.py"
)
for f in "${REQUIRED[@]}"; do
  [[ -f "$f" ]] || { echo "FAIL: missing $f"; exit 1; }
done
echo "PASS: hf_free_platform sanity OK"
