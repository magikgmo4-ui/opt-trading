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
RECENT_LOGS=$(ls -t "$LOGS_DIR"/*.log 2>/dev/null | head -n 5)

if [ -z "$RECENT_LOGS" ]; then
    echo "No logs found to analyze."
    exit 0
fi

CONTEXT_FILE="/tmp/deepseek_daily_context_${RANDOM}.txt"
echo "--- DAILY LOG CONTEXT ---" > "$CONTEXT_FILE"
for log in $RECENT_LOGS; do
    echo "Log: $(basename "$log")" >> "$CONTEXT_FILE"
    tail -n 100 "$log" >> "$CONTEXT_FILE"
    echo "---" >> "$CONTEXT_FILE"
done

# 2. Build Prompt
PROMPT="Analyse ces logs récents du système DeepSeek Student. Identifie les erreurs récurrentes, les succès notables et propose 3 actions d'amélioration prioritaires. Réponds en FRANÇAIS."

# 3. Run Thinking
# We use the existing 'think' command wrapper, but we want to capture the output specifically
# However, 'think' wrapper logs to its own log file.
# Here we want to capture the thinking output MD file.

CMD_WRAPPER="$SCRIPT_DIR/deepseek_student_cmd.sh"

echo "Running analysis..."
# We pass the content of context file + prompt as the argument
# Note: This might be large, but for a simple daily summary it should fit in args or we'd need a file input mode.
# DeepSeek hub 'think' takes a string.

FULL_PROMPT="$PROMPT $(cat "$CONTEXT_FILE")"

# Execute via wrapper (this will log the execution itself)
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
