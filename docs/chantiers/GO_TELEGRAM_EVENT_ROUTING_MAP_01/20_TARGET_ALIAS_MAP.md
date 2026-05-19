---
doc_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01_TARGET_ALIAS_MAP
doc_type: mapping
repo: opt-trading
go_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 20_TARGET_ALIAS_MAP - Alias bots/chats/topics

## Principe

On ne veut pas hardcoder des chat_id dans le repo. On standardise des alias, résolus via variables d’environnement.

## Aliases (cibles)

| Alias | Intention | Exemple de config |
| --- | --- | --- |
| `TG_OPS` | santé runtime / opérations | `TELEGRAM_CHAT_ID_OPS` |
| `TG_TRADING` | signaux/trades/résultats (prod) | `TELEGRAM_CHAT_ID_TRADING` |
| `TG_PAPER` | paper/dry-run journaux | `TELEGRAM_CHAT_ID_PAPER` |
| `TG_ALERTS` | alertes critiques (errors) | `TELEGRAM_CHAT_ID_ALERTS` |
| `TG_DEBUG` | debug/noise (optionnel) | `TELEGRAM_CHAT_ID_DEBUG` |

## Bots (cibles)

| Alias bot | Intention | Exemple de config |
| --- | --- | --- |
| `BOT_PRIMARY` | bot unique par défaut | `TELEGRAM_BOT_TOKEN` |
| `BOT_ALERTS` | bot dédié alertes (optionnel) | `TELEGRAM_BOT_TOKEN_ALERTS` |

## Topics (optionnel)

Si utilisation de supergroup topics:

- `TELEGRAM_TOPIC_ID_*` (par alias), ex: `TELEGRAM_TOPIC_ID_ALERTS`

Ce GO reste doc-only: pas d’implémentation topic tant que la politique n’est pas validée.
