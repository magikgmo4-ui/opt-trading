#!/usr/bin/env bash
# purge_old_sessions.sh — Purge des sessions archivées > 30 jours
set -euo pipefail

ARCHIVE_DIR="/tmp/opencode"
RETENTION_DAYS=30
REPORT=""

echo "=== PURGE SESSIONS ==="
echo "Date: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
echo "Retention: ${RETENTION_DAYS} jours"
echo "Archive: ${ARCHIVE_DIR}"
echo ""

if [ ! -d "$ARCHIVE_DIR" ]; then
  echo "Aucun repertoire d'archive — arret."
  exit 0
fi

COUNT=0
for f in "$ARCHIVE_DIR"/*.jsonl "$ARCHIVE_DIR"/*.archived; do
  [ -f "$f" ] || continue
  AGE_DAYS=$(( ($(date +%s) - $(stat -c %Y "$f")) / 86400 ))
  if [ "$AGE_DAYS" -gt "$RETENTION_DAYS" ]; then
    echo "Suppression: $(basename "$f") (${AGE_DAYS}j)"
    rm -f "$f"
    REPORT="${REPORT}supprime: $(basename "$f") (${AGE_DAYS}j)\n"
    COUNT=$((COUNT + 1))
  else
    echo "Conserve: $(basename "$f") (${AGE_DAYS}j)"
  fi
done

echo ""
echo "=== RESULTAT ==="
echo "Fichiers purges: ${COUNT}"
if [ "$COUNT" -gt 0 ]; then
  echo -e "$REPORT"
fi
echo "=== FIN PURGE ==="
