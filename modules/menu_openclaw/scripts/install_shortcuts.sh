#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo tee /usr/local/bin/menu-menu_openclaw >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/menu.sh" "\$@"
EOF

sudo tee /usr/local/bin/cmd-menu_openclaw >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/cmd.sh" "\$@"
EOF

sudo tee /usr/local/bin/menu-openclaw >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/menu.sh" "\$@"
EOF

sudo tee /usr/local/bin/cmd-openclaw >/dev/null <<EOF
#!/usr/bin/env bash
exec "$BASE/scripts/cmd.sh" "\$@"
EOF

sudo chmod +x \
  /usr/local/bin/menu-menu_openclaw \
  /usr/local/bin/cmd-menu_openclaw \
  /usr/local/bin/menu-openclaw \
  /usr/local/bin/cmd-openclaw

echo "Shortcuts installés:"
echo "  menu-menu_openclaw"
echo "  cmd-menu_openclaw"
echo "  menu-openclaw"
echo "  cmd-openclaw"
