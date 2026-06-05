---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_WORKER_AUDIT_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_WORKER_AUDIT_01
scope: doc_ops
parent_context: SYSTEM_WHY_LAYER_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer le futur worker d'audit WHY qui combine parser WHY, score generator, runtime governance, gaps et sorties audit.

## 3_INITIAL_NEED

Le repo possede maintenant:
- WHY layer,
- runtime risk map,
- parser WHY markdown,
- score generator WHY.

Il manque un cadrage coherent du worker d'audit WHY.

## 4_MASTER_PROJECT_PLAN

- Definir le role du worker.
- Definir ses entrees.
- Definir son pipeline.
- Definir ses sorties audit.
- Definir ses limites d'autonomie.
- Definir sa relation avec reviews humaines et runtime governance.

## 6_FINAL_TARGET

Produire une specification doc-only du worker WHY audit-oriented, sans implementation active.

## 7_CANONICAL_STATE

Le futur worker doit rester:
- non destructif,
- audit-oriented,
- sans APPLY,
- sans merge automatique,
- sans autorite runtime autonome.

## 12_INVARIANTS

- Aucun runtime touche.
- Aucun worker executable cree.
- Aucune CI active.
- Aucun APPLY automatique.
- Aucun merge automatique.
- Aucune review humaine remplacee.

## 16_TODO

- Definir worker scope.
- Definir inputs.
- Definir pipeline.
- Definir outputs.
- Definir safety limits.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_DOC_OPS_WHY_WORKER_AUDIT_01` pour cadrer le worker d'audit WHY.

## RISKS

- À qualifier.
