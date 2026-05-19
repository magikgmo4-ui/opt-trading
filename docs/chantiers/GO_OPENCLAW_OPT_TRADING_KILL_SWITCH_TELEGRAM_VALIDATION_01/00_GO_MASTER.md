---
go_id: GO_OPENCLAW_OPT_TRADING_KILL_SWITCH_TELEGRAM_VALIDATION_01
doc_type: go_master
repo: opt-trading
status: closed
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #510  (Live trading readiness protocol — merged)
  - PR #512  (Paper mode expansion decision — merged, Option C priorité haute)
created_at: 2026-05-17
closed_at: 2026-05-17
---

# GO_OPENCLAW_OPT_TRADING_KILL_SWITCH_TELEGRAM_VALIDATION_01

## Objectif

Valider les deux garde-fous critiques identifiés comme prérequis Phase 1
dans le protocole readiness (PR #510) :

1. **Kill switch** (`TRADING_KILL_SWITCH`) — bloque tout trade quelle que
   soit la confiance, à tous les niveaux du pipeline
2. **Telegram dispatcher dry_run** — confirme qu'en mode dry_run aucun
   appel HTTP n'est émis, et que l'absence d'env vars ne cause pas de crash

## Périmètre

- `tests/test_kill_switch_telegram_validation.py` — suite de validation dédiée
- Composants testés :
  - `modules/validation_gate/app/risk_check.py` — `check_risk()` + `KILL_SWITCH_ENV`
  - `modules/validation_gate/app/gate.py` — `ValidationGate.gate()`
  - `modules/notification_dispatcher/app/dispatcher.py` — `NotificationDispatcher.dispatch()`

## Contraintes

- Tests uniquement — aucune exécution live
- No live trade / No Bitget order
- No automatic Sheets write
- No secrets
