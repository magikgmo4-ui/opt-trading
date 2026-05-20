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
updated_at: 2026-05-20
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
- périmètre d’exécution courant : 8 GO non clos retenus (`active` / `open`)
- `pass` et `reference` : hors exécution courante
- `docs/index/NEXT_GO_CANDIDATES.md` est une matrice par **chantier parent actif**
- cardinalité : **1 parent actif → 1 next GO primaire** (ou explicitement “aucun nouveau GO”)
- si plusieurs parents actifs partagent la même priorité, et qu’un seul porte un `next GO primaire` explicite, ce parent devient le point de départ opératoire par défaut
- `docs/index/REPRISE.md` est un support opératoire ; il ne remplace pas cette matrice
- toute divergence locale avec `GO_INDEX.md` releve d'un manque de synchronisation documentaire et ne change pas la verite de liste

## Priorité opératoire active

- P0 : `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`
- P1 : `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, `GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01`, `GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01`

## Matrice — parent actif → next GO primaire

| parent (actif) | status | priority | next GO primaire | next action (résumé) | refs canoniques |
| --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | open | P1 | `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` | canoniser ou confirmer la mÃ©thode parent-local + inbox + batch aprÃ¨s pilote ; aucun runtime OpenClaw | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md`; `docs/governance/PARENT_CONTINUITY_INDEX_INBOX_METHOD_01.md` |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | active | P0 | `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` | executer l'implementation de base tmux-ide apres verification de la machine cible canonique ; OpenClaw hors scope | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/90_CLOSEOUT.md` |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | active | P1 | aucun nouveau GO | consolider la lecture canonique des lignées mixtes sans duplication de preuves | `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md` |
| `GO_GIT_PROGRESSIVE_MIGRATION_START_13` | active | P1 | aucun nouveau GO | expliciter la suite opératoire avant tout lot d’exécution | `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | open | P1 | aucun nouveau GO | exécuter l’audit détaillé de la famille réseau/ssh dans ce GO | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | open | P2 | aucun nouveau GO | utiliser l’entrée `OPEN` comme base si un futur GO enfant d’audit documentaire doit être rouvert | `docs/index/GO_INDEX.md`; `docs/chantiers/GO_GIT_AI_TEAM_ARCHITECTURE_PARENT_DOC_ONLY_INTEGRATION_01/03_decisions.md` |
| `GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01` | open | P2 | aucun nouveau GO | conserver la matrice bucketisee comme point d'entree canonique ; ne pas relancer de classification large hors contradiction prouvee | `docs/chantiers/GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01/00_classification_matrix.md` |
| `GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01` | open | P2 | `GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01` | si validation humaine du bucket 1, ouvrir un GO repo-only borne aux workflows/deploy, sinon ouvrir un GO `machine_runtime_map` separe | `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01/20_CLASSIFICATION_REVIEW.md`; `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01/90_REPRISE_POINT.md` |
