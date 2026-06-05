# 20_CONFIG_SURFACE_DECISION

## Configuration Surfaces Identified

| Surface | Location | Purpose |
|---------|----------|---------|
| Service env file | `/opt/trading/.env` | `EnvironmentFile` in `tv-webhook.service` |
| Router state | `/opt/trading/state/router_state.json` | In-memory engine state |
| Paper ledger | `/opt/trading/state/ledger_paper.json` | Ledger file for paper mode |

## Decision

Use `/opt/trading/.env` for paper flags (RUNNER_MODE, SIMULATION_MODE, TRADE_ALLOWED, LEDGER_PATH).
Clear `active_engine` in `router_state.json`.
Create empty `ledger_paper.json`.

## Why .env

- Already loaded by systemd via `EnvironmentFile=/opt/trading/.env`
- No code changes needed
- Flags read by `evaluate_paper_test_runtime_guards()` from `os.environ`

## Why router_state.json

- `active_engine` is stored in JSON file, not env
- `COINM_SHORT` is aggressive → guard fails
- Must clear to `null` for guard to pass

## Why ledger_paper.json

- Guard checks `LEDGER_PATH` ends in `ledger_paper.json`
- File must exist at specified path
- Empty JSON `{}` sufficient for guard check

## RISKS

- À qualifier.
