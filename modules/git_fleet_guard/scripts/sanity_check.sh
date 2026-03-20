#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
MODULE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

echo "=== sanity (git_fleet_guard) ==="

test -f "$MODULE_ROOT/app/git_fleet_guard.py"
test -f "$MODULE_ROOT/config/machines.default.json"
test -x "$SCRIPT_DIR/cmd.sh"
test -x "$SCRIPT_DIR/menu.sh"

python3 -m py_compile "$MODULE_ROOT/app/git_fleet_guard.py"

TMP_REPO="$(mktemp -d)"
TMP_REPORTS="$(mktemp -d)"
TMP_CFG="$(mktemp)"
cleanup() {
  rm -rf "$TMP_REPO" "$TMP_REPORTS" "$TMP_CFG"
}
trap cleanup EXIT

git -C "$TMP_REPO" init -q
git -C "$TMP_REPO" config user.email "sanity@example.local"
git -C "$TMP_REPO" config user.name "sanity"
echo "hello" > "$TMP_REPO/README.md"
git -C "$TMP_REPO" add README.md
git -C "$TMP_REPO" commit -q -m "init"

cat > "$TMP_CFG" <<EOF
{
  "machines": [
    {
      "name": "localhost",
      "ssh_target": "localhost",
      "repo_path": "$TMP_REPO",
      "local_names": ["localhost"]
    }
  ]
}
EOF

"$CMD" status --config "$TMP_CFG" --reports-dir "$TMP_REPORTS" >/dev/null
"$CMD" audit --config "$TMP_CFG" --machines localhost --repo-path "$TMP_REPO" --reports-dir "$TMP_REPORTS" --no-fetch >/dev/null
test -f "$TMP_REPORTS/latest.json"
test -f "$TMP_REPORTS/latest.md"
"$CMD" report --reports-dir "$TMP_REPORTS" --format json >/dev/null
"$CMD" report --reports-dir "$TMP_REPORTS" --format md >/dev/null

echo "PASS: git_fleet_guard sanity OK"
