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

### Three FastAPI services

| Service | File | Port | Persists to |
|---|---|---|---|
| TV Webhook | `webhook_server.py` | 8000 | `state/events.jsonl` |
| Perf Analytics | `perf/perf_app.py` | 8010 | `perf/perf.db` (SQLite, WAL) |
| LocalCMS | `modules/localcms/app.py` | 8700 | read-only — no writes |

**Data flow:** TradingView alert → `POST /tv` → risk checks → `state/events.jsonl` → optional `POST /perf/event` → `perf/perf.db`

`adapters/webhook_to_perf.py` normalizes the boundary between the two services.

**LocalCMS** is a read-only system cockpit (navigation menu, TMUX sessions, module state). It is distinct from Desk Pro — LocalCMS is for ops visibility, Desk Pro is the trading dashboard.

### Key module roles

- `modules/env/env.py` — `load_env()` + `ensure_dirs()` called at the top of every entry point
- `modules/risk_engine/` — evaluates GO_LONG/GO_SHORT decisions; outputs sizing tier (FULL/HALF/MICRO/NONE), not just a gate
- `modules/execution_engine/`, `modules/position_engine/` — trade lifecycle
- `modules/decision_engine/app/strategy_logic.py` — hardcoded signal config
- `modules/perf_engine/` — intermediate position tracker (candidate → active → closed); distinct from `perf/perf_app.py` which is the FastAPI service that exposes results
- `modules/desk_pro/` — shared API/UI/service core for Desk Pro, mounted at `/desk` in perf_app; operational entry point is `modules/desk_pro_runner/` (runner → orchestrator → dashboard stack)
- `shared/logger.py` — `setup_logger(name)` for all modules
- `shared/telegram_notify.py` — Telegram alerts (metrics tracked)

### Module convention

Every module under `modules/` follows this pattern:
- `scripts/cmd.sh` — CLI entry point
- `scripts/menu.sh` — interactive menu
- `scripts/sanity_check.sh` — validates installation
- `scripts/install_shortcuts.sh` — installs wrappers in `/usr/local/bin`

New modules must expose all four scripts. When adding a module, do not skip `sanity_check.sh`.

### Collectors family (`modules/collector_*`, `modules/derivatives_collector/`)

Standalone data-collection modules, not imported by live services. Each runs via its own `cmd.sh`. Current operational collectors:
- `collector_binance_spot` — Binance public market data (oneshot, no auth)
- `derivatives_collector` — OI, Funding Rate, Liquidations, Long/Short from Coinglass and exchanges

Coinglass data is acquired via headless browser (see Vision family below), not a direct API. `coinglass=NOT_PROVEN_RUNTIME_ADAPTER` — do not assume a live Coinglass REST adapter exists.

### Vision family (`modules/bot_vision*`, `modules/vision_bot/`)

Three modules; only two are operational:
- `vision_bot` — inbox/outbox processor (ShareX → SFTP → markdown output)
- `bot_vision_step2` — operational capture point
- `bot_vision` — legacy step1 skeleton, not a runtime survivor

Headless capture runs via Node.js + Playwright in `modules/bot_vision/headless_capture/`. Install separately:
```bash
cd modules/bot_vision/headless_capture && npm install && npx playwright install chromium
```

Profiles live in `headless_capture/profiles.*.json`. Run once with `--once` flag for a single capture cycle.

### Strategy tools (`tools/strategy/`)

Standalone backtesting engines, not imported by the live services. Each family (`dca_spot/`, `dca_capital/`, `dca_cfd_short/`, `daily_scalping/`, `weekly_dca/`) has its own `engine.py` state machine, data fetchers, and runner scripts. Results go to `artifacts/results/`.

`modules/strategy/` is separate and lightweight — it only parses `95_STRATEGY_REGISTRY.md` from chantier docs to validate strategy IDs at runtime. Do not confuse it with `tools/strategy/`.

### Post-change workflow

`scripts/post_change.sh MODULE TITLE MESSAGE` logs a module change event to the student workspace and triggers DeepSeek roadmap generation via SSH. Call it after any module modification that warrants tracking. Flags: `--no-deepseek`, `--no-push`, `--model`, `--n`.

### OpenClaw suite

- `modules/openclaw_config_modulaire/` — manages `~/.openclaw/config.d/` (safe apply + rollback for `agents.json5`, `tools.json5`)
- `modules/gateway_openclaw/` — starts/stops the OpenClaw gateway via tmux (no systemd); session `openclaw-gateway` under the `openclaw` user

### Chantier docs pattern

Feature work lives in `docs/chantiers/<GO_ID>/`:
- `00_INITIAL_PROJECT_DOC.md` — concept + rules
- `20_ACCEPTANCE_REPORT.md` — results + verdict

Branch naming: `go/GO_<NAME>_01`. Main branch: `sot/mainline`.

### Tests structure

`tests/` contains flat test files plus subdirectories for domain clusters:
- `tests/e2e/` — end-to-end pipeline and session tests
- `tests/fixtures/` — shared test data
- `tests/governance/` — policy and schema validation
- `tests/openclaw/` — openclaw module tests
- `tests/runtime_health/` — cursor/fleet health checks

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
