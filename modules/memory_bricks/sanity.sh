#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
STATE_ROOT="$(mktemp -d)"
PAYLOAD_FILE="$STATE_ROOT/brick.json"
trap 'rm -rf "$STATE_ROOT"' EXIT

cat > "$PAYLOAD_FILE" <<'EOF'
{
  "title": "Sanity Brick",
  "type": "decision",
  "summary_short": "Minimal sanity brick",
  "resume_point": "GO_MEMORY_BRICKS_V1_REAL_CLI_SURFACE_MATERIALIZATION_01",
  "tags": ["memory", "sanity"],
  "links": [],
  "decisions": ["sanity"],
  "todo": []
}
EOF

MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" bash "$SCRIPT_DIR/cmd.sh" new --payload-file "$PAYLOAD_FILE" >/dev/null
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" bash "$SCRIPT_DIR/cmd.sh" link --id MB-00001 --target GO-SANITY >/dev/null
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" bash "$SCRIPT_DIR/cmd.sh" index rebuild >/dev/null
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" bash "$SCRIPT_DIR/cmd.sh" query status >/dev/null

if [ ! -f "$STATE_ROOT/bricks/MB-00001.json" ]; then
    echo "sanity failed: brick missing" >&2
    exit 1
fi

if [ ! -f "$STATE_ROOT/index_full.json" ]; then
    echo "sanity failed: index_full.json missing" >&2
    exit 1
fi

echo "memory_bricks sanity ok"
