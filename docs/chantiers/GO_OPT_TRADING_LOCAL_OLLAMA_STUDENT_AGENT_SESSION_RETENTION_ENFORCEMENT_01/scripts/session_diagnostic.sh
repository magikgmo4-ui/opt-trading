#!/usr/bin/env bash
# session_diagnostic.sh — Diagnostic des sessions agent OpenClaw sur Student
set -euo pipefail

SESSIONS_DIR="/home/openclaw-lab/.openclaw/agents/main/sessions"
ARCHIVE_DIR="/tmp/opencode"
GATEWAY_URL="http://127.0.0.1:18790/health"
OLLAMA_URL="http://127.0.0.1:11434/api/generate"

echo "=== SESSION DIAGNOSTIC ==="
echo "Date: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
echo ""

# 1. Vérifier le gateway
echo "--- Gateway health ---"
if curl -sf "$GATEWAY_URL" >/dev/null 2>&1; then
  echo "STATUS: LIVE"
else
  echo "STATUS: OFFLINE (critique)"
fi
echo ""

# 2. Lister les sessions actives
echo "--- Sessions actives ---"
if [ -d "$SESSIONS_DIR" ]; then
  for f in "$SESSIONS_DIR"/*.jsonl; do
    [ -f "$f" ] || continue
    SESSION_ID=$(basename "$f" .jsonl)
    echo "Session: $SESSION_ID"
    # Compter le nombre de runs
    RUNS=$(sudo grep -c '"type":"message"' "$f" 2>/dev/null || echo "0")
    echo "  Messages (runs): $RUNS"
    # Compter les PROMPT_ERROR
    ERRORS=$(sudo grep -c '"error":"request timed out"' "$f" 2>/dev/null || echo "0")
    echo "  Timeouts: $ERRORS"
    # Vérifier l'âge
    AGE_HOURS=$(( ($(date +%s) - $(stat -c %Y "$f")) / 3600 ))
    echo "  Age: ${AGE_HOURS}h"
    if [ "$ERRORS" -ge 3 ] || [ "$RUNS" -ge 10 ] || [ "$AGE_HOURS" -ge 168 ]; then
      echo "  ** SATURATION DETECTEE **"
    fi
    echo ""
  done
else
  echo "Aucune session active"
fi

# 3. Lister les archives
echo "--- Sessions archivees ---"
if [ -d "$ARCHIVE_DIR" ]; then
  for f in "$ARCHIVE_DIR"/*.jsonl; do
    [ -f "$f" ] || continue
    AGE_DAYS=$(( ($(date +%s) - $(stat -c %Y "$f")) / 86400 ))
    echo "Archive: $(basename "$f") — ${AGE_DAYS}j"
  done
else
  echo "Aucune archive"
fi
echo ""

# 4. Vérifier Ollama
echo "--- Ollama status ---"
curl -sf -o /dev/null -w "HTTP %{http_code}" "$OLLAMA_URL" -d '{"model":"qwen2.5:0.5b-instruct","prompt":"warm","stream":false}' 2>/dev/null && echo " — OK"
echo ""

echo "=== FIN DIAGNOSTIC ==="
