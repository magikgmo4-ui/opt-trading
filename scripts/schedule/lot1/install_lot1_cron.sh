#!/usr/bin/env bash
# Installe les entrées cron Lot 1 dans le crontab de l'utilisateur courant.
# Ne touche pas aux entrées existantes.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CRON_SNIPPET="$SCRIPT_DIR/lot1_crontab.txt"
MARKER="GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_CRON_01"

if [[ ! -f "$CRON_SNIPPET" ]]; then
    echo "ERROR: lot1_crontab.txt not found at $CRON_SNIPPET" >&2
    exit 1
fi

# Vérifier si déjà installé
if crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo "INFO: Lot 1 cron already installed (marker found). Run uninstall first to reinstall."
    exit 0
fi

chmod +x "$SCRIPT_DIR/run_readonly_smoke.sh"
mkdir -p /opt/trading/data/logs/cron

# Ajouter le snippet au crontab existant
(crontab -l 2>/dev/null || true; cat "$CRON_SNIPPET") | crontab -

echo "OK: Lot 1 cron entries installed."
echo ""
crontab -l | grep -v '^#' | grep -v '^$' | grep -v '^SHELL\|^REPO\|^PY\|^LOGDIR'
