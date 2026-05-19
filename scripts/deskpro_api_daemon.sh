#!/usr/bin/env bash
# Desk Pro API daemon — start|stop|status|restart|logs for port 8010
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$ROOT/tmp/deskpro_api.pid"
LOG_FILE="$ROOT/tmp/uvicorn_8010.log"
PORT=8010
HOST=127.0.0.1

# ---------- helpers ----------------------------------------------------------

_python() {
    if [[ -x "$ROOT/.venv/bin/python3" ]]; then
        echo "$ROOT/.venv/bin/python3"
    else
        echo "python3"
    fi
}

_load_env() {
    if [[ -f "$ROOT/scripts/load_env.sh" ]]; then
        # shellcheck disable=SC1091
        source "$ROOT/scripts/load_env.sh"
    fi
}

_pid_running() {
    local pid="$1"
    [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

_read_pid() {
    if [[ -f "$PID_FILE" ]]; then
        cat "$PID_FILE"
    else
        echo ""
    fi
}

_port_in_use() {
    ss -ltnp 2>/dev/null | grep -q ":${PORT} " || \
    ss -ltnp 2>/dev/null | grep -q ":${PORT}\b"
}

# ---------- subcommands -------------------------------------------------------

cmd_start() {
    local pid
    pid="$(_read_pid)"

    if _pid_running "$pid"; then
        echo "deskpro_api already running (pid $pid)"
        return 0
    fi

    if _port_in_use; then
        echo "ERROR: port $PORT already in use (not by this daemon — check ss -ltnp | grep :$PORT)"
        return 1
    fi

    _load_env
    mkdir -p "$ROOT/tmp"

    local py
    py="$(_python)"

    PERF_DB_PATH="${PERF_DB_PATH:-$ROOT/tmp/perf_test.db}" \
    nohup "$py" -m uvicorn modules.perf.app:app \
        --host "$HOST" \
        --port "$PORT" \
        >> "$LOG_FILE" 2>&1 &

    local new_pid=$!
    echo "$new_pid" > "$PID_FILE"
    echo "deskpro_api started (pid $new_pid) — log: $LOG_FILE"

    # brief wait then health check
    sleep 2
    local health
    health="$(curl -sf "http://${HOST}:${PORT}/desk/health" 2>/dev/null || echo "unreachable")"
    if echo "$health" | grep -q '"ok":.*true'; then
        echo "health: OK"
    else
        echo "health: $health"
    fi
}

cmd_stop() {
    local pid
    pid="$(_read_pid)"

    if ! _pid_running "$pid"; then
        echo "deskpro_api not running"
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
        echo "deskpro_api killed (pid $pid)"
    else
        echo "deskpro_api stopped (pid $pid)"
    fi
    rm -f "$PID_FILE"
}

cmd_status() {
    local pid
    pid="$(_read_pid)"

    if _pid_running "$pid"; then
        echo "deskpro_api RUNNING (pid $pid)"
        local health
        health="$(curl -sf "http://${HOST}:${PORT}/desk/health" 2>/dev/null || echo "unreachable")"
        echo "health: $health"
    else
        echo "deskpro_api STOPPED"
        rm -f "$PID_FILE"
        if _port_in_use; then
            echo "WARNING: port $PORT in use by another process"
        fi
    fi
}

cmd_restart() {
    cmd_stop
    sleep 1
    cmd_start
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
    echo "Usage: $0 {start|stop|status|restart|logs}"
    return 1
}

cd "$ROOT"

case "${1:-}" in
    start)   cmd_start ;;
    stop)    cmd_stop ;;
    status)  cmd_status ;;
    restart) cmd_restart ;;
    logs)    cmd_logs ;;
    *)       usage ;;
esac
