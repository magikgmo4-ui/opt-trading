---
doc_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module:
  go_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - branch_audit
  - go_branches
  - matrix
  - housekeeping
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "01_branch_matrix_audit.md"
updated_at: 2026-04-28
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
---

# GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01

## Objet

Auditer les branches `GO_OPT_TRADING*` encore presentes contre :

- l'etat Git reel ;
- la matrice gouvernante ;
- `docs/index/GO_INDEX.md` ;
- `docs/index/ACTIVE_STREAMS.md` ;
- `docs/index/REPRISE.md` ;
- `docs/index/BRANCH_STATE.md` ;
- les dossiers `docs/chantiers/<GO_ID>/`.

## Scope

- audit documentaire et Git uniquement ;
- aucun merge ;
- aucune suppression ;
- aucun runtime modifie ;
- aucune rebase ni stash.

## Regle de lecture appliquee

Ordre retenu pour l'audit :

1. etat Git reel prouve ;
2. `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` ;
3. `docs/index/GO_INDEX.md` ;
4. `docs/index/ACTIVE_STREAMS.md` et `docs/index/REPRISE.md` ;
5. `docs/index/BRANCH_STATE.md` pour la seule surface branches ;
6. preuves de chantier sous `docs/chantiers/`.

## Branches auditees

- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01`
- `go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01`
- `go/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01`
- `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01`
- `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`
- `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01_ISOLATED`
- `go/GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01`
- `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`
- `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`
- `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01_ALIGNMENT_01`
- `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`
- `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LIVE_ARTIFACTS_01`
- `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01`
- `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`
- `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01`
- `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`

## Methode

- `git fetch --all --prune`
- base canonique confirmee sur `sot/mainline`
- capture des branches locales et distantes `*GO_OPT_TRADING*`
- pour chaque branche : `rev-list --left-right --count`, `diff --name-status`, `diff --stat`
- recroisement exact des GO et branches dans les index et dossiers chantier

Convention retenue pour `ahead_behind_vs_sot` :

- format `behind X / ahead Y`
- `X` = commits presents seulement sur `origin/sot/mainline`
- `Y` = commits presents seulement sur la branche auditee

## Artefacts bruts produits

- `remote_go_opt_trading_branches.txt`
- `local_go_opt_trading_branches.txt`
- `raw_branch_scan.json`
- `diff_*_name_status.txt`
- `diff_*_stat.txt`

## Point d'attention

Le scan montre deja plusieurs contradictions importantes :

- des branches encore presentes alors que le GO local est clos ou `pass` ;
- des branches referencees dans `GO_INDEX.md` sans dossier canonique present sur `sot/mainline` ;
- des branches doc-only non canonisees nulle part ;
- au moins deux branches avec deltas hors doc-only.

Le rapport est donc redige sans commit automatique.
