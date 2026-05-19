# 30_PNL_TRACKING_SPEC

## P&L Tracking Requirements

| Metric | Description | Implementation |
|--------|-------------|----------------|
| Per-trade P&L | Profit/loss per individual trade | Calculate on close |
| Daily P&L | Sum of all trades for current day | Daily tracker |
| Cumulative P&L | Total P&L since inception | Persistent counter |
| Unrealized P&L | P&L of open positions | Mark-to-market |
| Max drawdown | Largest peak-to-trough decline | Track high watermark |

## Implementation Plan

### 1. P&L Calculation

```python
def calculate_trade_pnl(entry_price, exit_price, qty, side):
    if side == "LONG":
        return (exit_price - entry_price) * qty
    else:  # SHORT
        return (entry_price - exit_price) * qty
```

### 2. Daily P&L Tracker

File: `/opt/trading/state/daily_pnl.json`

```json
{
    "date": "2026-05-14",
    "pnl": 0.0,
    "trades": 0,
    "wins": 0,
    "losses": 0
}
```

### 3. P&L Endpoint

```
GET /api/pnl
Response: {
    "ok": true,
    "daily": {"pnl": 0.0, "trades": 0},
    "cumulative": {"pnl": 0.0, "trades": 0},
    "unrealized": {"pnl": 0.0, "positions": 0}
}
```

### 4. Integration Points

- **On trade open**: Record entry price, qty, side
- **On trade close**: Calculate realized P&L, update daily/cumulative
- **On position check**: Calculate unrealized P&L

## Current State

- Daily P&L file: EXISTS (`/opt/trading/state/daily_pnl.json`)
- P&L calculation: NOT IMPLEMENTED
- P&L endpoint: NOT IMPLEMENTED
- Position tracking: EXISTS (positions.json)

## Status: SPECIFIED

P&L tracking specified. Implementation required.
