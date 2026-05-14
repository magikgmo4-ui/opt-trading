# 10_SOURCE_STATE

## Guards

ok:true (verified before scenarios)

## Positions (BEFORE)

| Symbol | Side | Qty | Entry | Status |
|--------|------|-----|-------|--------|
| BTCUSDT | BUY | 0.1 | 50000.0 | OPEN |
| PERFTEST1 | BUY | 10.0 | 50000.0 | OPEN |
| PERFTEST2 | SELL | 10.0 | 49500.0 | OPEN |

## Ledger

- ledger_paper.json: exists, empty `{}`
- ledger_live: does not exist

## Service

tv-webhook.service: active (running), port 8000
