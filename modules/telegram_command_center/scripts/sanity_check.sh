#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MOD_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$MOD_DIR/../.." && pwd)"

passed=0
failed=0

check() {
    local label="$1"
    shift
    if "$@" &>/dev/null; then
        echo "  PASS  $label"
        ((passed++)) || true
    else
        echo "  FAIL  $label"
        ((failed++)) || true
    fi
}

echo "=== telegram_command_center sanity check ==="

check "formatters import" python3 -c "from modules.telegram_command_center.app.formatters import alert, decision_required, info, ops_result"
check "commands import" python3 -c "from modules.telegram_command_center.app.commands import dispatch, COMMANDS"
check "commands registered" python3 -c "from modules.telegram_command_center.app.commands import COMMANDS; assert len(COMMANDS) >= 8"
check "dispatch /help" python3 -c "
from modules.telegram_command_center.app.commands import dispatch
resp, ch = dispatch('/help')
assert 'Command Center' in resp
assert ch is None
"
check "dispatch /status" python3 -c "
from modules.telegram_command_center.app.commands import dispatch
resp, ch = dispatch('/status')
assert ch == 'pipeline'
"
check "dispatch /routes" python3 -c "
from modules.telegram_command_center.app.commands import dispatch
resp, ch = dispatch('/routes')
assert 'Telegram routes' in resp
assert ch == 'ops'
"
check "dispatch unknown" python3 -c "
from modules.telegram_command_center.app.commands import dispatch
resp, ch = dispatch('/nonexistent')
assert 'Unknown command' in resp
"

echo ""
if [[ $failed -eq 0 ]]; then
    echo "RESULT: $passed passed, $failed failed — OK"
    exit 0
else
    echo "RESULT: $passed passed, $failed failed — FAIL"
    exit 1
fi
