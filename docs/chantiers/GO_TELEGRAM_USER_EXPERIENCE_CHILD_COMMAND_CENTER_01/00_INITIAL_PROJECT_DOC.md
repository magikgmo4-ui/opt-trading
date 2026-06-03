---
doc_id: GO_TELEGRAM_USER_EXPERIENCE_CHILD_COMMAND_CENTER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: telegram_command_center
go_id: GO_TELEGRAM_USER_EXPERIENCE_CHILD_COMMAND_CENTER_01
parent_go_id: GO_TELEGRAM_ROUTING_AUDIT_CHILD_CHAT_SPLIT_ENFORCEMENT_01
status: open
lifecycle_stage: in_progress
topic_keys:
  - opt-trading
  - telegram
  - command_center
  - ux
  - user_commands
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-06-03
working_branch: go/GO_TELEGRAM_USER_EXPERIENCE_CHILD_COMMAND_CENTER_01
links:
  - modules/telegram_command_center/app/commands.py
  - modules/telegram_command_center/app/formatters.py
  - modules/bot_vision_step2/app/bot_vision_step2.py
  - shared/telegram_channels.py
  - configs/telegram/channel_map.yaml
---

# GO_TELEGRAM_USER_EXPERIENCE_CHILD_COMMAND_CENTER_01

## Concept

Ajouter une couche UX Telegram simple au-dessus du routing PR #1081.
Créer des commandes utilisateur (/help, /status, /health, /approvals, etc.)
et standardiser les formats de messages par groupe.

## Bases validées

- PR #1081 mergée: routing split-channel fonctionnel
- 4 groupes Telegram: alerts/pipeline/push/ops
- `send_to_channel(channel, message)` fonctionne
- bot_vision_step2 a déjà une boucle long-poll qui peut être étendue

## Règles

1. Commandes dispatchées via table de routage, pas de `if` séquentiels
2. Messages formatés selon le standard du groupe (court/actionnable)
3. Aucun secret dans Git
4. Tests fixtures-first
5. Ne pas casser le routing existant de PR #1081
6. bot_vision_step2 intègre le command center via import, pas de copie

## Livrables

- `modules/telegram_command_center/app/commands.py` — registre + handlers
- `modules/telegram_command_center/app/formatters.py` — templates par groupe
- Intégration dans bot_vision_step2 (import + dispatch dans la boucle existante)
- Tests unitaires ciblés
- FILE_SCOPE.txt
