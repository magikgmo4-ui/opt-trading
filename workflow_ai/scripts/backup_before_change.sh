#!/usr/bin/env bash
set -euo pipefail

# Backup institutionnel light:
# - crée un dossier backups/<timestamp>_<topic>
# - écrit git status
# - exporte diff.patch (si repo git)
# - génère ROLLBACK.md minimal
#
# Usage:
#   ./scripts/backup_before_change.sh "topic"
#   ./scripts/backup_before_change.sh "fix_fail2ban_menu"

TOPIC="${1:-change}"
TS="$(date +%Y%m%d_%H%M%S)"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT/backups/${TS}_${TOPIC}"

mkdir -p "$OUT_DIR"

echo "[backup] root=$ROOT"
echo "[backup] out=$OUT_DIR"

if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[backup] git detected"
  git -C "$ROOT" status --porcelain=v1 > "$OUT_DIR/git_status.txt" || true
  git -C "$ROOT" status > "$OUT_DIR/git_status_human.txt" || true

  # Export patch (works even if clean => empty patch)
  git -C "$ROOT" diff > "$OUT_DIR/diff.patch" || true
  git -C "$ROOT" diff --name-only > "$OUT_DIR/files_list.txt" || true

  # Also capture HEAD info
  git -C "$ROOT" rev-parse HEAD > "$OUT_DIR/head.txt" || true
  git -C "$ROOT" log -1 --oneline > "$OUT_DIR/head_oneline.txt" || true
else
  echo "[backup] WARNING: not a git repo; creating empty placeholders"
  : > "$OUT_DIR/git_status.txt"
  : > "$OUT_DIR/diff.patch"
  : > "$OUT_DIR/files_list.txt"
fi

cat > "$OUT_DIR/ROLLBACK.md" <<EOF
# Rollback — ${TS}_${TOPIC}

## Si Git dispo
- HEAD avant changement: $(cat "$OUT_DIR/head_oneline.txt" 2>/dev/null || echo "N/A")
- Revenir à HEAD: \`git reset --hard $(cat "$OUT_DIR/head.txt" 2>/dev/null || echo "HEAD")\`
- Ou revert du futur commit: \`git revert <commit>\`

## Si patch
- Patch forward sauvegardé: \`$OUT_DIR/diff.patch\`
- Appliquer reverse: \`git apply -R "$OUT_DIR/diff.patch"\`

## Vérification
- Exécuter sanity du module après rollback.
EOF

echo "[backup] OK"
ls -lah "$OUT_DIR" | sed -n '1,120p'
