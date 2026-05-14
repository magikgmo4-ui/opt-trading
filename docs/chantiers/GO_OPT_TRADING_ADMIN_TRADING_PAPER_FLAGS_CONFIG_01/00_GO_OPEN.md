# GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01

## Metadata

| Field | Value |
|-------|-------|
| target_machine | admin-trading |
| scope | paper flags config |
| payload_sent | none |
| live_trading_impact | none |
| secrets_exposed | none |
| depends_on | PR #348 merged (6a48c1ee) |

## Context

After PR #348 merge, `GET /api/paper/guards` returned HTTP 200 with `ok: false`. Guards correctly blocking because paper flags not configured. This GO configures the required flags to achieve `ok: true`.

## Objectives

1. Configure `RUNNER_MODE=PAPER`, `SIMULATION_MODE=true`, `TRADE_ALLOWED=false`, `LEDGER_PATH` in `/opt/trading/.env`
2. Create paper ledger file
3. Clear `active_engine` in `router_state.json`
4. Restart `tv-webhook.service`
5. Verify `GET /api/paper/guards` returns `ok: true`

## Constraints

- No payload PAPER_TEST sent
- No live trading orders
- No secrets committed
- No db-layer/OpenClaw changes
