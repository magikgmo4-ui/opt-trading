# 10_SOURCE_STATE

## Current State

| Element | State |
|---------|-------|
| sot/mainline | @ 6152413f |
| Guards | ok:true (paper mode) |
| TRADE_ALLOWED | false |
| Risk limits | not implemented |
| Kill switch | not implemented |
| Live trading | inactive |

## Production Readiness Status

- Conditions defined: 7
- Conditions satisfied: 0
- This GO addresses: conditions 3 (risk limits) and 4 (kill switch)

## Service Status

- tv-webhook.service: active (running)
- Port: 8000
- Mode: paper only
