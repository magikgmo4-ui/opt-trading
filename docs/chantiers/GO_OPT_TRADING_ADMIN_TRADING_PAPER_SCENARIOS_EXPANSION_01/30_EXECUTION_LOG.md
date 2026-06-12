# 30_EXECUTION_LOG

## Scenario A: PAPER_SELL_VALID

```bash
curl -sS -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -d '{"engine":"PAPER_TEST","signal":"SELL","symbol":"ETH/USDT","tf":"1h","price":3500.0,"tp":3400.0,"sl":3600.0,"reason":"SCENARIO_A_SELL_VALID"}'
```

Response: `{"ok":true}`
Logs: EXECUTION filled, POSITION UPDATED ETH/USDT SELL

## Scenario B1: PAPER_INVALID_PAYLOAD

```bash
curl -sS -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -d '{"engine":"PAPER_TEST","signal":"BUY"}'
```

Response: `{"detail":"Missing/invalid price or sl for risk sizing"}` (HTTP 400)

## Scenario B2: PAPER_INVALID_SIGNAL

```bash
curl -sS -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -d '{"engine":"PAPER_TEST","signal":"INVALID","symbol":"BTC/USDT","tf":"1h","price":65000.0,"sl":64000.0}'
```

Response: `{"detail":"signal must be BUY or SELL"}` (HTTP 400)

## Scenario C: PAPER_GUARD_FAILURE

Setup:
```python
# Set active_engine=COINM_SHORT
d["active_engine"] = "COINM_SHORT"
```

Guards check: ok:false (active_engine FAIL)

```bash
curl -sS -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -d '{"engine":"PAPER_TEST","signal":"BUY","symbol":"TEST/USDT","tf":"1h","price":100.0,"sl":90.0,"reason":"SCENARIO_C_GUARD_FAIL"}'
```

Response: HTTP 409, PAPER_TEST_RUNTIME_GUARD_FAILED

Cleanup: Restored active_engine=None

## Scenario D: PAPER_LEDGER_REGRESSION

Checks:
- ledger_paper.json: exists, `{}`
- ledger_live: not found
- Events log: PAPER_TEST entries tagged correctly

## Position Cleanup

Removed scenario positions: ETH/USDT, BTC/USDT
Remaining: BTCUSDT, PERFTEST1, PERFTEST2 (pre-existing)

## RISKS

- À qualifier.
