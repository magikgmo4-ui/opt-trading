#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
MODULE_DIR="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
APP="$MODULE_DIR/app/deploy_module_multi_machine.py"

usage() {
  cat <<'EOF'
Usage:
  deploy_module_multi_machine_cmd.sh status
  deploy_module_multi_machine_cmd.sh plan   --module-name <name> --source-dir <dir> --targets host1,host2 [--dry-run]
  deploy_module_multi_machine_cmd.sh preflight --module-name <name> --source-dir <dir> --targets host1,host2 [--post-install] [--lock-stale-after-seconds <n>]
  deploy_module_multi_machine_cmd.sh deploy --module-name <name> --source-dir <dir> --targets host1,host2 [--dry-run] [--post-install] [--cleanup-stale-lock] [--lock-stale-after-seconds <n>]
  deploy_module_multi_machine_cmd.sh sanity --module-name <name> --source-dir <dir> --targets host1,host2 [--dry-run]

Notes:
- registry root par défaut: /opt/trading/registry
- fallback inventory: modules/deploy_module_multi_machine/config/hosts_fallback.json
- ce module cible uniquement des hôtes POSIX avec /opt/trading
- --post-install lance scripts/install_module.sh sur la cible si present
- --cleanup-stale-lock tente de supprimer un lock stale avant le deploy
- --lock-stale-after-seconds règle le seuil stale lock (défaut: 3600)
EOF
}

if [ "$#" -lt 1 ]; then
  usage
  exit 1
fi

case "$1" in
  -h|--help|help)
    usage
    ;;
  status|plan|preflight|deploy|sanity)
    exec "$PYTHON_BIN" "$APP" "$@"
    ;;
  *)
    echo "Commande inconnue: $1" >&2
    usage
    exit 1
    ;;
esac
