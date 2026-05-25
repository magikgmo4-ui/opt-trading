---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_TELEGRAM_CLAIM_READONLY_01_EXISTING_SURFACE_READ
doc_type: surface_read
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_TELEGRAM_CLAIM_READONLY_01
created_at: 2026-05-25
---

# 10_EXISTING_SURFACE_READ

## Inventaire Telegram côté repo (pré-GO)

### Telegram envoi / notifications

- `shared/telegram_notify.py` — envoi d'alertes sortantes ; hors scope
- `modules/notification_dispatcher/app/dispatcher.py` — dispatcher notifications ; hors scope
- `modules/vision/coinglass/telegram_sender.py` — sender Coinglass ; hors scope

### Telegram screener

- Aucun `telegram_screener` module dans le repo.
- Aucun channel registry.
- Aucun parser de messages inbound.

### `telegram_claim.v1` — absent (gap ouvert)

Aucun fichier `telegram_claim_reader.py` dans le repo.
Aucune référence à `telegram_claim` dans le codebase.
Le contrat `telegram_claim.v1` est déclaré dans `20_TARGET_INPUT_CLASSES.md` du parent
comme cible future (`claim_type: trade_claim / setup / news`).

### Fixtures Telegram existantes

- Aucune fixture `telegram_claim_*` avant ce GO.

## Conclusion

Le reader `telegram_claim` est à créer de zéro.
Le contrat minimal est à définir par fixture-first :
`input_class`, `claim_id`, `source`, `channel_id`, `message_id`,
`symbol`, `timeframe`, `claim_ts`, `claim_type`, `text`, `entities`, `refs`.

Upstream possible `PF_TELEGRAM_SCREENER` (non implémenté) sera le producteur live
lorsqu'il existera. Ce GO prouve uniquement la consommation Desk Pro read-only.
