#!/usr/bin/env python3
"""Smoke tests for Botpress ↔ OpenClaw Adapter. Uses spec payload examples."""

import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from adapter_botpress_openclaw import BotpressOpenClawAdapter

results = []

def check(name, expected_status, resp):
    ok = resp.status == expected_status
    results.append(ok)
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}")
    print(f"  Expected: {expected_status} | Got: {resp.status} | Safety: {resp.safety_check}")
    print(f"  Reply: {resp.reply_text[:120]}")
    print()
    return ok

adapter = BotpressOpenClawAdapter()

# Mock gateway for all tests (no localhost dependency)
def mock_gateway(adapter, response):
    adapter._call_gateway = lambda r: response

screener_response = {
    "status": "ok",
    "intent": "screener",
    "result": {
        "data": {"symbol": "BTCUSDT", "price": 67890, "rsi": 52},
        "summary": "**BTCUSDT** 1h: Price 67890 | RSI 52 neutral | MACD bullish",
        "actions_taken": ["market_scan"],
        "warnings": [],
    },
    "trace_id": "trace-mock-001",
}
ok_response = {"status": "ok", "result": {"data": {}, "summary": "OK"}, "trace_id": "mock"}

# ─── TEST 1: Screener BTCUSDT (whitelist) ───
mock_gateway(adapter, screener_response)
check("TEST_01: Screener BTCUSDT (whitelist OK)", "ok", adapter.process({
    "botpress_event_id": "evt-001",
    "telegram_chat_id": "123456789",
    "telegram_user_id": "987654321",
    "intent": "screener",
    "original_message": "/screener BTCUSDT 1h",
    "parsed_params": {"symbol": "BTCUSDT", "timeframe": "1h"},
    "session_context": {},
}))

# ─── TEST 2: execute_trade (blocked) ───
check("TEST_02: Execute trade (BLOCKED)", "blocked", adapter.process({
    "botpress_event_id": "evt-002",
    "telegram_user_id": "987654321",
    "intent": "execute_trade",
    "original_message": "/trade buy BTCUSDT 0.01",
    "parsed_params": {"symbol": "BTCUSDT", "side": "buy", "qty": 0.01},
}))

# ─── TEST 3: help (whitelist) ───
mock_gateway(adapter, ok_response)
check("TEST_03: Help (whitelist OK)", "ok", adapter.process({
    "botpress_event_id": "evt-003",
    "telegram_user_id": "987654321",
    "intent": "help",
    "parsed_params": {},
}))

# ─── TEST 4: analysis (whitelist) ───
check("TEST_04: Analysis (whitelist OK)", "ok", adapter.process({
    "botpress_event_id": "evt-004",
    "telegram_user_id": "987654321",
    "intent": "analysis",
    "parsed_params": {"symbol": "ETHUSDT", "timeframe": "4h"},
}))

# ─── TEST 5: git_push (blocked) ───
check("TEST_05: Git push (BLOCKED)", "blocked", adapter.process({
    "botpress_event_id": "evt-005",
    "telegram_user_id": "987654321",
    "intent": "git_push",
    "parsed_params": {},
}))

# ─── TEST 6: status (whitelist) ───
check("TEST_06: Status cockpit (whitelist OK)", "ok", adapter.process({
    "botpress_event_id": "evt-006",
    "telegram_user_id": "987654321",
    "intent": "status",
    "parsed_params": {},
}))

# ─── TEST 7: journal (whitelist) ───
check("TEST_07: Journal (whitelist OK)", "ok", adapter.process({
    "botpress_event_id": "evt-007",
    "telegram_user_id": "987654321",
    "intent": "journal",
    "parsed_params": {},
}))

# ─── TEST 8: unknown intent (blocked) ───
check("TEST_08: Unknown intent (BLOCKED)", "blocked", adapter.process({
    "botpress_event_id": "evt-008",
    "telegram_user_id": "987654321",
    "intent": "unknown_command",
    "parsed_params": {},
}))

# ─── TEST 9: modify_production (blocked) ───
check("TEST_09: Modify production (BLOCKED)", "blocked", adapter.process({
    "botpress_event_id": "evt-009",
    "telegram_user_id": "987654321",
    "intent": "modify_production",
    "parsed_params": {},
}))

# ─── TEST 10: expose_secret (blocked) ───
check("TEST_10: Expose secret (BLOCKED)", "blocked", adapter.process({
    "botpress_event_id": "evt-010",
    "telegram_user_id": "987654321",
    "intent": "expose_secret",
    "parsed_params": {},
}))

# ─── TEST 11: Rate limit (>10 req/min, separate adapter) ───
adapter_rl = BotpressOpenClawAdapter()
mock_gateway(adapter_rl, ok_response)
# Pre-fill 10 requests
for i in range(10):
    adapter_rl.process({"botpress_event_id": f"prefill-{i}", "telegram_user_id": "rate_limited", "intent": "help", "parsed_params": {}})
# 11th should be rate limited
resp = adapter_rl.process({"botpress_event_id": "evt-011", "telegram_user_id": "rate_limited", "intent": "help", "parsed_params": {}})
check("TEST_11: Rate limit blocked (>10/min)", "error", resp)

# ─── TEST 12: Circuit breaker ───
adapter_cb = BotpressOpenClawAdapter()
mock_gateway(adapter_cb, ok_response)
for _ in range(3):
    adapter_cb.circuit.record_failure()
resp = adapter_cb.process({"botpress_event_id": "evt-012", "telegram_user_id": "cb_user", "intent": "help", "parsed_params": {}})
check("TEST_12: Circuit breaker (error/maintenance)", "error", resp)

# ─── TEST 13: Journalisation active (fresh user to avoid rate limit) ───
resp_log = adapter.process({
    "botpress_event_id": "evt-013",
    "telegram_user_id": "smoke_test_journal",
    "intent": "help",
    "parsed_params": {},
})
logged = len(adapter.logs) > 0
results.append(logged)
tag = "PASS" if logged else "FAIL"
print(f"[{tag}] TEST_13b: Logs recorded ({len(adapter.logs)} entries)")
print()

# ─── SUMMARY ───
passed = sum(results)
total = len(results)
print(f"{'='*50}")
print(f"SMOKE: {passed}/{total} PASS")
print(f"Verdict: {'PASS' if passed == total else 'FAIL'}")
print(f"{'='*50}")
sys.exit(0 if passed == total else 1)
