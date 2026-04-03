#!/usr/bin/env bash
set -euo pipefail

sudo tee /usr/local/bin/menu-install_module_openclaw >/dev/null <<'EOF'
#!/usr/bin/env bash
exec bash /opt/trading/modules/install_module_openclaw/scripts/menu.sh "$@"
EOF

sudo tee /usr/local/bin/cmd-install_module_openclaw >/dev/null <<'EOF'
#!/usr/bin/env bash
exec bash /opt/trading/modules/install_module_openclaw/scripts/cmd.sh "$@"
EOF

sudo chmod +x /usr/local/bin/menu-install_module_openclaw /usr/local/bin/cmd-install_module_openclaw

echo "Shortcuts installés:"
echo "  menu-install_module_openclaw"
echo "  cmd-install_module_openclaw"
