#!/usr/bin/env bash
set -euo pipefail

PASS=0
FAIL=0

assert() {
    local desc="$1" cmd="$2"
    if eval "$cmd" 2>/dev/null; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== daily-session.service exists ==="
assert "service file in repo"         "[[ -f /opt/trading/scripts/schedule/daily-session.service ]]"
assert "timer file in repo"           "[[ -f /opt/trading/scripts/schedule/daily-session.timer ]]"
assert "install script exists"        "[[ -f /opt/trading/scripts/schedule/install_scheduler_service.sh ]]"
assert "uninstall script exists"      "[[ -f /opt/trading/scripts/schedule/uninstall_scheduler_service.sh ]]"
assert "check script exists"          "[[ -f /opt/trading/scripts/schedule/check_scheduler_status.sh ]]"

echo "=== Install ==="
assert "install as root succeeds"     "sudo bash /opt/trading/scripts/schedule/install_scheduler_service.sh 2>&1"
assert "service file in systemd"      "[[ -f /etc/systemd/system/daily-session.service ]]"
assert "timer file in systemd"        "[[ -f /etc/systemd/system/daily-session.timer ]]"
assert "timer is enabled"             "systemctl is-enabled daily-session.timer --quiet 2>/dev/null"
assert "timer is active"              "systemctl is-active daily-session.timer --quiet 2>/dev/null"

echo "=== Run ==="
rm -f /opt/trading/data/journal/daily/20260516_*.json /opt/trading/data/journal/daily/20260516_*.csv
assert "service starts successfully"  "sudo systemctl start daily-session.service 2>&1"
sleep 2
assert "service finished ok"          "journalctl -u daily-session.service --no-pager -n 5 2>&1 | grep -q 'Finished daily-session.service'"
assert "journal JSON generated"       "[[ -f /opt/trading/data/journal/daily/20260516_001.json ]]"
assert "journal all_ok=true"          "python3 -c \"import json; d=json.load(open('/opt/trading/data/journal/daily/20260516_001.json')); assert d['all_ok']==True\""
assert "journal dry_run=true"         "python3 -c \"import json; d=json.load(open('/opt/trading/data/journal/daily/20260516_001.json')); assert d['dry_run']==True\""
assert "journal localcms_ok=true"     "python3 -c \"import json; d=json.load(open('/opt/trading/data/journal/daily/20260516_001.json')); assert d['localcms_ok']==True\""
assert "scheduler log exists"         "[[ -f /opt/trading/data/logs/scheduler/scheduler.log ]]"
assert "scheduler log tmux=true"      "grep -q 'tmux=true' /opt/trading/data/logs/scheduler/scheduler.log"
assert "scheduler log localcms=true"  "grep -q 'localcms=true' /opt/trading/data/logs/scheduler/scheduler.log"
assert "check_status script runs"     "bash /opt/trading/scripts/schedule/check_scheduler_status.sh &>/dev/null"

echo "=== Rollback ==="
assert "uninstall as root succeeds"   "sudo bash /opt/trading/scripts/schedule/uninstall_scheduler_service.sh 2>&1"
assert "service file removed"         "[[ ! -f /etc/systemd/system/daily-session.service ]]"
assert "timer file removed"           "[[ ! -f /etc/systemd/system/daily-session.timer ]]"
assert "timer not in list"            "! systemctl list-timers --all 2>/dev/null | grep -q daily-session"

echo ""
echo "=== Results: $PASS pass, $FAIL fail ==="
[[ $FAIL -eq 0 ]] || exit 1
