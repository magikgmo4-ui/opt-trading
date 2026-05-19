#!/usr/bin/env bash
set -euo pipefail
echo "HF FREE PLATFORM MENU"
echo "1) status"
echo "2) tree"
read -r -p "> " CHOICE
case "$CHOICE" in
  1) bash "$(dirname "$0")/hf_free_platform_cmd.sh" status ;;
  2) bash "$(dirname "$0")/hf_free_platform_cmd.sh" tree ;;
  *) echo "Unknown choice" ;;
esac
