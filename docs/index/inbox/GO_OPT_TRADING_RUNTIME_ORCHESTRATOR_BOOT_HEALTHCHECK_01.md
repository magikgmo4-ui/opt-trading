---
doc_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_01_INBOX
doc_type: inbox
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: active
lifecycle_stage: impl
surface: index
source_kind: canonical
created_at: 2026-05-18
updated_at: 2026-05-18
links:
  - modules/runtime_health/healthcheck.py
  - modules/runtime_health/config/runtime_health.yml
  - deploy/systemd/opt-trading-runtime-health.service
  - deploy/systemd/opt-trading-runtime-health.timer
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_01

## Objet

Runtime Health Supervisor Phase 1 — diagnostic-only. Checks systemd services/timers, venv, env,
ports, HTTP, paths, artifacts, logs, orchestrator (tmux). Notification Telegram sur changement
d'état. Aucun restart automatique. Aucun secret dans les logs.

## Livrables crees

- `modules/runtime_health/healthcheck.py` — script principal stdlib-only
- `modules/runtime_health/config/runtime_health.yml` — config declarative
- `modules/runtime_health/schemas/runtime_health.schema.json` — JSON Schema draft-07
- `scripts/runtime_healthcheck.sh` — wrapper shell (+x)
- `deploy/systemd/opt-trading-runtime-health.service` — Type=oneshot, User=ghost
- `deploy/systemd/opt-trading-runtime-health.timer` — OnBootSec=90s, toutes les 5min

## Prochaine etape

Deployer sur db-layer : copier les unites systemd, `systemctl enable --now opt-trading-runtime-health.timer`.
Phase 2 (self-heal) a planifier apres validation Phase 1 en production.
