# 10_BEFORE_STATE

## Guards

```json
{
    "ok": true,
    "mode": "PAPER_TEST"
}
```

## Positions (BEFORE)

| Symbol | Side | Qty | Entry | Status | Source |
|--------|------|-----|-------|--------|--------|
| BTCUSDT | BUY | 0.1 | 50000.0 | OPEN | pre-existing |
| PERFTEST1 | BUY | 10.0 | 50000.0 | OPEN | pre-existing |
| PERFTEST2 | SELL | 10.0 | 49500.0 | OPEN | pre-existing |
| BTC/USDT | BUY | 0.1 | 65000.0 | OPEN | PAPER_TEST retry |

## Target Position

- Symbol: BTC/USDT
- Side: BUY
- Qty: 0.1
- Entry: 65000.0
- Source: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01
- Action: CLOSE

## RISKS

- À qualifier.
