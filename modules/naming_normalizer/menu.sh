#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "naming_normalizer"
echo "1) explain-rules"
echo "2) audit current directory"
echo "3) quit"
read -r -p "Choice: " choice

case "${choice:-}" in
  1) bash "$SCRIPT_DIR/cmd.sh" explain-rules ;;
  2) bash "$SCRIPT_DIR/cmd.sh" audit "$(pwd)" ;;
  *) echo "Bye" ;;
esac
