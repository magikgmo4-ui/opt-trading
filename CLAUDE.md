# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Run services (two separate processes)
python3 webhook_server.py        # TV webhook server — port 8000
python3 perf/perf_app.py         # Perf analytics API — port 8010

# Verify (syntax check + smoke + diagnostics)
./scripts/verify_all.sh

# Tests
python3 -m pytest tests/                        # all 714 tests
python3 -m pytest tests/test_foo.py::test_name  # single test
./scripts/smoke.sh                              # live API smoke (needs server running)
./scripts/diagnose.sh                           # system diagnostics
```

No Makefile. No pytest.ini — pytest runs with defaults.

## Architecture

### Two FastAPI services

| Service | File | Port | Persists to |
|---|---|---|---|
| TV Webhook | `webhook_server.py` | 8000 | `state/events.jsonl` |
| Perf Analytics | `perf/perf_app.py` | 8010 | `perf/perf.db` (SQLite, WAL) |

**Data flow:** TradingView alert → `POST /tv` → risk checks → `state/events.jsonl` → optional `POST /perf/event` → `perf/perf.db`

`adapters/webhook_to_perf.py` normalizes the boundary between the two services.

### Key module roles

- `modules/env/env.py` — `load_env()` + `ensure_dirs()` called at the top of every entry point
- `modules/risk_engine/` — risk checks before execution
- `modules/execution_engine/`, `modules/position_engine/` — trade lifecycle
- `modules/decision_engine/app/strategy_logic.py` — hardcoded signal config
- `modules/desk_pro/` — Desk Pro UI surface (mounted at `/desk` in perf_app)
- `shared/logger.py` — `setup_logger(name)` for all modules
- `shared/telegram_notify.py` — Telegram alerts (metrics tracked)

### Strategy tools (`tools/strategy/`)

Standalone backtesting engines, not imported by the live services. Each family (`dca_spot/`, `dca_capital/`, `dca_cfd_short/`, `daily_scalping/`, `weekly_dca/`) has its own `engine.py` state machine, data fetchers, and runner scripts. Results go to `artifacts/results/`.

### Chantier docs pattern

Feature work lives in `docs/chantiers/<GO_ID>/`:
- `00_INITIAL_PROJECT_DOC.md` — concept + rules
- `20_ACCEPTANCE_REPORT.md` — results + verdict

Branch naming: `go/GO_<NAME>_01`. Main branch: `sot/mainline`.

## Gated workflow (from `workflow_ai/.cursorrules`)

Work proceeds in explicit Gates. **Do not write code before Gates 0–3 are validated.** Each deliverable must include:
1. Files modified/created
2. Diff summary (what + why)
3. Commands to run
4. Expected results (how to verify)
5. Rollback steps

Never modify files not explicitly referenced. No gratuitous refactors, renames, or added dependencies.

## Environment

Required `.env` vars at repo root:
```
TV_WEBHOOK_KEY=...      # Webhook signature validation
OPS_ADMIN_KEY=...       # Admin operations
TELEGRAM_BOT_TOKEN=...  # Notifications
TELEGRAM_CHAT_ID=...    # Alert destination
```

Optional: `TRADE_ALLOWED=true`, `PERF_URL=http://127.0.0.1:8010`, `LOG_LEVEL=DEBUG`

## Key reference docs

- `docs/ARCHITECTURE.md` — flux + persistance
- `docs/API.md` — all endpoints with curl examples
- `docs/RUNBOOK.md` — systemd, logs, LAN/Windows ops
- `docs/SCHEMAS.md` — canonical Event → Trade → Perf schema
- `docs/INDEX.md` — full doc navigation
- `schemas/webhook_event_v1.json` — JSON Schema (source of truth for webhook payload)
