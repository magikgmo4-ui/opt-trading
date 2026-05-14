# GO_OPT_TRADING_ADMIN_TRADING_RUNTIME_SYNC_AFTER_PAPER_GUARDS_01

## Metadata

| Field | Value |
|-------|-------|
| target_machine | admin-trading |
| scope | runtime sync + guards verification |
| payload_sent | none |
| live_trading_impact | none |
| secrets_exposed | none |
| depends_on | PR #346 merged (2df4f09e) |

## Context

PR #346 documented `BLOCKED_NO_RETRY` because `admin-trading:/opt/trading` was not synchronized on `sot/mainline` containing the paper test guards. The runtime returned HTTP 404 on `GET /api/paper/guards`.

After merge of PR #346, the runtime must be synchronized and the guards endpoint verified before any retry of `PAPER_TEST`.

## Objectives

1. Verify `admin-trading:/opt/trading` is on `sot/mainline @ 50df15c3` or newer
2. Restart webhook server to pick up new code
3. Verify `GET /api/paper/guards` returns 200 (not 404)
4. Confirm guards correctly block PAPER_TEST when configuration is missing

## Constraints

- No payload `PAPER_TEST` sent
- No live trading orders
- No configuration changes to runtime flags
- Read-only verification + server restart only
