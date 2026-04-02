#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sudo tee /usr/local/bin/menu-configure_openclaw >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/menu.sh" "\$@"
EOF
sudo tee /usr/local/bin/cmd-configure_openclaw >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/cmd.sh" "\$@"
EOF
sudo chmod +x /usr/local/bin/menu-configure_openclaw /usr/local/bin/cmd-configure_openclaw
echo "Shortcuts installés:"
echo "  menu-configure_openclaw"
echo "  cmd-configure_openclaw"
