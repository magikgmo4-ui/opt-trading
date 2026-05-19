#!/usr/bin/env bash
# Desk Pro watchdog — active health polling for ports 8000/8010
# Subcommands: start|stop|status|run-once
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$ROOT/tmp/deskpro_watchdog.pid"
LOG_FILE="$ROOT/tmp/deskpro_watchdog.log"
INTERVAL="${WATCHDOG_INTERVAL:-60}"   # seconds between polls

HOST_8000=127.0.0.1
PORT_8000=8000
HOST_8010=127.0.0.1
PORT_8010=8010

# ---------- helpers ----------------------------------------------------------

_ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

_log() { echo "[$(_ts)] $*" | tee -a "$LOG_FILE"; }

_pid_running() {
    local pid="$1"
    [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

_read_pid() {
    [[ -f "$PID_FILE" ]] && cat "$PID_FILE" || echo ""
}

_port_up() {
    local host="$1" port="$2"
    ss -ltnp 2>/dev/null | grep -q ":${port} " || \
    ss -ltnp 2>/dev/null | grep -q ":${port}\b"
}

_health_ok() {
    curl -sf "http://${HOST_8010}:${PORT_8010}/desk/health" 2>/dev/null | grep -q '"ok":.*true'
}

# ---------- single poll ------------------------------------------------------

_poll() {
    local issues=0

    # port 8000
    if _port_up "$HOST_8000" "$PORT_8000"; then
        _log "HEARTBEAT port=${PORT_8000} status=UP"
    else
        _log "WARN port=${PORT_8000} status=DOWN"
        issues=$(( issues + 1 ))
    fi

    # port 8010 + health endpoint
    if _port_up "$HOST_8010" "$PORT_8010"; then
        if _health_ok; then
            _log "HEARTBEAT port=${PORT_8010} status=UP health=ok"
        else
            _log "WARN port=${PORT_8010} status=UP health=FAIL"
            issues=$(( issues + 1 ))
        fi
    else
        _log "WARN port=${PORT_8010} status=DOWN"
        issues=$(( issues + 1 ))
    fi

    # desk/status webhook check
    local wh_check
    wh_check=$(curl -sf "http://${HOST_8010}:${PORT_8010}/desk/status" 2>/dev/null \
        | python3 -c "import sys,json; d=json.load(sys.stdin); h=d['health']; checks=' '.join(f'{c[\"check\"]}:{c[\"status\"]}' for c in h['checks']); print(f'{h[\"status\"]} {checks}')" 2>/dev/null \
        || echo "unreachable")
    _log "STATUS health=${wh_check}"

    if (( issues > 0 )); then
        _log "ALERT issues=${issues} — check services"
    fi

    return "$issues"
}

# ---------- subcommands -------------------------------------------------------

cmd_run_once() {
    mkdir -p "$ROOT/tmp"
    _poll || true
}

cmd_start() {
    local pid
    pid="$(_read_pid)"
    if _pid_running "$pid"; then
        echo "deskpro_watchdog already running (pid $pid)"
        return 0
    fi

    mkdir -p "$ROOT/tmp"
    _log "WATCHDOG starting — interval=${INTERVAL}s"

    (
        while true; do
            _poll || true
            sleep "$INTERVAL"
        done
    ) >> "$LOG_FILE" 2>&1 &

    local new_pid=$!
    echo "$new_pid" > "$PID_FILE"
    echo "deskpro_watchdog started (pid $new_pid) — log: $LOG_FILE"
}

cmd_stop() {
    local pid
    pid="$(_read_pid)"
    if ! _pid_running "$pid"; then
        echo "deskpro_watchdog not running"
        rm -f "$PID_FILE"
        return 0
    fi
    kill "$pid"
    local i=0
    while _pid_running "$pid" && (( i < 10 )); do
        sleep 1
        i=$(( i + 1 ))
    done
    if _pid_running "$pid"; then
        kill -9 "$pid" 2>/dev/null || true
        echo "deskpro_watchdog killed (pid $pid)"
    else
        echo "deskpro_watchdog stopped (pid $pid)"
    fi
    rm -f "$PID_FILE"
}

cmd_status() {
    local pid
    pid="$(_read_pid)"
    if _pid_running "$pid"; then
        echo "deskpro_watchdog RUNNING (pid $pid)"
        echo "log: $LOG_FILE"
        tail -3 "$LOG_FILE" 2>/dev/null | sed 's/^/  /'
    else
        echo "deskpro_watchdog STOPPED"
        rm -f "$PID_FILE"
    fi
}

cmd_logs() {
    if [[ -f "$LOG_FILE" ]]; then
        tail -f "$LOG_FILE"
    else
        echo "log file not found: $LOG_FILE"
        return 1
    fi
}

# ---------- dispatch ----------------------------------------------------------

usage() {
    echo "Usage: $0 {start|stop|status|run-once|logs}"
    echo "  WATCHDOG_INTERVAL=<sec>  poll interval (default: 60)"
    return 1
}

cd "$ROOT"

case "${1:-}" in
    start)    cmd_start ;;
    stop)     cmd_stop ;;
    status)   cmd_status ;;
    run-once) cmd_run_once ;;
    logs)     cmd_logs ;;
    *)        usage ;;
esac
