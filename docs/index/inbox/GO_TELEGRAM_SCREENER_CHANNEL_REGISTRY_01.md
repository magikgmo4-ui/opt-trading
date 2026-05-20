---
doc_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - telegram
  - screener
  - inbound
  - registry
  - trust_tiers
  - signal_chain
links:
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/10_CURRENT_INBOUND_SURFACES.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/20_REGISTRY_SCHEMA_TARGET.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/90_REPRISE_POINT.md
---

# INBOX - GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01

## Objet

Définir un registry de channels Telegram inbound (screener) avec trust tiers + catégories, sans mélanger inbound et outbound.

## Résultat

État établi :

- surfaces Telegram relues et reconfirmees pour `modules/bot_vision_step2/app/bot_vision_step2.py`, `modules/notification_dispatcher/`, `shared/telegram_notify.py` et `e2e_telegram_smoke.py`
- presence d'un `getUpdates` constatee dans `bot_vision_step2`, mais cette surface reste un bot utilitaire/vision et ne prouve pas un screener inbound structure par channels
- validation relancee dans cette passe : `python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py -q` -> `23 passed`
- aucune mutation runtime introduite ; le chantier reste doc-only

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total sans melanger inbound et outbound
- `Tableau Kanban du bundle` : reste la reference principale
- `Prochain item Kanban exact` : `GO_DESKPRO_INPUT_EXPANSION_01`
- `Gaps encore ouverts` : registry YAML, trust tiers actifs, parse contracts, listener inbound gouverne

## Point de reprise

```text
docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/20_REGISTRY_SCHEMA_TARGET.md
docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/40_GAPS_AND_NEXT_GO.md
```
