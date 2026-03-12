#!/usr/bin/env bash
#
# Trae Module Validator - Sanity Check
#
# Self-validates the module structure and basic functionality.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

echo "Checking Trae Module Validator..."

# 1. Structure Check
[ -f "$CMD" ] || { echo "FAIL: cmd.sh missing"; exit 1; }
[ -f "$SCRIPT_DIR/menu.sh" ] || { echo "FAIL: menu.sh missing"; exit 1; }
[ -d "$SCRIPT_DIR/scripts" ] || { echo "FAIL: scripts dir missing"; exit 1; }
[ -f "$SCRIPT_DIR/scripts/validate_module.sh" ] || { echo "FAIL: validate_module.sh missing"; exit 1; }

# 2. Logic Check (Self-Validation)
echo -n "Checking Self-Validation... "
if bash "$CMD" validate "trae_module_validator" | grep -q "RESULT: OK"; then
    echo "OK"
else
    echo "FAIL: Self-validation failed"
    exit 1
fi

echo "Sanity Check Passed."
