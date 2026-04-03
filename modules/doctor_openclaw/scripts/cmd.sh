#!/usr/bin/env bash
set -euo pipefail
case "${1:-help}" in
  sanity) "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/sanity.sh" ;;
  quick) openclaw doctor --non-interactive; openclaw config validate; openclaw gateway health; openclaw gateway probe ;;
  deep) openclaw doctor --deep ;;
  repair-safe) openclaw doctor --repair ;;
  generate-token) openclaw doctor --generate-gateway-token ;;
  validate) openclaw config validate ;;
  health) openclaw gateway health ;;
  probe) openclaw gateway probe ;;
  logs) tail -n 120 "/tmp/openclaw/openclaw-$(date +%F).log" 2>/dev/null || ls -lah /tmp/openclaw ;;
  status) echo "USER=$(whoami)"; echo "CONFIG=$(openclaw config file 2>/dev/null || echo ~/.openclaw/openclaw.json)"; openclaw agents list || true ;;
  dashboard) openclaw dashboard ;;
  *) echo "Usage: cmd.sh sanity|quick|deep|repair-safe|generate-token|validate|health|probe|logs|status|dashboard"; exit 1 ;;
esac
