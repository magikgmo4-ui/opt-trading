---
doc_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02_MATRIX
doc_type: audit_matrix
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - branches
  - matrix
  - membership
  - go_index
  - branch_state
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Tableau d'appartenance"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02/02_findings.md
---

# 01_membership_matrix — GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02

## Tableau d'appartenance

| branch | in_GO_INDEX | in_BRANCH_STATE | in_MATRICE | chantier_dir_present | frontmatter_go_id | statut_coherence | correction_proposee_non_appliquee |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | yes | yes | no | no | `NO_CHANTIER_DIR` | `INDEXED_BRANCHSTATE_UNMATERIALIZED` | Materialiser `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/` sur la ligne canonique courante et ajouter un `go_id` top-level ; ajouter une mention explicite dans la matrice si le parent reste actif |
| `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Ouvrir un dossier chantier canonique et ses references d'index si la branche reste legitime, sinon laisser pour arbitrage ulterieur hors de ce lot |
| `go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Ouvrir un dossier chantier canonique et ses references d'index si la branche reste legitime, sinon laisser pour arbitrage ulterieur hors de ce lot |
| `go/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Ouvrir un dossier chantier canonique et ses references d'index si la branche reste legitime, sinon laisser pour arbitrage ulterieur hors de ce lot |
| `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Ouvrir un dossier chantier canonique et ses references d'index si la branche reste legitime, sinon laisser pour arbitrage ulterieur hors de ce lot |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` | no | no | no | yes | `NESTED_ONLY` | `CHANTIER_PRESENT_FRONTMATTER_INVALID` | Remonter `go_id` au top-level du frontmatter puis decider, dans un lot separe, si le GO doit etre reflechi dans `GO_INDEX.md` et `BRANCH_STATE.md` |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01_ISOLATED` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Documenter soit un dossier chantier propre, soit une reclassification explicite en branche temporaire de support dans un lot ulterieur |
| `go/GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01` | no | no | no | yes | `MATCH` | `CHANTIER_ONLY_UNINDEXED` | Si la branche reste utile, ajouter sa qualification dans `BRANCH_STATE.md` et statuer sur sa presence ou non dans `GO_INDEX.md` ; sinon laisser pour arbitrage de cloture separe |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Ouvrir un dossier chantier canonique et ses references d'index si la branche reste legitime, sinon laisser pour arbitrage ulterieur hors de ce lot |
| `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` | yes | yes | yes | yes | `MATCH` | `COHERENT_COMPLETE` | Aucune correction d'appartenance proposee dans ce lot |
| `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01_ALIGNMENT_01` | no | yes | no | no | `NO_CHANTIER_DIR` | `BRANCHSTATE_ONLY_UNMATERIALIZED` | Soit materialiser un chantier et une justification canonique si la branche doit survivre, soit la garder hors index comme support temporaire clairement annote dans un lot separe |
| `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | yes | yes | no | yes | `MATCH` | `COHERENT_EXCEPT_MATRIX` | Ajouter une mention explicite du parent dans la matrice maitre ou une annexe canonique referencee par elle, sans toucher a la branche dans ce lot |
| `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LIVE_ARTIFACTS_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Ouvrir un dossier chantier canonique et ses references d'index si la branche reste legitime, sinon laisser pour arbitrage ulterieur hors de ce lot |
| `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Ouvrir un dossier chantier canonique et ses references d'index si la branche reste legitime, sinon laisser pour arbitrage ulterieur hors de ce lot |
| `go/GO_OPT_TRADING_REMAINING_BRANCHES_TRANSPORT_DELETE_03` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Si la branche doit etre gardee comme reference de lot clos/non merge, materialiser son closeout canonique sur la ligne courante ; sinon laisser pour housekeeping ulterieur |
| `go/GO_OPT_TRADING_REMAINING_BRANCHES_TRANSPORT_DELETE_03_CANCEL_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Si la branche doit etre gardee comme reference d'annulation, materialiser son closeout canonique sur la ligne courante ; sinon laisser pour housekeeping ulterieur |
| `go/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Si l'audit doit rester comme reference canonique, integrer son dossier documentaire sur la ligne courante ; sinon laisser la branche comme reference Git non canonisee |
| `go/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02` | no | no | no | yes | `MATCH` | `SELF_DOCUMENTED_NOT_CANONIZED` | Garder ce lot hors `GO_INDEX.md` et `BRANCH_STATE.md` si c'est un audit temporaire, ou definir explicitement sa place canonique si la branche doit durer |
| `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Ouvrir un dossier chantier canonique et ses references d'index si la branche reste legitime, sinon laisser pour arbitrage ulterieur hors de ce lot |
| `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Ouvrir un dossier chantier canonique et ses references d'index si la branche reste legitime, sinon laisser pour arbitrage ulterieur hors de ce lot |
| `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | no | no | no | no | `NO_CHANTIER_DIR` | `BRANCH_ONLY_UNREPRESENTED` | Ouvrir un dossier chantier canonique et ses references d'index si la branche reste legitime, sinon laisser pour arbitrage ulterieur hors de ce lot |

## Notes de lecture

- `frontmatter_go_id = MATCH` signifie qu'un `go_id:` top-level coherent a ete trouve dans `docs/chantiers/<GO_ID>/`
- `frontmatter_go_id = NESTED_ONLY` signifie qu'un `go_id` n'apparait qu'imbrique sous `module:` et est donc traite comme non conforme pour ce controle
- l'absence dans la matrice n'implique pas suppression ; elle signale seulement une non-representation documentaire sur cette surface
