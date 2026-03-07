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

echo "Archives:"
# Thinking
if [ -d "$THINK_DIR" ]; then
    LAST_THINK=$(ls -t "$THINK_DIR"/*.md 2>/dev/null | head -n 1)
    if [ -n "$LAST_THINK" ]; then
        echo "  Last Thinking: $(basename "$LAST_THINK")"
    else
        echo "  Last Thinking: None"
    fi
else
    echo "  Thinking Dir:  MISSING"
fi

# Response
if [ -d "$RESP_DIR" ]; then
    LAST_RESP=$(ls -t "$RESP_DIR"/*.md 2>/dev/null | head -n 1)
    if [ -n "$LAST_RESP" ]; then
        echo "  Last Response: $(basename "$LAST_RESP")"
    else
        echo "  Last Response: None"
    fi
else
    echo "  Response Dir:  MISSING"
fi

# Roadmap
if [ -d "$ROADMAP_DIR" ]; then
    LAST_ROADMAP=$(ls -t "$ROADMAP_DIR"/*.md 2>/dev/null | head -n 1)
    if [ -n "$LAST_ROADMAP" ]; then
        echo "  Last Roadmap:  $(basename "$LAST_ROADMAP")"
    else
        echo "  Last Roadmap:  None"
    fi
else
    echo "  Roadmap Dir:   MISSING (or empty)"
fi

echo "--------------------------------"

# 3. Model Check (Simple)
if command -v ollama >/dev/null 2>&1; then
    if systemctl is-active --quiet ollama; then
        echo "Ollama:       RUNNING"
    else
        echo "Ollama:       STOPPED (systemctl status ollama)"
    fi
else
    echo "Ollama:       NOT FOUND"
fi

echo "================================"
