---
doc_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02_FINDINGS
doc_type: audit_findings
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
  - findings
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02/01_membership_matrix.md
point_de_reprise: "Synthese"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02/01_membership_matrix.md
---

# 02_findings — GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02

## Synthese

- branches auditees : `21`
- `COHERENT_COMPLETE` : `1`
- `COHERENT_EXCEPT_MATRIX` : `1`
- `INDEXED_BRANCHSTATE_UNMATERIALIZED` : `1`
- `CHANTIER_PRESENT_FRONTMATTER_INVALID` : `1`
- `CHANTIER_ONLY_UNINDEXED` : `1`
- `BRANCHSTATE_ONLY_UNMATERIALIZED` : `1`
- `SELF_DOCUMENTED_NOT_CANONIZED` : `1`
- `BRANCH_ONLY_UNREPRESENTED` : `14`

## Constats majeurs

- `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` est la seule branche pleinement representee sur les cinq surfaces controlees.
- `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` est pratiquement alignee, mais reste absente de `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.
- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` est referencee dans `GO_INDEX.md` et `BRANCH_STATE.md`, mais son dossier chantier canonique n'est pas materialise sur la ligne courante.
- `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` possede un dossier chantier, mais le `go_id` n'est pas top-level : il est imbrique sous `module:` dans `00_cadrage.md`, ce qui rompt la conformite frontmatter de ce controle.
- la majorite des branches restantes sont des branches Git sans representation canonique courante dans la matrice, les index ou `docs/chantiers/`.

## Lecture recommandee

- ne pas confondre `branch exists` avec `GO canonise`
- ne pas deduire suppression ou transport depuis ce seul audit
- traiter les corrections d'appartenance dans des lots separes, apres arbitrage humain sur la legitimite de chaque branche
