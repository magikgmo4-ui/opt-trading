#!/usr/bin/env bash
# safe_rewrite.sh — Réécriture sûre de fichiers sur mount Windows/Linux
#
# PROBLÈME :
#   Les outils d'édition Windows (Edit/Write) écrivent côté Windows.
#   Le mount Linux ne met pas à jour le mtime sur le côté Linux.
#   Python utilise le mtime stocké dans les .pyc pour valider le cache.
#   Si mtime Linux = mtime .pyc → cache considéré valide → fichier tronqué/
#   incohérent ignoré → tests faux ou instables.
#
# SOLUTION :
#   1. Écrire via bash heredoc (cat > fichier << 'EOF') — met à jour le mtime Linux.
#   2. `touch` explicite après écriture pour forcer mtime.
#   3. Suppression ciblée du __pycache__ pour les fichiers Python touchés.
#
# USAGE :
#   ./scripts/safe_rewrite.sh <fichier_cible> <contenu_heredoc_via_stdin>
#
#   Ou utiliser directement dans bash :
#     cat > path/to/file.py << 'EOF'
#     ... contenu complet ...
#     EOF
#     touch path/to/file.py
#     find "$(dirname path/to/file.py)" -name "*.pyc" -path "*__pycache__*" -delete 2>/dev/null || true
#
# RÈGLE OFFICIELLE (voir docs/DEV_CONTRACTS.md) :
#   Pour tout fichier Python/JSON/YAML critique monté via Windows/Linux :
#   - NE PAS utiliser l'Edit tool Windows pour des réécritures complètes.
#   - UTILISER bash heredoc + touch + suppression __pycache__.
#
# -------------------------------------------------------------------

set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
    echo "Usage: $0 <target_file>" >&2
    echo "       Le contenu est lu depuis stdin (heredoc)." >&2
    exit 1
fi

# Crée les dossiers parents si nécessaire
mkdir -p "$(dirname "$TARGET")"

# Écrit le contenu depuis stdin
cat > "$TARGET"

# Force le mtime côté Linux
touch "$TARGET"

# Si c'est un fichier Python, purge le __pycache__ local
if [[ "$TARGET" == *.py ]]; then
    PYDIR="$(dirname "$TARGET")/__pycache__"
    if [[ -d "$PYDIR" ]]; then
        # Suppression best-effort (peut échouer si permissions manquantes)
        find "$PYDIR" -name "$(basename "${TARGET%.py}").*.pyc" -delete 2>/dev/null || true
        echo "[safe_rewrite] __pycache__ purgé : $PYDIR" >&2
    fi
fi

echo "[safe_rewrite] OK : $TARGET (mtime=$(stat -c '%Y' "$TARGET" 2>/dev/null || stat -f '%m' "$TARGET" 2>/dev/null))" >&2
