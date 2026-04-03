#!/usr/bin/env bash
set -euo pipefail

BACKUP_ROOT="$HOME/openclaw_module_backups"
OPENCLAW_DIR="$HOME/.openclaw"
CFG="$OPENCLAW_DIR/openclaw.json"
CFG_D="$OPENCLAW_DIR/config.d"

TARGET="${1:-}"
if [ -z "$TARGET" ]; then
  TARGET="$(ls -dt "$BACKUP_ROOT"/openclaw_config_modulaire_* 2>/dev/null | head -n1 || true)"
fi

if [ -z "$TARGET" ] || [ ! -d "$TARGET" ]; then
  echo "FAIL: backup introuvable" >&2
  exit 1
fi

cp "$TARGET/openclaw.json.before" "$CFG"
if [ -d "$TARGET/config.d.before" ]; then
  rm -rf "$CFG_D"
  cp -r "$TARGET/config.d.before" "$CFG_D"
fi

openclaw config validate
echo "Rollback OK depuis: $TARGET"
