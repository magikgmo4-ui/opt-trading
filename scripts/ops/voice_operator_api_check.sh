#!/usr/bin/env bash
set -euo pipefail
# Voice Operator API health check
echo "=== voice_operator_api ==="

# Port check
if ss -lntp | grep -q ':8020 '; then
    echo "✅ port 8020 listening"
else
    echo "❌ port 8020 NOT listening"
    exit 1
fi

# Health
if curl -s http://127.0.0.1:8020/health | grep -q '"ok":true'; then
    echo "✅ /health OK"
else
    echo "⚠️ /health failed"
fi

# Read endpoints
for ep in /read/system "/read/spacex" "/read/setup?symbol=BTC"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 "http://127.0.0.1:8020$ep")
    if [ "$code" = "200" ]; then
        echo "✅ $ep → $code"
    else
        echo "❌ $ep → $code"
    fi
done
