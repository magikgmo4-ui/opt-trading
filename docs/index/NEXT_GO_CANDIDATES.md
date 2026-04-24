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
search_tags:
  - surface:chantier
  - doc_role:index
  - flow:next_surface
  - closeout:reference
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Matrice - parent actif -> next GO primaire"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# NEXT_GO_CANDIDATES — opt-trading

## Règle canonique

- gouvernance d'ensemble : `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- source de vérité : repo `opt-trading`
- pour la liste canonique des GO et toute cardinalite systeme, `docs/index/GO_INDEX.md` reste prioritaire
- périmètre d’exécution courant : 14 GO non clos retenus (`active` / `open`)
- `pass` et `reference` : hors exécution courante
- `docs/index/NEXT_GO_CANDIDATES.md` est une matrice par **chantier parent actif**
- cardinalité : **1 parent actif → 1 next GO primaire** (ou explicitement “aucun nouveau GO”)
- si plusieurs parents actifs partagent la même priorité, et qu’un seul porte un `next GO primaire` explicite, ce parent devient le point de départ opératoire par défaut
- `docs/index/REPRISE.md` est un support opératoire ; il ne remplace pas cette matrice
- toute divergence locale avec `GO_INDEX.md` releve d'un manque de synchronisation documentaire et ne change pas la verite de liste

## Priorité opératoire active

- P0 : `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01`, `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`, `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`
- P1 : `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`, `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`, `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_JOURNAL_FULL_READING_03`, `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04`, `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, `GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01`, `GO_OPT_TRADING_PARENT_NAMING_CANON_01`

## Matrice — parent actif → next GO primaire

| parent (actif) | status | priority | next GO primaire | next action (résumé) | refs canoniques |
| --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` | active | P0 | aucun nouveau GO | exécuter LOT 1 (index) puis LOT 2 (hiérarchie journal) | `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md` |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | active | P0 | `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` | exécuter l’implémentation de base tmux-ide sur machine cible | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` |
| `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01` | active | P0 | aucun nouveau GO | produire la matrice canonique (PHASE C) puis le plan de lots physiques futurs (PHASE D) | `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md` |
| `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01` | active | P1 | aucun nouveau GO | consolider la carte des surfaces et ses points d’ancrage documentaires | `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md` |
| `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01` | active | P1 | aucun nouveau GO | consolider la politique racine et les arbitrages de reclassement documentaire | `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md` |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | active | P1 | aucun nouveau GO | consolider la lecture canonique des lignées mixtes sans duplication de preuves | `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md` |
| `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01` | active | P1 | aucun nouveau GO | consolider le scope registry et ses exceptions dans la source canonique | `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/00_cadrage.md` |
| `GO_GIT_PROGRESSIVE_MIGRATION_START_13` | active | P1 | aucun nouveau GO | expliciter la suite opératoire avant tout lot d’exécution | `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | open | P1 | aucun nouveau GO | exécuter l’audit détaillé de la famille réseau/ssh dans ce GO | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| `GO_OPT_TRADING_JOURNAL_FULL_READING_03` | active | P2 | aucun nouveau GO | reprise à `BLOCK_16` seulement si réouverture explicite | `docs/chantiers/GO_OPT_TRADING_JOURNAL_FULL_READING_03/03_decision_freeze_after_block_15.md` |
| `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04` | active | P2 | aucun nouveau GO | poursuivre LOT_S24→LOT_S28 puis croiser avec `journal.md` | `docs/chantiers/GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04/00_cadrage.md` |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | open | P2 | aucun nouveau GO | utiliser l’entrée `OPEN` comme base si un futur GO enfant d’audit documentaire doit être rouvert | `docs/index/GO_INDEX.md`; `docs/chantiers/GO_GIT_AI_TEAM_ARCHITECTURE_PARENT_DOC_ONLY_INTEGRATION_01/03_decisions.md` |
| `GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01` | open | P2 | aucun nouveau GO | poursuivre le pilote documentaire borné avant toute extension plus large | `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/03_decisions.md` |
| `GO_OPT_TRADING_PARENT_NAMING_CANON_01` | open | P2 | `GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01` | reprendre l’inventaire repo-first des écarts de nommage avant tout lot d’application | `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md`; `docs/governance/NAMING_CANON_POLICY_01.md` |
