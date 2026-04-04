#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo tee /usr/local/bin/menu-dev_validation_hub >/dev/null <<EOF
#!/usr/bin/env bash
exec bash "$BASE/scripts/menu.sh" "\$@"
EOF
sudo tee /usr/local/bin/cmd-dev_validation_hub >/dev/null <<EOF
#!/usr/bin/env bash
exec bash "$BASE/scripts/cmd.sh" "\$@"
EOF
sudo tee /usr/local/bin/sanity-dev_validation_hub >/dev/null <<EOF
#!/usr/bin/env bash
exec bash "$BASE/scripts/sanity.sh" "\$@"
EOF
sudo chmod +x /usr/local/bin/menu-dev_validation_hub /usr/local/bin/cmd-dev_validation_hub /usr/local/bin/sanity-dev_validation_hub

echo "Shortcuts installés:"
echo "  menu-dev_validation_hub"
echo "  cmd-dev_validation_hub"
echo "  sanity-dev_validation_hub"
