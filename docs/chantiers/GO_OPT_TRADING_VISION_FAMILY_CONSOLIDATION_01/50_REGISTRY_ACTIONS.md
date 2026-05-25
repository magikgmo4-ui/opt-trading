---
doc_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01_REGISTRY_ACTIONS
doc_type: registry_actions
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - vision
  - registry
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/40_SURVIVOR_DECISION.md
---

# 50_REGISTRY_ACTIONS

## Invariant du lot

Aucune mutation de `registry/modules_registry.yaml` n'est executee dans ce GO.

## Etat registry actuel

- `vision_bot` est present en registry
- `bot_vision_step2` est absent
- `bot_vision` est absent

## Action registry requise ensuite

### Action R1

Conserver `vision_bot` comme entree canonique de famille, mais enrichir sa description pour expliciter qu'il est l'owner de la paire transitoire `vision_bot + bot_vision_step2`.

### Action R2

Ajouter `bot_vision_step2` en registry comme module actif complementaire, non comme doublon concurrent, avec role explicite `analyse / Telegram / artefacts Desk Pro`.

### Action R3

Documenter `bot_vision` comme legacy preserve ou compat surface, avec note explicite que `headless_capture` reste un runtime utile non encore extrait.

## Action registry a ne pas faire

- ne pas supprimer `vision_bot`
- ne pas remplacer `vision_bot` par `bot_vision_step2`
- ne pas classer `bot_vision` archive simple tant que `headless_capture` y reside

## GO suivant necessaire pour mutation registry

`GO_OPT_TRADING_VISION_FAMILY_REGISTRY_REALIGNMENT_01`

Objet attendu:

- appliquer R1, R2, R3
- sans refactor runtime
- avec relecture de `docs/status/bot_vision_canonique.md` et `docs/product/guides/BOT_VISION.md`
