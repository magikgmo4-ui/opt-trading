# 50_POSITION_AND_LEDGER_CHECK

## Positions After Scenarios

| Symbol | Side | Qty | Entry | Status | Action |
|--------|------|-----|-------|--------|--------|
| BTCUSDT | BUY | 0.1 | 50000.0 | OPEN | untouched |
| PERFTEST1 | BUY | 10.0 | 50000.0 | OPEN | untouched |
| PERFTEST2 | SELL | 10.0 | 49500.0 | OPEN | untouched |
| ETH/USDT | - | - | - | - | created then removed |
| BTC/USDT | - | - | - | - | created then removed |

## Ledger State

| File | Exists | Content | Status |
|------|--------|---------|--------|
| ledger_paper.json | yes | `{}` | clean |
| ledger_live.json | no | - | correct |

## Non-regression

- Paper positions created during scenarios properly cleaned up
- Pre-existing positions unchanged
- No ledger live created
- No live data contamination

## RISKS

- À qualifier.
