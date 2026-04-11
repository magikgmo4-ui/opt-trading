---
doc_id: OPT_TRADING_NEXT_GO_CANDIDATES
doc_type: next_candidate
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: next
topic_keys:
  - opt-trading
  - next
  - continuity
  - migration
surface: chantier
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# NEXT_GO_CANDIDATES — opt-trading

## Candidats actuels

### GO_OPT_TRADING_LOCAL_CONTINUITY_INDEXES_01
- origine : `GO_GIT_PROGRESSIVE_MIGRATION_START_13`
- type : continuité locale
- valeur attendue : compléter la couche locale de reprise et d’orientation
- condition d’ouverture : paquet index et gouvernance locale stabilisé
- pourquoi pas maintenant : encore dans le flux actif courant
- priorité : high

### GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01
- origine : migration uniforme de continuité
- type : migration / chantier pilote
- valeur attendue : valider un premier chantier au format canonique avec dérivation vers `memory_bricks`
- condition d’ouverture : index locaux et gouvernance minimale en place
- pourquoi pas maintenant : la couche de continuité locale doit être finalisée d’abord
- priorité : high
