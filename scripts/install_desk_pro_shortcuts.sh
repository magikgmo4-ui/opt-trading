#!/usr/bin/env bash
set -euo pipefail

BIN_DIR="${BIN_DIR:-/usr/local/bin}"
ROOT="${ROOT:-/opt/trading}"

need() { [[ -f "$ROOT/scripts/$1" ]] || { echo "FAIL: missing $ROOT/scripts/$1"; exit 2; }; }

need "desk_pro_menu.sh"
need "desk_pro_cmd.sh"
need "desk_pro_sanity.sh"
need "load_env.sh"

mkdir -p "$BIN_DIR"

install_wrapper() {
  local name="$1"
  local target="$2"
  local path="$BIN_DIR/$name"

  cat > "$path" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$ROOT"
exec bash "$target" "\$@"
EOF
  chmod +x "$path"
  echo "OK installed: $path"
}

install_wrapper "menu-desk_pro"  "./scripts/desk_pro_menu.sh"
install_wrapper "cmd-desk_pro"   "./scripts/desk_pro_cmd.sh"
install_wrapper "sanity-desk_pro" "./scripts/desk_pro_sanity.sh"

cat > "$BIN_DIR/ui-desk_pro" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
# shellcheck disable=SC1091
source "$ROOT/scripts/load_env.sh"
echo "Desk Pro UI: ${TV_PERF_BASE_URL}/desk/ui"
if [[ "${1:-}" == "curl" ]]; then
  curl -s "${TV_PERF_BASE_URL}/desk/ui" | head -n 40
fi
EOF
chmod +x "$BIN_DIR/ui-desk_pro"
echo "OK installed: $BIN_DIR/ui-desk_pro"

echo
echo "Done. Try:"
echo "  menu-desk_pro"
echo "  sanity-desk_pro"
echo "  cmd-desk_pro health"
