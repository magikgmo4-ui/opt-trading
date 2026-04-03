#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sudo tee /usr/local/bin/menu-trading_lab_v1 >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/menu.sh" "\$@"
EOF
sudo tee /usr/local/bin/cmd-trading_lab_v1 >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/cmd.sh" "\$@"
EOF
sudo tee /usr/local/bin/sanity-trading_lab_v1 >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/sanity.sh" "\$@"
EOF
sudo chmod +x /usr/local/bin/menu-trading_lab_v1 /usr/local/bin/cmd-trading_lab_v1 /usr/local/bin/sanity-trading_lab_v1
echo "Shortcuts installés:"
echo "  menu-trading_lab_v1"
echo "  cmd-trading_lab_v1"
echo "  sanity-trading_lab_v1"
