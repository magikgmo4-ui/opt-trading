#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"
CONFIG_DIR="$SCRIPT_DIR/config"
OUTPUT_DIR="$SCRIPT_DIR/output"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Checking naming_normalizer..."

[[ -f "$CMD" ]] || { echo "FAIL: cmd.sh missing"; exit 1; }
[[ -f "$CONFIG_DIR/naming_rules.json" ]] || { echo "FAIL: naming_rules.json missing"; exit 1; }
[[ -f "$CONFIG_DIR/exceptions.json" ]] || { echo "FAIL: exceptions.json missing"; exit 1; }

echo -n "Checking Help... "
if bash "$CMD" help | grep -q "Usage:"; then
  echo "OK"
else
  echo "FAIL"
  exit 1
fi

echo -n "Checking Rules... "
if bash "$CMD" explain-rules | grep -q "Surfaces"; then
  echo "OK"
else
  echo "FAIL"
  exit 1
fi

echo -n "Checking Audit... "
mkdir -p "$OUTPUT_DIR"
if bash "$CMD" audit "$REPO_ROOT" --output-dir "$OUTPUT_DIR" > /dev/null; then
  [[ -f "$OUTPUT_DIR/naming_audit_report.md" ]] || { echo "FAIL: markdown report missing"; exit 1; }
  [[ -f "$OUTPUT_DIR/naming_audit_report.json" ]] || { echo "FAIL: json report missing"; exit 1; }
  echo "OK"
else
  echo "FAIL"
  exit 1
fi

echo "Sanity Check Passed."
