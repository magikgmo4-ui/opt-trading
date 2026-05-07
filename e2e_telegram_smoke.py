#!/usr/bin/env python3
"""E2E Smoke: Telegram webhook → Adapter → Response. Simulated Telegram calls."""

import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from adapter_botpress_openclaw import BotpressOpenClawAdapter

results = []
adapter = BotpressOpenClawAdapter()

def mock_gateway(resp):
    adapter._call_gateway = lambda r: resp

ok = {"status": "ok", "result": {"data": {}, "summary": "OK"}, "trace_id": "mock"}
screener_ok = {
    "status": "ok", "intent": "screener",
    "result": {"data": {"symbol": "BTCUSDT", "price": 67890, "rsi": 52, "trend": "neutral"},
               "summary": "**BTCUSDT** Price 67890 | RSI 52 | Trend neutral", "actions_taken": ["market_scan"], "warnings": []},
    "trace_id": "e2e-001",
}

def e2e(name, intent, params, expected_status, mock_resp=None):
    if mock_resp:
        mock_gateway(mock_resp)
    else:
        mock_gateway(ok)

    # Simule Telegram webhook → Botpress → Adapter
    botpress_event = {
        "botpress_event_id": f"e2e-{name}",
        "telegram_chat_id": "555666777",
        "telegram_user_id": "e2e_user",
        "intent": intent,
        "original_message": params.get("msg", f"/{intent}"),
        "parsed_params": params.get("parsed", {}),
        "session_context": {},
    }

    resp = adapter.process(botpress_event)

    ok_status = resp.status == expected_status
    results.append(ok_status)
    tag = "PASS" if ok_status else "FAIL"
    print(f"[{tag}] {name}")
    print(f"  Intent: {intent} | Expected: {expected_status} | Got: {resp.status} | Safety: {resp.safety_check}")
    reply = resp.reply_text[:100]
    if len(reply) > 80:
        reply = reply[:80] + "..."
    print(f"  Reply: {reply}")
    print(f"  Trace: {resp.trace_id} | {resp.duration_ms}ms")
    print()
    return ok_status

# ─── E2E SCENARIOS ───
e2e("SCENARIO_01: Market scan", "screener",
    {"msg": "/screener BTCUSDT 1h", "parsed": {"symbol": "BTCUSDT", "timeframe": "1h"}},
    "ok", screener_ok)

e2e("SCENARIO_02: Analyse symbol", "analysis",
    {"msg": "/analysis ETHUSDT", "parsed": {"symbol": "ETHUSDT", "timeframe": "4h"}},
    "ok")

e2e("SCENARIO_03: Help", "help",
    {"msg": "/help"}, "ok")

e2e("SCENARIO_04: Journal", "journal",
    {"msg": "/journal today"}, "ok")

e2e("SCENARIO_05: Status GO", "status",
    {"msg": "/status"}, "ok")

e2e("SCENARIO_06: Trade blocked", "execute_trade",
    {"msg": "/trade buy BTCUSDT 0.01", "parsed": {"symbol": "BTCUSDT", "side": "buy"}},
    "blocked")

e2e("SCENARIO_07: Git push blocked", "git_push",
    {"msg": "/push all"}, "blocked")

e2e("SCENARIO_08: Unknown command", "unknown_cmd",
    {"msg": "/blah"}, "blocked")

# Rate limit test: 10 requests to same user
adapter_rl = BotpressOpenClawAdapter()
adapter_rl._call_gateway = lambda r: ok
for i in range(10):
    adapter_rl.process({
        "botpress_event_id": f"rl-{i}", "telegram_user_id": "e2e_rl",
        "intent": "help", "parsed_params": {},
    })
resp = adapter_rl.process({
    "botpress_event_id": "e2e-rl-final", "telegram_user_id": "e2e_rl",
    "intent": "help", "parsed_params": {},
})
results.append(resp.status == "error")
print(f"[{'PASS' if resp.status == 'error' else 'FAIL'}] SCENARIO_09: Rate limit >10/min")
print(f"  Got: {resp.status} | Reply: {resp.reply_text[:80]}")
print()

# Circuit breaker
adapter_cb = BotpressOpenClawAdapter()
adapter_cb._call_gateway = lambda r: ok
for _ in range(3):
    adapter_cb.circuit.record_failure()
resp = adapter_cb.process({
    "botpress_event_id": "e2e-cb", "telegram_user_id": "e2e_cb",
    "intent": "help", "parsed_params": {},
})
results.append(resp.status == "error" and "maintenance" in resp.reply_text)
print(f"[{'PASS' if resp.status == 'error' else 'FAIL'}] SCENARIO_10: Circuit breaker")
print(f"  Got: {resp.status} | Reply: {resp.reply_text[:80]}")
print()

# Structured logging
logged = len(adapter.logs) > 0
results.append(logged)
print(f"[{'PASS' if logged else 'FAIL'}] SCENARIO_11: Structured logging ({len(adapter.logs)} entries)")
print()

# No secrets in logs
for entry in adapter.logs:
    log_str = json.dumps(entry)
    for secret_word in ["token", "secret", "password", "api_key", "bearer"]:
        if secret_word in log_str.lower():
            results.append(False)
            print(f"[FAIL] SCENARIO_12: Secret found in log: {secret_word}")
            break
else:
    results.append(True)
    print(f"[PASS] SCENARIO_12: No secrets in logs")

print()
passed = sum(results)
total = len(results)
print(f"{'='*50}")
print(f"E2E SMOKE: {passed}/{total} PASS")
print(f"Verdict: {'PASS' if passed == total else 'FAIL'}")
print(f"{'='*50}")
sys.exit(0 if passed == total else 1)
