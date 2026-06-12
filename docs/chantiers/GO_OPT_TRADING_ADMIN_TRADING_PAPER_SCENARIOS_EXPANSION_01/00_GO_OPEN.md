# GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01

## Metadata

| Field | Value |
|-------|-------|
| target_machine | admin-trading |
| scope | paper scenarios expansion |
| payload_sent | yes (PAPER_TEST, paper adapter) |
| live_trading_impact | none |
| secrets_exposed | none |

## Objectives

Test additional paper scenarios after complete PAPER_TEST cycle:
1. SELL paper scenario
2. Invalid payload rejection
3. Guard failure blocking
4. Ledger non-regression

## Constraints

- Paper mode only
- No real orders
- No live trading
- Guards ok:true required for valid scenarios

## RISKS

- À qualifier.
