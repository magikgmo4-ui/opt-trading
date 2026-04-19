#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

echo "KIL V1"
echo "1) Run sample campaign"
echo "2) Show help"
read -r -p "Choice [1-2]: " choice

case "$choice" in
    1)
        read -r -p "Workspace path: " workspace
        bash "$SCRIPT_DIR/cmd.sh" sample --workspace "$workspace"
        ;;
    2)
        bash "$SCRIPT_DIR/cmd.sh" help
        ;;
    *)
        echo "Unknown choice" >&2
        exit 1
        ;;
esac
