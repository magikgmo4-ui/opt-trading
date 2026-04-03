#!/usr/bin/env bash
set -euo pipefail
case "${1:-help}" in
  sanity) "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/sanity.sh" ;;
  status) echo "USER=$(whoami)"; echo "CONFIG=$(openclaw config file)"; echo; openclaw config validate; echo; openclaw agents list || true ;;
  validate) openclaw config validate ;;
  config-file) openclaw config file ;;
  wizard) openclaw configure ;;
  dashboard) openclaw dashboard ;;
  agents-list) openclaw agents list ;;
  agents-add) [ -n "${2:-}" ] || { echo "FAIL: nom agent requis" >&2; exit 1; }; openclaw agents add "$2" ;;
  set-identity-from-workspace) [ -n "${2:-}" ] || { echo "FAIL: workspace requis" >&2; exit 1; }; openclaw agents set-identity --workspace "$2" --from-identity ;;
  get) [ -n "${2:-}" ] || { echo "FAIL: path requis" >&2; exit 1; }; openclaw config get "$2" ;;
  set) [ -n "${2:-}" ] || { echo "FAIL: path requis" >&2; exit 1; }; [ -n "${3:-}" ] || { echo "FAIL: value requise" >&2; exit 1; }; openclaw config set "$2" "$3" ;;
  unset) [ -n "${2:-}" ] || { echo "FAIL: path requis" >&2; exit 1; }; openclaw config unset "$2" ;;
  *) echo "Usage: cmd.sh sanity|status|validate|config-file|wizard|dashboard|agents-list|agents-add <name>|set-identity-from-workspace <workspace>|get <path>|set <path> <value>|unset <path>"; exit 1 ;;
esac
