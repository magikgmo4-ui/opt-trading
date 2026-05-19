#!/usr/bin/env bash
set -euo pipefail

echo "=== Airtable Bridge — Sanity Check ==="

if [ -z "${AIRTABLE_API_KEY:-}" ]; then
    echo "FAIL: AIRTABLE_API_KEY is not set"
    exit 1
fi
echo "PASS: AIRTABLE_API_KEY is set"

if [ -z "${AIRTABLE_BASE_ID:-}" ]; then
    echo "FAIL: AIRTABLE_BASE_ID is not set"
    exit 1
fi
echo "PASS: AIRTABLE_BASE_ID is set"

echo "Checking API connectivity (dry-run, no write)..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $AIRTABLE_API_KEY" \
    -H "Content-Type: application/json" \
    "https://api.airtable.com/v0/$AIRTABLE_BASE_ID/" 2>/dev/null || echo "000")

if [ "$STATUS" = "200" ]; then
    echo "PASS: API reachable (HTTP 200)"
elif [ "$STATUS" = "401" ]; then
    echo "WARN: API reachable but unauthorized (HTTP 401) — check token"
elif [ "$STATUS" = "404" ]; then
    echo "WARN: Base ID not found (HTTP 404) — check AIRTABLE_BASE_ID"
else
    echo "WARN: Unexpected HTTP status $STATUS"
fi

echo "=== Sanity check complete ==="
