#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Daily AI Report (LLM-based)
# Reads recent logs and triggers a structured AI analysis

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$ROOT_DIR/data/logs/deepseek_student"
# Store daily reports in response/ai_daily to separate from deterministic reports
DAILY_ARCHIVE_DIR="$ROOT_DIR/_student_archive/response/ai_daily"
mkdir -p "$DAILY_ARCHIVE_DIR"

echo "=== DeepSeek Student: Daily AI Report ==="
echo "Date: $(date -u)"

if [ ! -d "$LOGS_DIR" ]; then
    echo "Error: Logs directory not found at $LOGS_DIR"
    exit 1
fi

# 1. Gather recent logs (last 5)
RECENT_LOGS=$(ls -t "$LOGS_DIR"/*.log 2>/dev/null | head -n 5)

if [ -z "$RECENT_LOGS" ]; then
    echo "No logs found to analyze."
    exit 0
fi

CONTEXT_FILE="/tmp/deepseek_daily_ai_context_${RANDOM}.txt"
echo "--- CONTEXTE : LOGS RÉCENTS DU SYSTÈME STUDENT ---" > "$CONTEXT_FILE"
echo "Date de l'analyse : $(date -u)" >> "$CONTEXT_FILE"
echo "" >> "$CONTEXT_FILE"

# Keywords to prioritize for context filtering
KEYWORDS="ERROR|WARN|FAILED|SUCCESS|PASS|Start:|End:|Status:|Latest log linked|archive path final"

for log in $RECENT_LOGS; do
    echo "=== Fichier Log : $(basename "$log") ===" >> "$CONTEXT_FILE"
    
    # Strategy: 
    # 1. Grep lines with key status words
    # 2. Add last 20 lines for recent context
    # 3. Filter out repetitive noise/empty lines
    
    {
        grep -E "$KEYWORDS" "$log" || true
        tail -n 20 "$log"
    } | sort | uniq | grep -vE "^#|^$" | tail -n 50 >> "$CONTEXT_FILE"
    
    echo "" >> "$CONTEXT_FILE"
done

# 2. Build Structured Prompt
PROMPT="Tu es un assistant opérateur expert. Analyse les logs ci-joints du système DeepSeek Student.
Ton objectif est de fournir un RAPPORT FINAL pour l'opérateur.

RÈGLES STRICTES :
- Réponds UNIQUEMENT en FRANÇAIS.
- NE MONTRE JAMAIS ton raisonnement interne.
- Sois CONCIS, PROFESSIONNEL et ACTIONNABLE.
- Si l'information est absente, dis 'Non observé'.
- Ne PAS inventer de problèmes ou de succès non présents dans les logs.

FORMAT DE RÉPONSE OBLIGATOIRE :

## RÉSUMÉ EXÉCUTIF
- [État général en une phrase : Stable / Instable / Critique]

## SUCCÈS NOTABLES
- [Point positif 1 (max 3 puces)]

## ERREURS ET POINTS D'ATTENTION
- [Erreur ou Warning 1 (max 3 puces)]

## ACTIONS PRIORITAIRES
1. [Action immédiate 1]
2. [Action immédiate 2]
3. [Action immédiate 3]

CONTEXTE LOGS :"

# 3. Run Response (NOT Think)
CMD_WRAPPER="$SCRIPT_DIR/deepseek_student_cmd.sh"

echo "Running analysis with Ollama..."
FULL_PROMPT="$PROMPT
$(cat "$CONTEXT_FILE")"

# Execute via wrapper using 'response' command
# This ensures we get the final output, not the raw thinking stream
bash "$CMD_WRAPPER" response "$FULL_PROMPT" > /dev/null 2>&1

# 4. Archive/Move
# The wrapper created a file in _student_archive/response/
# We need to move it to our specific daily archive location
LATEST_RAW_RESPONSE=$(ls -t "$ROOT_DIR/_student_archive/response"/*.md 2>/dev/null | head -n 1)

if [ -n "$LATEST_RAW_RESPONSE" ]; then
    TS=$(date -u +"%Y%m%d_%H%M%S")
    REPORT_FILE="$DAILY_ARCHIVE_DIR/daily_ai_report_${TS}.md"
    mv "$LATEST_RAW_RESPONSE" "$REPORT_FILE"
    
    DAILY_LINK="$DAILY_ARCHIVE_DIR/daily_ai_latest.md"
    rm -f "$DAILY_LINK"
    ln -s "$REPORT_FILE" "$DAILY_LINK"
    
    echo "AI Report generated: $REPORT_FILE"
    echo "Linked to: $DAILY_LINK"
    echo "Use 'deepseek-student show-latest-ai-report' to view it."
else
    echo "Warning: No output file generated."
fi

rm -f "$CONTEXT_FILE"
echo "Daily AI report complete."
