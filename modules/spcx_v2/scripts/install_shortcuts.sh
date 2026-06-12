#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SCRIPT_NAME="spcx-v2"
TARGET="/usr/local/bin/$SCRIPT_NAME"

cat > "$TARGET" << 'INNER'
#!/usr/bin/env bash
MODDIR="$(dirname "$(readlink -f "$0")")"
# Adjust to your actual repo path
REPO_DIR="/home/fantome/opt-trading-clean"
cd "$REPO_DIR" || exit 1
python3 -m modules.spcx_v2.runner "$@"
INNER

chmod +x "$TARGET"
echo "Installed $SCRIPT_NAME to $TARGET"
