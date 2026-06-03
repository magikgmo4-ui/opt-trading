---
doc_id: GO_CRON_TELEGRAM_TMUX_ALERTS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: notification_dispatcher
go_id: GO_CRON_TELEGRAM_TMUX_ALERTS_01
status: open
lifecycle_stage: in_progress
topic_keys:
  - opt-trading
  - telegram
  - cron
  - tmux
  - alerts
  - notification_dispatcher
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-06-03
working_branch: go/GO_CRON_TELEGRAM_TMUX_ALERTS_01
links:
  - configs/telegram/channel_map.yaml
  - shared/telegram_channels.py
  - modules/notification_dispatcher/app/dispatcher.py
---

# GO_CRON_TELEGRAM_TMUX_ALERTS_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ajouter le routing multi-canal Telegram (alerts/pipeline/push/ops) et les alertes WARN cron
avec visibilité tmux pour les strict workers.

## 6_FINAL_TARGET

- `shared/telegram_channels.py` : constantes canaux Telegram
- `configs/telegram/channel_map.yaml` : mapping canal → chat_id
- `modules/notification_dispatcher/app/dispatcher.py` : routing multi-canal
- Workers strict (5 scripts) : notification via canal approprié
- `scripts/schedule/lot1/run_readonly_smoke.sh` : smoke cron mis à jour

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| Commits | 3 |
| Fichiers modifiés | 11 |
| Additions | 312 |
| Suppressions | 53 |
| PR | #1063 |
| Statut | open — CI en cours |
