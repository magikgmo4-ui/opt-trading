# GO_OPT_TRADING_ADMIN_TRADING_PAPER_POSITION_CLOSE_01

## Metadata

| Field | Value |
|-------|-------|
| target_machine | admin-trading |
| scope | paper position close |
| payload_sent | none (direct JSON edit) |
| live_trading_impact | none |
| secrets_exposed | none |
| depends_on | PR #356 merged (c1603081) |

## Context

After PAPER_TEST retry, a paper position was opened: BTC/USDT BUY 0.1 @ 65000.0. This GO closes only that position without touching pre-existing paper positions.

## Objectives

1. Verify guards ok:true before action
2. Close only BTC/USDT BUY 0.1 @ 65000.0
3. Leave pre-existing positions unchanged
4. Verify guards still ok:true after action

## Constraints

- Paper mode only
- No real orders
- No live trading
- Don't touch pre-existing positions
- No secrets exposed

## RISKS

- À qualifier.
