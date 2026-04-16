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
surface: chantier
source_kind: canonical
updated_at: 2026-04-16
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# NEXT_GO_CANDIDATES — opt-trading 

## Règle canonique

- source de vérité : repo `opt-trading`
- périmètre d’exécution courant : 6 GO non clos (`active` / `open` / `fail`)
- `pass` et `reference` : hors exécution courante

## Priorité opératoire active

- P0 : `GO_GITHUB_PARK_AUDIT_EXPANSION_01`, `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`
- P1 : `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_JOURNAL_FULL_READING_03`, `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04`


## Candidats actuels

- aucun nouveau GO à ouvrir tant que le lot prioritaire des 6 GO non clos n’est pas réaligné/exécuté selon `REPRISE.md`
- prochaine action immédiate : exécuter `GO_GITHUB_PARK_AUDIT_EXPANSION_01` (Next GO : `GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01`)
