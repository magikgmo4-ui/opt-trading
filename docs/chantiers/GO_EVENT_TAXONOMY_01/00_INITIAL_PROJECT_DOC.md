---
doc_id: GO_EVENT_TAXONOMY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_EVENT_TAXONOMY_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_EVENT_TAXONOMY_01/10_CURRENT_EVENT_SURFACES.md
  - docs/chantiers/GO_EVENT_TAXONOMY_01/20_CANONICAL_EVENT_ENVELOPE.md
  - docs/chantiers/GO_EVENT_TAXONOMY_01/30_EVENT_FAMILY_MAPPING.md
  - docs/chantiers/GO_EVENT_TAXONOMY_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - Event taxonomy transverse

## But

Fournir un langage commun (enveloppe + types + familles) pour:

- ingestion (webhook / observer / bot vision / headless)
- pipeline workers (router/proposition/gate/execute/track/write/feed)
- Desk Pro hub (synthèse + UI)
- routing Telegram (outbound) et futures surfaces inbound
- Sheets / Perf / Registry

## Contraintes

- documenter à partir du repo réel (pas de refactor runtime, pas de breaking change)
- conserver la compatibilité avec les objets existants (dataclasses `schema.py` et payloads dict)
- privilégier un envelope "read-only" d’abord (fixtures / dry-run), puis brancher routing

## Livrables dans ce GO

- `10_CURRENT_EVENT_SURFACES.md` : état réel des surfaces et formats existants
- `20_CANONICAL_EVENT_ENVELOPE.md` : envelope canonique minimal (V1)
- `30_EVENT_FAMILY_MAPPING.md` : mapping event_type ↔ familles ↔ owners ↔ routing impact
- `90_REPRISE_POINT.md` : reprise + next GO
