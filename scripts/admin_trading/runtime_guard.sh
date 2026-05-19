#!/usr/bin/env bash
set -euo pipefail

LOOKBACK_SECONDS="${RUNTIME_GUARD_LOOKBACK_SECONDS:-900}"
CURL_TIMEOUT="${RUNTIME_GUARD_CURL_TIMEOUT:-3}"

WARN_COUNT=0
FAIL_COUNT=0
DETAILS=()
PRIMARY_REASON="all critical checks green"
PRIMARY_PRIORITY=999

add_detail() {
  DETAILS+=("$1")
}

record_pass() {
  add_detail "PASS: $1"
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

check_service() {
  local unit="$1"
  local severity="$2"
  local active

  active="$(systemctl is-active "$unit" 2>/dev/null || true)"
  if [[ "$active" == "active" ]]; then
    record_pass "$unit active"
    return
  fi

  if [[ "$severity" == "fail" ]]; then
    set_primary_reason 1 "$unit not active"
    record_fail "$unit -> ${active:-unknown}"
  else
    set_primary_reason 1 "$unit degraded"
    record_warn "$unit -> ${active:-unknown}"
  fi
}

probe_http() {
  local label="$1"
  local url="$2"
  local severity="$3"
  local code

  code="$(curl -sS -L -o /dev/null -w '%{http_code}' --max-time "$CURL_TIMEOUT" "$url" 2>/dev/null || true)"
  if [[ "$code" == "200" ]]; then
    record_pass "$label -> 200"
    return
  fi

  if [[ "$severity" == "fail" ]]; then
    set_primary_reason 2 "$label endpoint not healthy"
    record_fail "$label -> ${code:-curl_error}"
  else
    set_primary_reason 2 "$label endpoint degraded"
    record_warn "$label -> ${code:-curl_error}"
  fi
}

recent_journal_has_errors() {
  local units=("$@")
  local combined=""
  local unit
  for unit in "${units[@]}"; do
    combined+="$(journalctl --no-pager --since "${LOOKBACK_SECONDS} seconds ago" -u "$unit" 2>/dev/null || true)"
    combined+=$'\n'
  done

  if printf '%s\n' "$combined" | grep -Eqi 'HTTPError|missing in env|POST /tv.* (400|5[0-9][0-9])'; then
    return 0
  fi
  return 1
}

echo "=== admin-trading runtime guard ==="
echo "lookback=${LOOKBACK_SECONDS}s"
echo

check_service "tv-bitget-runner.service" "fail"
check_service "tv-webhook.service" "fail"
check_service "ngrok-tv.service" "fail"
check_service "tv-perf.service" "warn"

probe_http "dash" "http://127.0.0.1:8000/dash" "fail"
probe_http "perf/open" "http://127.0.0.1:8010/perf/open" "warn"
probe_http "desk/health" "http://127.0.0.1:8010/desk/health" "warn"

if recent_journal_has_errors "tv-bitget-runner.service" "tv-webhook.service"; then
  set_primary_reason 3 "critical runtime journal pattern detected"
  record_fail "recent critical runtime journal pattern detected"
else
  record_pass "no recent critical runtime journal pattern detected"
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

echo
printf 'VERDICT: %s (warn=%s fail=%s)\n' "$VERDICT" "$WARN_COUNT" "$FAIL_COUNT"
exit "$EXIT_CODE"
