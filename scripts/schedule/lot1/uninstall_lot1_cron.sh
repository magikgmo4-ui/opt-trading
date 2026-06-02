#!/usr/bin/env bash
# Supprime les entrées cron Lot 1 du crontab.
set -euo pipefail

MARKER="GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_CRON_01"

if ! crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo "INFO: Lot 1 cron not found in crontab. Nothing to remove."
    exit 0
fi

# Supprimer du marqueur jusqu'à la fin du bloc (dernière ligne vide ou EOF)
tmp=$(mktemp)
crontab -l 2>/dev/null | awk "/$MARKER/{found=1} !found{print}" > "$tmp"
crontab "$tmp"
rm -f "$tmp"

echo "OK: Lot 1 cron entries removed."
