---
doc_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01_CURRENT_INBOUND_SURFACES
doc_type: inventory
repo: opt-trading
go_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 10_CURRENT_INBOUND_SURFACES - État actuel (repo)

## Ce qui existe

| Surface | Preuve | Rôle |
| --- | --- | --- |
| Bot Vision Step2 (bot API) | `modules/bot_vision_step2/app/bot_vision_step2.py` | bot Telegram (callbacks + /analyze), plutôt vision/outbound |
| Notification dispatcher (outbound) | `modules/notification_dispatcher/` | envoi Telegram par event_type (pipeline) |
| Helper outbound générique | `shared/telegram_notify.py` | sendMessage HTML |
| E2E Telegram smoke (simulé) | `e2e_telegram_smoke.py` | tests adapter “botpress/openclaw” (pas screener channels) |

## Ce qui manque (gap direct du bundle)

| Manquant | Pourquoi | Notes |
| --- | --- | --- |
| Registry de channels inbound | base de confiance + gouvernance | ne pas hardcoder chat_id |
| Ingestion Telegram inbound “screener” | capter messages de channels | doit être séparé de l’outbound |
| Parsers (trade/setup/news) | convertir texte → events | doc-only ici |

## Conclusion

Le repo a déjà l’outbound et des bots utilitaires, mais pas de “screener inbound” structuré. Le registry est le pré-requis pour implémenter un ingest sûr et filtré.
