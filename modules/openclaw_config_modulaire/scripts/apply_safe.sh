#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$BASE/app"
OPENCLAW_DIR="$HOME/.openclaw"
CFG="$OPENCLAW_DIR/openclaw.json"
CFG_D="$OPENCLAW_DIR/config.d"
BACKUP_ROOT="$HOME/openclaw_module_backups"
STAMP="$(date +%Y%m%d_%H%M%S)"
THIS_BACKUP="$BACKUP_ROOT/openclaw_config_modulaire_$STAMP"
CANDIDATE="$THIS_BACKUP/openclaw.json.candidate"

mkdir -p "$CFG_D" "$THIS_BACKUP"

echo "[1/8] Sanity..."
"$BASE/scripts/sanity.sh"

echo "[2/8] Backup..."
cp "$CFG" "$THIS_BACKUP/openclaw.json.before"
if [ -d "$CFG_D" ]; then
  cp -r "$CFG_D" "$THIS_BACKUP/config.d.before"
fi

echo "[3/8] Extraction du token gateway..."
TOKEN="$(python3 - <<'PY'
import json, pathlib
cfg = pathlib.Path.home()/'.openclaw'/'openclaw.json'
data = json.loads(cfg.read_text())
print((((data.get('gateway') or {}).get('auth') or {}).get('token')) or "")
PY
)"
if [ -z "$TOKEN" ]; then
  echo "FAIL: token gateway introuvable" >&2
  exit 1
fi

echo "[4/8] Préparation du candidat racine..."
python3 - <<PY
from pathlib import Path
tpl = Path(r"$APP/openclaw_root_template.json5").read_text()
tpl = tpl.replace("__OPENCLAW_GATEWAY_TOKEN__", r"$TOKEN")
Path(r"$CANDIDATE").write_text(tpl)
print("Candidate:", r"$CANDIDATE")
PY

echo "[5/8] Installation des sous-fichiers..."
cp "$APP/agents.json5" "$CFG_D/agents.json5"
cp "$APP/tools.json5" "$CFG_D/tools.json5"

echo "[6/8] Installation du fichier racine..."
cp "$CANDIDATE" "$CFG"

echo "[7/8] Validation..."
if openclaw config validate; then
  echo "PASS: validation OK"
else
  echo "FAIL: validation échouée, rollback immédiat..." >&2
  cp "$THIS_BACKUP/openclaw.json.before" "$CFG"
  if [ -d "$THIS_BACKUP/config.d.before" ]; then
    rm -rf "$CFG_D"
    cp -r "$THIS_BACKUP/config.d.before" "$CFG_D"
  fi
  openclaw config validate || true
  exit 1
fi

echo "[8/8] Terminé."
echo "Backup courant: $THIS_BACKUP"
echo "Étapes suivantes:"
echo "  openclaw gateway run"
echo "  openclaw gateway health"
echo "  openclaw gateway probe"
