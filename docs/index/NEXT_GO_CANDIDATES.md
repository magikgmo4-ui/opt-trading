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
updated_at: 2026-04-22
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# NEXT_GO_CANDIDATES — opt-trading

## Règle canonique

- source de vérité : repo `opt-trading`
- périmètre d’exécution courant : 12 GO non clos (`active` / `open`)
- `pass` et `reference` : hors exécution courante
- `docs/index/NEXT_GO_CANDIDATES.md` est une matrice par **chantier parent actif**
- cardinalité : **1 parent actif → 1 next GO primaire** (ou explicitement “aucun nouveau GO”)
- si plusieurs parents actifs partagent la même priorité, et qu’un seul porte un `next GO primaire` explicite, ce parent devient le point de départ opératoire par défaut
- `docs/index/REPRISE.md` est un support opératoire ; il ne remplace pas cette matrice

## Priorité opératoire active

- P0 : `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`, `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01`, `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`, `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`
- P1 : `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`, `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`, `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_JOURNAL_FULL_READING_03`, `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04`

## Matrice — parent actif → next GO primaire

| parent (actif) | status | priority | next GO primaire | next action (résumé) | refs canoniques |
| --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` | open | P0 | aucun nouveau GO | produire la matrice maître unique à partir du plan ancré et du recroisement canonique réel du repo | `docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md` |
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
