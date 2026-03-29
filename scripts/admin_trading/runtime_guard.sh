#!/usr/bin/env bash
set -euo pipefail

LOOKBACK_SECONDS="${RUNTIME_GUARD_LOOKBACK_SECONDS:-900}"
SUCCESS_LOOKBACK_SECONDS="${RUNTIME_GUARD_SUCCESS_LOOKBACK_SECONDS:-3600}"
NGROK_TRANSIENT_LOOKBACK_SECONDS="${RUNTIME_GUARD_NGROK_TRANSIENT_LOOKBACK_SECONDS:-3600}"
NGROK_ACTIVE_INCIDENT_THRESHOLD="${RUNTIME_GUARD_NGROK_ACTIVE_INCIDENT_THRESHOLD:-3}"
CURL_TIMEOUT="${RUNTIME_GUARD_CURL_TIMEOUT:-3}"

WARN_COUNT=0
FAIL_COUNT=0
PRIMARY_REASON="all critical checks green"
PRIMARY_PRIORITY=999

SERVICE_RESTARTS=()
DETAILS=()

add_detail() {
    DETAILS+=("$1")
}

record_pass() {
    add_detail "PASS: $1"
}

record_info() {
    add_detail "INFO: $1"
}

record_warn() {
    WARN_COUNT=$((WARN_COUNT + 1))
    add_detail "WARN: $1"
}

record_fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    add_detail "FAIL: $1"
}

set_primary_reason() {
    local priority="$1"
    local reason="$2"

    if (( priority < PRIMARY_PRIORITY )); then
        PRIMARY_PRIORITY="$priority"
        PRIMARY_REASON="$reason"
    fi
}

probe_http() {
    local label="$1"
    local url="$2"
    local severity="$3"
    local http_code

    http_code="$(curl -sS -L -o /dev/null -w '%{http_code}' --max-time "$CURL_TIMEOUT" "$url" 2>/dev/null || true)"

    if [[ "$http_code" == "200" ]]; then
        record_pass "$label -> 200 ($url)"
        return
    fi

    if [[ "$severity" == "fail" ]]; then
        set_primary_reason 3 "$label endpoint not healthy (${http_code:-curl_error})"
        record_fail "$label -> ${http_code:-curl_error} ($url)"
    else
        set_primary_reason 3 "$label endpoint not healthy (${http_code:-curl_error})"
        record_warn "$label -> ${http_code:-curl_error} ($url)"
    fi
}

check_service() {
    local unit="$1"
    local severity="$2"
    local active_state
    local sub_state
    local restarts
    local show_output

    if ! show_output="$(systemctl show "$unit" --property=ActiveState --property=SubState --property=NRestarts 2>/dev/null)"; then
        if [[ "$severity" == "fail" ]]; then
            set_primary_reason 1 "$unit status unavailable"
            record_fail "$unit -> systemctl show failed"
        else
            set_primary_reason 1 "$unit status unavailable"
            record_warn "$unit -> systemctl show failed"
        fi
        return
    fi

    active_state="$(printf '%s\n' "$show_output" | awk -F= '/^ActiveState=/{print $2}')"
    sub_state="$(printf '%s\n' "$show_output" | awk -F= '/^SubState=/{print $2}')"
    restarts="$(printf '%s\n' "$show_output" | awk -F= '/^NRestarts=/{print $2}')"

    SERVICE_RESTARTS+=("INFO: $unit NRestarts=${restarts:-unknown}")

    if [[ "$active_state" == "active" && "$sub_state" == "running" ]]; then
        record_pass "$unit -> active/running"
        return
    fi

    if [[ "$severity" == "fail" ]]; then
        set_primary_reason 1 "$unit not ${active_state:-unknown}/${sub_state:-unknown}"
        record_fail "$unit -> ${active_state:-unknown}/${sub_state:-unknown}"
    else
        set_primary_reason 1 "$unit not ${active_state:-unknown}/${sub_state:-unknown}"
        record_warn "$unit -> ${active_state:-unknown}/${sub_state:-unknown}"
    fi
}

journal_lines() {
    local unit="$1"
    local since_seconds="$2"
    journalctl --no-pager --since "${since_seconds} seconds ago" -u "$unit" 2>/dev/null || true
}

count_matches() {
    local text="$1"
    local pattern="$2"
    printf '%s\n' "$text" | python3 -c 'import re, sys; pattern = sys.argv[1]; text = sys.stdin.read(); print(len(re.findall(pattern, text, re.IGNORECASE)))' "$pattern"
}

