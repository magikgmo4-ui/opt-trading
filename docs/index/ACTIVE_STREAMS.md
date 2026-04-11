---
doc_id: OPT_TRADING_ACTIVE_STREAMS
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - active_streams
  - continuity
  - reprise
surface: chantier
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/index/GO_INDEX.md
---

# ACTIVE_STREAMS — opt-trading

## Objet

Ce document référence les flux réellement actifs ou bloqués dans `opt-trading`.

Il sert à :
- distinguer l’actif du simple historique
- rendre la reprise immédiate plus lisible
- éviter la confusion entre chantier en cours et candidat futur

---

## Règles

- ne référencer ici que ce qui est réellement actif ou bloqué
- ne pas y mettre les simples opportunités ni les archives mortes
- pour chaque flux, garder un dernier point établi et une prochaine action claire

---

## Flux actifs

### GO_GIT_PROGRESSIVE_MIGRATION_START_13
- statut : active
- repo : opt-trading
- branche : sot/mainline
- machine principale : non fixée dans ce document
- dernier point établi : paquet gouvernance locale créé (`REPO_ROLE.md`, `DOC_LAYERS.md`, `MEMORY_BRICKS_MAPPING.md`)
- prochaine action : créer les index locaux (`GO_INDEX.md`, `ACTIVE_STREAMS.md`, `REPRISE.md`) puis `NEXT_GO_CANDIDATES.md` et `OPPORTUNITY_LOG.md`
- blocages : aucun blocage établi à ce stade
