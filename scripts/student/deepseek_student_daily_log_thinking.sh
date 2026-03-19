#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Daily Log Report (Deterministic)
# Generates a factual operator report based on system signals and logs

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$ROOT_DIR/data/logs/deepseek_student"
DAILY_ARCHIVE_DIR="$ROOT_DIR/_student_archive/response/daily"
mkdir -p "$DAILY_ARCHIVE_DIR"

TS=$(date -u +"%Y%m%d_%H%M%S")
REPORT_FILE="$DAILY_ARCHIVE_DIR/daily_report_${TS}.md"
DAILY_LINK="$DAILY_ARCHIVE_DIR/daily_latest.md"

echo "=== DeepSeek Student: Daily Log Report (Deterministic) ==="
echo "Date: $(date -u)"

# --- 1. Signal Collection ---

# Timer Status
TIMER_STATUS="INCONNU"
if systemctl --user is-active --quiet deepseek_student_daily_log_thinking.timer; then
    TIMER_STATUS="ACTIF"
else
    TIMER_STATUS="INACTIF"
fi

# Service Status (Last Run)
SERVICE_STATUS="INCONNU"
if systemctl --user is-active --quiet deepseek_student_daily_log_thinking.service; then
    SERVICE_STATUS="EN COURS"
else
    # Check exit code of last run
    if systemctl --user status deepseek_student_daily_log_thinking.service | grep -q "SUCCESS"; then
        SERVICE_STATUS="SUCCÈS (Dernier run)"
    elif systemctl --user status deepseek_student_daily_log_thinking.service | grep -q "FAILED"; then
        SERVICE_STATUS="ÉCHEC (Dernier run)"
    else
        SERVICE_STATUS="INACTIF"
    fi
fi

# Log Analysis
LOG_ERRORS=0
LOG_WARNINGS=0
LOG_SUCCESS=0

if [ -d "$LOGS_DIR" ]; then
    # Analyze last 5 logs
    RECENT_LOGS=$(ls -t "$LOGS_DIR"/*.log 2>/dev/null | head -n 5)
    if [ -n "$RECENT_LOGS" ]; then
        for log in $RECENT_LOGS; do
            ERR=$(grep -c "ERROR" "$log" || true)
            WARN=$(grep -c "WARN" "$log" || true)
            SUCC=$(grep -c "SUCCESS" "$log" || true)
            LOG_ERRORS=$((LOG_ERRORS + ERR))
            LOG_WARNINGS=$((LOG_WARNINGS + WARN))
            LOG_SUCCESS=$((LOG_SUCCESS + SUCC))
        done
    fi
fi

# Artifact Detection
LAST_THINKING=$(ls -t "$ROOT_DIR/_student_archive/thinking"/*.md 2>/dev/null | head -n 1 | xargs basename 2>/dev/null || echo "Aucun")
LAST_RESPONSE=$(ls -t "$ROOT_DIR/_student_archive/response"/*.md 2>/dev/null | head -n 1 | xargs basename 2>/dev/null || echo "Aucun")

# --- 2. Report Generation ---

{
    echo "## RÉSUMÉ EXÉCUTIF"
    if [ "$LOG_ERRORS" -eq 0 ]; then
        echo "- Système STABLE. Timer $TIMER_STATUS. Aucune erreur critique récente."
    else
        echo "- Système À SURVEILLER. $LOG_ERRORS erreurs détectées dans les logs récents."
    fi
    echo ""

    echo "## SUCCÈS NOTABLES"
    echo "- Timer quotidien : $TIMER_STATUS"
    echo "- Service quotidien : $SERVICE_STATUS"
    if [ "$LOG_SUCCESS" -gt 0 ]; then
        echo "- $LOG_SUCCESS opérations réussies détectées dans les logs récents"
    fi
    if [ "$LAST_THINKING" != "Aucun" ]; then
        echo "- Activité Thinking récente : $LAST_THINKING"
    fi
    echo ""

    echo "## ERREURS ET POINTS D'ATTENTION"
    if [ "$LOG_ERRORS" -gt 0 ]; then
        echo "- $LOG_ERRORS erreurs critiques (ERROR) dans les 5 derniers logs"
    fi
    if [ "$LOG_WARNINGS" -gt 0 ]; then
        echo "- $LOG_WARNINGS avertissements (WARN) dans les 5 derniers logs"
    fi
    if [ "$LOG_ERRORS" -eq 0 ] && [ "$LOG_WARNINGS" -eq 0 ]; then
        echo "- Non observé (Logs sains)"
    fi
    echo ""

    echo "## ACTIONS PRIORITAIRES"
    if [ "$TIMER_STATUS" != "ACTIF" ]; then
        echo "1. Activer le timer quotidien : 'deepseek-student install-daily-timer'"
    fi
    if [ "$LOG_ERRORS" -gt 0 ]; then
        echo "1. Analyser les erreurs : 'deepseek-student tail-latest-log'"
        echo "2. Vérifier le service : 'deepseek-student timer-status'"
    elif [ "$LOG_WARNINGS" -gt 0 ]; then
        echo "1. Vérifier les warnings : 'deepseek-student tail-latest-log'"
    else
        echo "1. Aucune action immédiate requise"
        echo "2. Vérification de routine : 'deepseek-student summary'"
    fi
    echo "3. Consulter la doc : 'menu-deepseek-student' (Option 15)"

} > "$REPORT_FILE"

# --- 3. Finalize ---

rm -f "$DAILY_LINK"
ln -s "$REPORT_FILE" "$DAILY_LINK"

echo "Report generated: $REPORT_FILE"
echo "Linked to: $DAILY_LINK"
echo "Use 'deepseek-student show-latest-response' to view it."
