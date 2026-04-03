#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sudo tee /usr/local/bin/menu-doctor_openclaw >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/menu.sh" "\$@"
EOF
sudo tee /usr/local/bin/cmd-doctor_openclaw >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/cmd.sh" "\$@"
EOF
sudo chmod +x /usr/local/bin/menu-doctor_openclaw /usr/local/bin/cmd-doctor_openclaw
echo "Shortcuts installes:"
echo "  menu-doctor_openclaw"
echo "  cmd-doctor_openclaw"
