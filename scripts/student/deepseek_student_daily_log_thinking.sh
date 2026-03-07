#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Daily Log Thinking
# Reads recent logs and triggers a thinking process on them

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$ROOT_DIR/data/logs/deepseek_student"
DAILY_ARCHIVE_DIR="$ROOT_DIR/_student_archive/thinking/daily"
mkdir -p "$DAILY_ARCHIVE_DIR"

echo "=== DeepSeek Student: Daily Log Thinking ==="
echo "Date: $(date -u)"

if [ ! -d "$LOGS_DIR" ]; then
    echo "Error: Logs directory not found at $LOGS_DIR"
    exit 1
fi

# 1. Gather recent logs (last 5, excluding today's thinking if recursive)
# We take the last 200 lines of the 5 most recent logs
# Sort by modification time, newest first, take top 5
RECENT_LOGS=$(ls -t "$LOGS_DIR"/*.log 2>/dev/null | head -n 5)

if [ -z "$RECENT_LOGS" ]; then
    echo "No logs found to analyze."
    exit 0
fi

CONTEXT_FILE="/tmp/deepseek_daily_context_${RANDOM}.txt"
echo "--- CONTEXTE : LOGS RÉCENTS DU SYSTÈME STUDENT ---" > "$CONTEXT_FILE"
echo "Date de l'analyse : $(date -u)" >> "$CONTEXT_FILE"
echo "" >> "$CONTEXT_FILE"

for log in $RECENT_LOGS; do
    echo "=== Fichier Log : $(basename "$log") ===" >> "$CONTEXT_FILE"
    # Filter lines to remove noise, keep relevant info, take last 100 lines
    # Exclude typical progress bars or empty lines if possible
    tail -n 100 "$log" | grep -vE "^#|^$" >> "$CONTEXT_FILE"
    echo "" >> "$CONTEXT_FILE"
done

# 2. Build Structured Prompt
PROMPT="Analyse les logs ci-joints du système DeepSeek Student.
Ton objectif est de fournir un rapport d'état clair et actionnable pour l'opérateur.

RÈGLES :
- Réponds en FRANÇAIS.
- Sois CONCIS et structuré.
- Ignore le bruit (chemins de fichiers sans erreur, barres de progression).
- Concentre-toi sur les états, les transitions, les erreurs et les succès.

STRUCTURE DE LA RÉPONSE ATTENDUE :
1. **RÉSUMÉ EXÉCUTIF** : État général du système (Stable / Instable / Critique).
2. **SUCCÈS NOTABLES** : Ce qui a bien fonctionné récemment.
3. **ERREURS & POINTS D'ATTENTION** : Problèmes détectés, warnings récurrents.
4. **ACTIONS PRIORITAIRES** : 1 à 3 commandes ou vérifications à lancer immédiatement.

CONTEXTE LOGS :"

# 3. Run Thinking
CMD_WRAPPER="$SCRIPT_DIR/deepseek_student_cmd.sh"

echo "Running analysis..."
FULL_PROMPT="$PROMPT
$(cat "$CONTEXT_FILE")"

# Execute via wrapper (this will log the execution itself)
# We use quotes to ensure the multiline prompt is passed correctly
bash "$CMD_WRAPPER" think "$FULL_PROMPT"

# 4. Archive/Move (Optional)
# The wrapper created a file in _student_archive/thinking/
# We can find the latest one and symlink it as 'daily_latest.md'
LATEST_THINKING=$(ls -t "$ROOT_DIR/_student_archive/thinking"/*.md 2>/dev/null | head -n 1)

if [ -n "$LATEST_THINKING" ]; then
    DAILY_LINK="$DAILY_ARCHIVE_DIR/daily_latest.md"
    rm -f "$DAILY_LINK"
    ln -s "$LATEST_THINKING" "$DAILY_LINK"
    echo "Daily analysis linked to: $DAILY_LINK"
    echo "Use 'deepseek-student show-latest-thinking' to view it."
else
    echo "Warning: No output file found."
fi

rm -f "$CONTEXT_FILE"
echo "Daily log thinking complete."
