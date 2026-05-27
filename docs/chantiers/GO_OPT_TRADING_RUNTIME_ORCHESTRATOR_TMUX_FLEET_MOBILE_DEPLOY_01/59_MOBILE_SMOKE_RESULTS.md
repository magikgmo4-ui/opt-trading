---
doc_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_MOBILE_SMOKE_01_RESULTS
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_MOBILE_SMOKE_01
parent_go_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01
status: open
source_kind: canonical
updated_at: 2026-05-26
---

# 59 — Mobile smoke results (read-only)

## Objective

Prouver un smoke minimal operateur distant en read-only :

- phone / SSH / tmux / OpenClaw / repo
- sans watchdog 11–12
- sans ecriture sous `/opt/trading/tmp/`
- sans modification `secrets/`
- sans `git clean` / `git restore` distants

## Precheck local

```text
branch = sot/mainline...origin/sot/mainline
worktree = clean
```

## Execution (SSH read-only)

| Etape | Host | Commande | Sortie utile | Verdict | Notes |
|---:|---|---|---|---|---|
| 1 | `db-layer` | `hostname; whoami; pwd` | `db-layer / ghost / /home/ghost` | PASS | |
| 2 | `admin-trading` | `hostname; whoami; pwd` | `admin-trading / ghost / /home/ghost` | PASS | |
| 3 | `db-layer` | `cd /opt/trading && git status --short --branch` | `sot/mainline...origin/sot/mainline` + untracked `.claude/`, `artifacts/backtests/`, `secrets/` | PASS_WITH_WARNINGS | hygiene runtime-local |
| 4 | `db-layer` | `tmux ls` | `openclaw-core` | PASS | |
| 5 | `db-layer` | `tmux has-session -t openclaw-core` | `rc=0` | PASS | |
| 6 | `db-layer` | `sudo -n -u openclaw openclaw gateway health` | `Gateway Health OK` ; `Telegram: ok` | PASS_WITH_WARNINGS | warning allowlist Telegram vide |
| 7 | `db-layer` | `sudo -n -u openclaw openclaw gateway probe` | `Reachable: yes` ; `RPC: ok` ; `loopback ws://127.0.0.1:18789` | PASS_WITH_WARNINGS | warning allowlist Telegram vide |
| 8 | `admin-trading` | `tmux ls` | sessions: `apps-connectors`, `desk-pro`, `market-data`, `screeners`, `trading-pipeline` | PASS | |
| 9 | `admin-trading` | `tmux has-session -t desk-pro` | `rc=0` | PASS | |
| 10 | `admin-trading` | `tmux has-session -t screeners` | `rc=0` | PASS | |

## Verdict

```text
MOBILE_SMOKE = PASS_WITH_WARNINGS
RUNTIME_OPERATOR_CHAIN = PROVEN_READ_ONLY
```

## Warnings (non bloquants)

- `db-layer` untracked runtime-local : `.claude/`, `artifacts/backtests/`, `secrets/`
- `openclaw` : warning `channels.telegram.groupPolicy=allowlist` avec allowlist vide (drop silencieux des messages de groupe)

## Remaining gaps (hors scope du smoke)

- fleet_orchestrator `WARN` (machines stale/unreachable)
- mobile smoke avec actions ecriture (hors scope read-only) : NOT_RUN
- closeout parent : toujours bloque par surfaces e2e restantes (TradingView/webhook, Bot Vision, inbound parser, etc.)
