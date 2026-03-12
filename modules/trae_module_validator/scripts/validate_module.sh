#!/usr/bin/env bash
#
# Trae Module Validator - Core Logic
#
# Validates the structure and compliance of a module against V1 standards.
# Usage: ./validate_module.sh <module_path>
#

set -euo pipefail

MODULE_PATH="${1:-}"

if [ -z "$MODULE_PATH" ]; then
    echo "Usage: $0 <module_path>"
    exit 1
fi

if [ ! -d "$MODULE_PATH" ]; then
    echo "FAIL: Module directory not found: $MODULE_PATH"
    exit 1
fi

MODULE_NAME=$(basename "$MODULE_PATH")
echo "=== Validating Module: $MODULE_NAME ==="

ERRORS=0
WARNINGS=0

# Helper functions
report_pass() {
    echo "PASS: $1"
}

report_fail() {
    echo "FAIL: $1"
    ERRORS=$((ERRORS + 1))
}

report_warn() {
    echo "WARN: $1"
    WARNINGS=$((WARNINGS + 1))
}

# 1. Existence check
if [ -d "$MODULE_PATH" ]; then
    report_pass "Directory exists"
else
    report_fail "Directory missing"
    exit 1
fi

# 2. Standard Scripts Check
# Strategy: Check root scripts first (new standard), then scripts/ dir (legacy but accepted)

HAS_CMD=false
HAS_MENU=false
HAS_SANITY=false

# Check cmd.sh
if [ -f "$MODULE_PATH/cmd.sh" ]; then
    report_pass "cmd.sh found at root"
    HAS_CMD=true
elif [ -f "$MODULE_PATH/scripts/cmd.sh" ]; then
    report_warn "cmd.sh found in scripts/ (legacy location)"
    HAS_CMD=true
else
    report_fail "cmd.sh missing"
fi

# Check menu.sh
if [ -f "$MODULE_PATH/menu.sh" ]; then
    report_pass "menu.sh found at root"
    HAS_MENU=true
elif [ -f "$MODULE_PATH/scripts/menu.sh" ]; then
    report_warn "menu.sh found in scripts/ (legacy location)"
    HAS_MENU=true
else
    report_fail "menu.sh missing"
fi

# Check sanity.sh / sanity_check.sh
if [ -f "$MODULE_PATH/sanity.sh" ]; then
    report_pass "sanity.sh found at root"
    HAS_SANITY=true
elif [ -f "$MODULE_PATH/sanity_check.sh" ]; then
    report_warn "sanity_check.sh found at root (legacy name)"
    HAS_SANITY=true
elif [ -f "$MODULE_PATH/scripts/sanity.sh" ]; then
    report_warn "sanity.sh found in scripts/ (legacy location)"
    HAS_SANITY=true
elif [ -f "$MODULE_PATH/scripts/sanity_check.sh" ]; then
    report_warn "sanity_check.sh found in scripts/ (legacy location)"
    HAS_SANITY=true
else
    report_fail "sanity.sh (or sanity_check.sh) missing"
fi

# 3. Structure Check
if [ -d "$MODULE_PATH/app" ] || [ -d "$MODULE_PATH/lib" ] || [ -d "$MODULE_PATH/scripts" ]; then
    report_pass "Structure seems valid (has app/ or lib/ or scripts/)"
else
    report_fail "Structure invalid (missing app/, lib/ or scripts/)"
fi

# 4. Documentation Check
if [ -f "$MODULE_PATH/README.md" ]; then
    report_pass "README.md found"
else
    report_warn "README.md missing"
fi

# Summary
echo "----------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    if [ "$WARNINGS" -eq 0 ]; then
        echo "RESULT: OK (Module is compliant)"
    else
        echo "RESULT: OK WITH WARNINGS ($WARNINGS warnings)"
    fi
else
    echo "RESULT: FAILED ($ERRORS errors)"
    exit 1
fi