runner_short_journal="$(journal_lines tv-bitget-runner.service "$LOOKBACK_SECONDS")"
webhook_short_journal="$(journal_lines tv-webhook.service "$LOOKBACK_SECONDS")"
ngrok_short_journal="$(journal_lines ngrok-tv.service "$LOOKBACK_SECONDS")"
combined_runtime_journal="$runner_short_journal
$webhook_short_journal"

runner_success_journal="$(journal_lines tv-bitget-runner.service "$SUCCESS_LOOKBACK_SECONDS")"
webhook_success_journal="$(journal_lines tv-webhook.service "$SUCCESS_LOOKBACK_SECONDS")"
combined_success_journal="$runner_success_journal
$webhook_success_journal"

ngrok_transient_journal="$(journal_lines ngrok-tv.service "$NGROK_TRANSIENT_LOOKBACK_SECONDS")"
ngrok_pattern='heartbeat timeout|starting reconnect loop|reconnect'
ngrok_short_hits="$(count_matches "$ngrok_short_journal" "$ngrok_pattern")"
ngrok_transient_hits="$(count_matches "$ngrok_transient_journal" "$ngrok_pattern")"

echo "=== desk-pro runtime-guard ==="
echo "lookback=${LOOKBACK_SECONDS}s success_lookback=${SUCCESS_LOOKBACK_SECONDS}s ngrok_transient_lookback=${NGROK_TRANSIENT_LOOKBACK_SECONDS}s"
echo

check_service "tv-bitget-runner.service" "fail"
check_service "tv-webhook.service" "fail"
check_service "tv-perf.service" "warn"
check_service "ngrok-tv.service" "fail"

probe_http "dash" "http://127.0.0.1:8000/dash" "fail"
probe_http "perf/open" "http://127.0.0.1:8010/perf/open" "warn"
probe_http "desk/health" "http://127.0.0.1:8010/desk/health" "warn"

if printf '%s\n' "$combined_runtime_journal" | grep -Eqi 'HTTPError|missing in env|POST /tv[^[:cntrl:]]* (400|5[0-9]{2})'; then
    set_primary_reason 2 "critical runtime journal pattern detected"
    record_fail "recent critical journal pattern detected (HTTPError|missing in env|/tv 400|/tv 5xx)"
else
    record_pass "no recent critical journal pattern detected"
fi

if printf '%s\n' "$webhook_success_journal" | grep -Eq 'POST /tv[^[:cntrl:]]* 200'; then
    record_pass "recent /tv success seen via tv-webhook journal"
elif printf '%s\n' "$runner_success_journal" | grep -Eiq "resp=\{'ok': True|resp=\{\"ok\": True"; then
    record_pass "recent /tv success seen via tv-bitget-runner response trace"
elif printf '%s\n' "$combined_success_journal" | grep -Eiq 'POST /tv|sent .* resp='; then
    set_primary_reason 4 "/tv traffic seen without success signal"
    record_warn "recent /tv traffic seen but no success signal observed"
else
    record_info "no recent /tv traffic observed in success window"
fi

if (( ngrok_short_hits >= NGROK_ACTIVE_INCIDENT_THRESHOLD )); then
    set_primary_reason 5 "ngrok reconnect burst suggests active incident"
    record_fail "recent ngrok reconnect/timeout burst detected (${ngrok_short_hits} hits in ${LOOKBACK_SECONDS}s)"
elif (( ngrok_transient_hits > 0 )); then
    set_primary_reason 5 "ngrok reconnect transient recovered"
    record_warn "recent ngrok reconnect/timeout seen but service recovered (${ngrok_transient_hits} hits in ${NGROK_TRANSIENT_LOOKBACK_SECONDS}s)"
else
    record_pass "no recent ngrok heartbeat timeout/reconnect seen"
fi

if (( FAIL_COUNT > 0 )); then
    VERDICT="FAIL"
    EXIT_CODE=2
elif (( WARN_COUNT > 0 )); then
    VERDICT="WARN"
    EXIT_CODE=1
else
    VERDICT="PASS"
    EXIT_CODE=0
fi

echo
printf 'VERDICT: %s -- main cause: %s\n' "$VERDICT" "$PRIMARY_REASON"

for detail in "${DETAILS[@]}"; do
    printf '%s\n' "$detail"
done

for info in "${SERVICE_RESTARTS[@]}"; do
    printf '%s\n' "$info"
done

echo
printf 'VERDICT: %s (warn=%s fail=%s)\n' "$VERDICT" "$WARN_COUNT" "$FAIL_COUNT"
exit "$EXIT_CODE"
