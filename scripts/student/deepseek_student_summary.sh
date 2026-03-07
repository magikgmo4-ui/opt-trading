#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Summary
# Displays recent activity and system status

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== DeepSeek Student Summary ==="
echo "Repo Root:    $ROOT_DIR"
echo "Date:         $(date -u)"
echo "--------------------------------"

# 1. Logs
LOGS_DIR="$ROOT_DIR/data/logs/deepseek_student"
LATEST_LOG="$LOGS_DIR/latest.log"

if [ -d "$LOGS_DIR" ]; then
    COUNT=$(ls "$LOGS_DIR"/*.log 2>/dev/null | wc -l)
    echo "Logs Dir:     $LOGS_DIR ($COUNT files)"
    if [ -L "$LATEST_LOG" ]; then
        REAL_LOG=$(readlink -f "$LATEST_LOG")
        echo "Latest Log:   $(basename "$REAL_LOG") ($(stat -c %y "$REAL_LOG" 2>/dev/null || echo 'unknown date'))"
    else
        echo "Latest Log:   None"
    fi
else
    echo "Logs Dir:     MISSING"
fi

echo "--------------------------------"

# 2. Archives (Thinking / Response / Roadmap)
ARCHIVE_DIR="$ROOT_DIR/_student_archive"
THINK_DIR="$ARCHIVE_DIR/thinking"
RESP_DIR="$ARCHIVE_DIR/response"
ROADMAP_DIR="$ARCHIVE_DIR/roadmap"
DAILY_DIR="$ARCHIVE_DIR/thinking/daily"

echo "Archives:"
# Thinking
if [ -d "$THINK_DIR" ]; then
    LAST_THINK=$(ls -t "$THINK_DIR"/*.md 2>/dev/null | head -n 1)
    echo "  Last Thinking: ${LAST_THINK:+$(basename "$LAST_THINK")}"
else
    echo "  Thinking Dir:  MISSING"
fi

# Response
if [ -d "$RESP_DIR" ]; then
    # Check for Daily Report first
    DAILY_REP="$RESP_DIR/daily/daily_latest.md"
    LAST_STD=$(ls -t "$RESP_DIR"/*.md 2>/dev/null | grep -v "/daily/" | head -n 1)
    
    if [ -L "$DAILY_REP" ] || [ -f "$DAILY_REP" ]; then
        echo "  Daily Report:  $(basename $(readlink -f "$DAILY_REP"))"
    else
        echo "  Daily Report:  None"
    fi
    
    if [ -n "$LAST_STD" ]; then
        echo "  Last Standard: $(basename "$LAST_STD")"
    else
        echo "  Last Standard: None"
    fi
else
    echo "  Response Dir:  MISSING"
fi

# Roadmap
if [ -d "$ROADMAP_DIR" ]; then
    LAST_ROADMAP=$(ls -t "$ROADMAP_DIR"/*.md 2>/dev/null | head -n 1)
    echo "  Last Roadmap:  ${LAST_ROADMAP:+$(basename "$LAST_ROADMAP")}"
else
    echo "  Roadmap Dir:   MISSING (or empty)"
fi

# Daily Thinking
if [ -d "$DAILY_DIR" ]; then
    LAST_DAILY=$(ls -t "$DAILY_DIR"/*.md 2>/dev/null | head -n 1)
    echo "  Daily Latest:  ${LAST_DAILY:+$(basename "$LAST_DAILY")}"
else
    echo "  Daily Dir:     MISSING (or empty)"
fi

echo "--------------------------------"

# 3. System Status (Timer & Model)
echo "System Status:"

# Timer Status
SERVICE_NAME="deepseek_student_daily_log_thinking"
if systemctl --user is-active --quiet "${SERVICE_NAME}.timer"; then
    echo "  Daily Timer:   ACTIVE"
else
    echo "  Daily Timer:   INACTIVE (systemctl --user status ${SERVICE_NAME}.timer)"
fi

# Model Status
if command -v ollama >/dev/null 2>&1; then
    if systemctl is-active --quiet ollama; then
        echo "  Ollama:        RUNNING"
    else
        echo "  Ollama:        STOPPED (systemctl status ollama)"
    fi
else
    echo "  Ollama:        NOT FOUND"
fi

echo "================================"
