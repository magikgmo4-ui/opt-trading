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
updated_at: 2026-04-13
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

### GO_UNIFORM_CONTINUITY_HARDENING_01
- statut : active
- repo : opt-trading
- branche : sot/mainline
- machine principale : non fixée dans ce document
- dernier point établi : `GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01` et `GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01` sont PASS, avec hardening documentaire restant à fermer proprement
- prochaine action : finir le hardening documentaire, puis ouvrir le prochain lot métier réel
- blocages : aucun blocage documentaire résiduel identifié en Git natif
