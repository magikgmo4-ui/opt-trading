# GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01

## Metadata

| Field | Value |
|-------|-------|
| target_machine | admin-trading |
| scope | PAPER_TEST execution |
| payload_sent | yes (PAPER_TEST) |
| live_trading_impact | none (paper adapter) |
| secrets_exposed | none |
| depends_on | PR #352 merged (260f0442) |

## Context

After PR #352 merge, paper flags configured and guards returning `ok: true`. This GO sends the first PAPER_TEST payload to verify end-to-end execution through the paper adapter.

## Objectives

1. Verify guards `ok: true` before payload
2. Send PAPER_TEST payload via POST /tv
3. Verify execution through paper adapter
4. Verify position tracking
5. Verify guards still `ok: true` after execution

## Constraints

- No real trades (paper adapter only)
- No live trading activation
- No secrets exposed
