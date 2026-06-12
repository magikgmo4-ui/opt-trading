---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_SCORE_GENERATOR_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_SCORE_GENERATOR_01
scope: doc_ops
parent_context: SYSTEM_WHY_LAYER_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer le futur WHY score generator afin de transformer les regles WHY preparatoires en modele calculable et explicable.

## 3_INITIAL_NEED

Le repo possede maintenant:
- un WHY layer,
- une governance runtime,
- un parser WHY markdown,
- des regles de gaps,
- une preparation de scoring.

Il manque un modele de score WHY coherent et exploitable.

## 4_MASTER_PROJECT_PLAN

- Definir les composantes du score.
- Definir les ponderations.
- Definir les penalites critiques.
- Definir les relations avec R0-R5.
- Definir les limites du score.
- Preparer les futures sorties audit.

## 6_FINAL_TARGET

Produire une specification complete du WHY score generator sans implementation runtime.

## 7_CANONICAL_STATE

Le parser WHY reste:
- doc-only,
- audit-oriented,
- non destructif.

Le score generator doit conserver ces invariants.

## 12_INVARIANTS

- Aucun APPLY automatique.
- Aucun FAIL runtime autonome.
- Aucun merge automatique.
- Aucun scoring bloqueur.
- Aucun remplacement de review humaine.

## 16_TODO

- Definir score model.
- Definir score penalties.
- Definir runtime weighting.
- Definir audit outputs.
- Definir governance limits.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_DOC_OPS_WHY_SCORE_GENERATOR_01` pour cadrer le futur WHY score generator.

## RISKS

- À qualifier.
