---
doc_id: GO_OPT_TRADING_SECURITY_CREDENTIALS_TELEGRAM_MULTICHANNEL_CHILD_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: security_credentials
go_id: GO_OPT_TRADING_SECURITY_CREDENTIALS_TELEGRAM_MULTICHANNEL_CHILD_01
parent_go_id: GO_OPT_TRADING_SECURITY_CREDENTIALS_CANONICAL_METHOD_PARENT_01
status: open
lifecycle_stage: in_progress
topic_keys:
  - opt-trading
  - security_credentials
  - telegram
  - multi_channel
  - credentials_registry
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-06-03
working_branch: go/GO_OPT_TRADING_SECURITY_CREDENTIALS_TELEGRAM_MULTICHANNEL_CHILD_01
links:
  - configs/env/registry/credentials.yaml
  - configs/env/registry/roles.yaml
  - configs/env/roles/telegram_collector.env.example
  - configs/telegram/channel_map.yaml
  - shared/telegram_channels.py
---

# GO_OPT_TRADING_SECURITY_CREDENTIALS_TELEGRAM_MULTICHANNEL_CHILD_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Aligner le registre de credentials Telegram avec les 4 nouveaux canaux
multi-channel introduits par PR #1063 (`shared/telegram_channels.py`,
`configs/telegram/channel_map.yaml`).

Passer par `CREDENTIAL_CHANGE_REQUEST / ADD` conformément à la méthode canonique
`GO_OPT_TRADING_SECURITY_CREDENTIALS_CANONICAL_METHOD_PARENT_01`.

## 6_FINAL_TARGET

| Credential ID | Env Var | Statut |
|---|---|---|
| `telegram_chat_id_alerts` | `TELEGRAM_CHAT_ID_ALERTS` | ADD |
| `telegram_chat_id_pipeline` | `TELEGRAM_CHAT_ID_PIPELINE` | ADD |
| `telegram_chat_id_push` | `TELEGRAM_CHAT_ID_PUSH` | ADD |
| `telegram_chat_id_ops` | `TELEGRAM_CHAT_ID_OPS` | ADD |

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| Branche de départ | sot/mainline @ 4f880fbd |
| PR routing multi-canal | #1063 — mergée 2026-06-03 |
| PR setup credentials base | #1055 — mergée 2026-06-02 |
| Gap identifié | credentials.yaml, roles.yaml, env.example ne déclarent pas les 4 nouveaux chat_id |

## Contraintes

- Zéro valeur réelle de chat_id, token ou secret dans Git.
- Zéro modification de `/etc/opt-trading/` depuis le repo.
- Placeholders vides uniquement dans les `.env.example`.
- Toute valeur réelle reste dans `/etc/opt-trading/env.d/roles/telegram_collector.env` sur chaque machine autorisée.
