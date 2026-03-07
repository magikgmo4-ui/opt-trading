#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Daily Log Thinking
# Reads recent logs and triggers a response process on them

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$ROOT_DIR/data/logs/deepseek_student"
# Store daily reports in response/daily to separate from raw thinking
DAILY_ARCHIVE_DIR="$ROOT_DIR/_student_archive/response/daily"
mkdir -p "$DAILY_ARCHIVE_DIR"

echo "=== DeepSeek Student: Daily Log Report ==="
echo "Date: $(date -u)"

if [ ! -d "$LOGS_DIR" ]; then
    echo "Error: Logs directory not found at $LOGS_DIR"
    exit 1
fi

# 1. Gather recent logs (last 5)
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
    tail -n 100 "$log" | grep -vE "^#|^$" >> "$CONTEXT_FILE"
    echo "" >> "$CONTEXT_FILE"
done

# 2. Build Structured Prompt
PROMPT="Tu es un assistant opérateur expert. Analyse les logs ci-joints du système DeepSeek Student.
Ton objectif est de fournir un RAPPORT FINAL pour l'opérateur.

RÈGLES STRICTES :
- Réponds UNIQUEMENT en FRANÇAIS.
- NE MONTRE JAMAIS ton raisonnement interne.
- Sois CONCIS, PROFESSIONNEL et ACTIONNABLE.
- Ignore le bruit (chemins de fichiers sans erreur, barres de progression).

FORMAT DE RÉPONSE OBLIGATOIRE :

## RÉSUMÉ EXÉCUTIF
[État général : Stable / Instable / Critique. Une phrase de synthèse.]

## SUCCÈS NOTABLES
- [Point positif 1]
- [Point positif 2]

## ERREURS ET POINTS D'ATTENTION
- [Erreur ou Warning 1]
- [Erreur ou Warning 2]

## ACTIONS PRIORITAIRES
1. [Action immédiate 1]
2. [Action immédiate 2]
3. [Action immédiate 3]

CONTEXTE LOGS :"

# 3. Run Response (NOT Think)
CMD_WRAPPER="$SCRIPT_DIR/deepseek_student_cmd.sh"

echo "Running analysis..."
FULL_PROMPT="$PROMPT
$(cat "$CONTEXT_FILE")"

# Execute via wrapper using 'response' command
# This ensures we get the final output, not the raw thinking stream
bash "$CMD_WRAPPER" response "$FULL_PROMPT"

# 4. Archive/Move (Optional)
# The wrapper created a file in _student_archive/response/
# We can find the latest one and symlink it as 'daily_latest.md'
# Note: We look in response/ folder now
LATEST_RESPONSE=$(ls -t "$ROOT_DIR/_student_archive/response"/*.md 2>/dev/null | head -n 1)

if [ -n "$LATEST_RESPONSE" ]; then
    DAILY_LINK="$DAILY_ARCHIVE_DIR/daily_latest.md"
    rm -f "$DAILY_LINK"
    ln -s "$LATEST_RESPONSE" "$DAILY_LINK"
    echo "Daily report linked to: $DAILY_LINK"
    echo "Use 'deepseek-student show-latest-response' to view it."
else
    echo "Warning: No output file found."
fi

rm -f "$CONTEXT_FILE"
echo "Daily log report complete."
