# 20_SCENARIO_MATRIX

| # | Scenario | Description | Expected | Actual | Status |
|---|----------|-------------|----------|--------|--------|
| A | PAPER_SELL_VALID | SELL paper payload | ok:true, position opened | ok:true, ETH/USDT SELL opened | PASS |
| B1 | PAPER_INVALID_PAYLOAD | Missing price/sl | HTTP 400 | 400: Missing/invalid price or sl | PASS |
| B2 | PAPER_INVALID_SIGNAL | Invalid signal value | HTTP 400 | 400: signal must be BUY or SELL | PASS |
| C | PAPER_GUARD_FAILURE | Aggressive engine blocks | HTTP 409 | 409: PAPER_TEST_RUNTIME_GUARD_FAILED | PASS |
| D | PAPER_LEDGER_REGRESSION | Ledger paper only | No ledger_live | Only ledger_paper.json exists | PASS |

## Scenario A: PAPER_SELL_VALID

Payload:
```json
{"engine":"PAPER_TEST","signal":"SELL","symbol":"ETH/USDT","tf":"1h","price":3500.0,"tp":3400.0,"sl":3600.0,"reason":"SCENARIO_A_SELL_VALID"}
```

Result: ok:true, position ETH/USDT SELL 1.0 @ 3500.0 opened via paper adapter.

## Scenario B1: PAPER_INVALID_PAYLOAD

Payload:
```json
{"engine":"PAPER_TEST","signal":"BUY"}
```

Result: HTTP 400, "Missing/invalid price or sl for risk sizing". No side effects.

## Scenario B2: PAPER_INVALID_SIGNAL

Payload:
```json
{"engine":"PAPER_TEST","signal":"INVALID","symbol":"BTC/USDT","tf":"1h","price":65000.0,"sl":64000.0}
```

Result: HTTP 400, "signal must be BUY or SELL". No side effects.

## Scenario C: PAPER_GUARD_FAILURE

Setup: Set active_engine=COINM_SHORT (aggressive)
Guards: ok:false (active_engine FAIL)
Payload: PAPER_TEST BUY TEST/USDT
Result: HTTP 409, "PAPER_TEST_RUNTIME_GUARD_FAILED". No position created.

## Scenario D: PAPER_LEDGER_REGRESSION

Checks:
- ledger_paper.json exists: yes (empty `{}`)
- ledger_live exists: no
- Events log: PAPER_TEST entries properly tagged
- No live ledger contamination: confirmed
