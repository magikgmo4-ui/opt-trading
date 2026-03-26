#!/usr/bin/env python3
"""Smoke test minimal pour la validation engine dans /tv."""
import os
import sys

# Set test key BEFORE importing the app (webhook_server reads env at import time)
os.environ["TV_WEBHOOK_KEY"] = "smoke_test_key_2026"

sys.path.insert(0, "/opt/trading")

from fastapi.testclient import TestClient
from webhook_server import app

client = TestClient(app)

BASE_PAYLOAD = {
    "key": "smoke_test_key_2026",
    "signal": "SELL",
    "symbol": "BTCUSDT.P",
    "tf": "H1",
    "price": 68750,
    "sl": 69200,
    "tp": 67200,
    "reason": "smoke test",
}

passed = 0
failed = 0

# Test 1: engine inconnu -> HTTP 400 + "not registered"
r = client.post("/tv", json={**BASE_PAYLOAD, "engine": "UNKNOWN_ENGINE_XYZ"})
if r.status_code == 400 and "not registered" in r.text:
    print("[PASS] engine inconnu -> 400 not registered")
    passed += 1
else:
    print(f"[FAIL] engine inconnu -> {r.status_code} {r.text}")
    failed += 1

# Test 2: engine valide (COINM_SHORT) -> pas de rejet engine
r = client.post("/tv", json={**BASE_PAYLOAD, "engine": "COINM_SHORT"})
if "not registered" not in r.text:
    print(f"[PASS] engine COINM_SHORT passe la validation engine (status={r.status_code})")
    passed += 1
else:
    print(f"[FAIL] engine COINM_SHORT rejete par validation engine: {r.text}")
    failed += 1

print(f"\nResultats: {passed} passed, {failed} failed")
sys.exit(1 if failed > 0 else 0)
