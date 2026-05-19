#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sudo tee /usr/local/bin/menu-openclaw_config_modulaire >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/menu.sh" "\$@"
EOF
sudo tee /usr/local/bin/cmd-openclaw_config_modulaire >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/cmd.sh" "\$@"
EOF
sudo chmod +x /usr/local/bin/menu-openclaw_config_modulaire /usr/local/bin/cmd-openclaw_config_modulaire
echo "Shortcuts installés:"
echo "  menu-openclaw_config_modulaire"
echo "  cmd-openclaw_config_modulaire"
