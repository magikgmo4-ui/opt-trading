#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/opt/trading}"

if [[ $EUID -ne 0 ]]; then
  echo "Please run as root: sudo bash $0"
  exit 2
fi

echo "=== Install Desk Pro shortcuts ==="
echo "Repo: $REPO"

# Ensure target scripts exist
for f in "$REPO/scripts/desk_pro_menu.sh" "$REPO/scripts/desk_pro_cmd.sh" "$REPO/scripts/sanity_desk_pro.sh"; do
  [[ -f "$f" ]] || { echo "Missing: $f"; exit 3; }
  chmod +x "$f" || true
done

# Install wrappers into /usr/local/bin (works even if /usr/local/bin is not writable for non-root)
cat > /usr/local/bin/menu-desk_pro <<'EOF'
#!/usr/bin/env bash
exec /opt/trading/scripts/desk_pro_menu.sh "$@"
EOF

cat > /usr/local/bin/cmd-desk_pro <<'EOF'
#!/usr/bin/env bash
exec /opt/trading/scripts/desk_pro_cmd.sh "$@"
EOF

chmod +x /usr/local/bin/menu-desk_pro /usr/local/bin/cmd-desk_pro

echo "OK installed:"
echo "  menu-desk_pro"
echo "  cmd-desk_pro"
