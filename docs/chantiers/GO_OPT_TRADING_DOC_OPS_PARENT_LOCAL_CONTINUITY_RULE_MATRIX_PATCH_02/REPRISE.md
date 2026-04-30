---
doc_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02_REPRISE
doc_type: chantier_reprise
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02
status: draft
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - doc_ops
  - matrix_patch
  - reprise
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02/01_PATCH_PROPOSAL.md
point_de_reprise: "Apply patch proposal to master matrix locally"
updated_at: 2026-04-30
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02/01_PATCH_PROPOSAL.md
  - docs/governance/MATRICE_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01.md
---

# REPRISE — MATRIX PATCH 02

## 7_CANONICAL_STATE

- Branche dédiée ouverte : `go/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02`.
- Addendum gouvernance candidat créé : `docs/governance/MATRICE_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01.md`.
- Proposition de patch exact créée : `01_PATCH_PROPOSAL.md`.
- La matrice maître n'a pas été réécrite directement via connecteur pour éviter un remplacement risqué du gros fichier.

## 16_TODO

1. Reprendre localement la branche.
2. Appliquer les blocs de `01_PATCH_PROPOSAL.md` dans `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.
3. Vérifier que la règle ne contredit pas les obligations de fermeture / propagation globale.
4. Commit + push.
5. Closeout PASS si la matrice contient la règle.

## 17_RESUME_POINT

```bash
git fetch --all --prune
git checkout go/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02
git rebase origin/sot/mainline
```

Puis appliquer :

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02/01_PATCH_PROPOSAL.md
```
