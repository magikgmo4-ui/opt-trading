---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_GOVERNANCE_DASHBOARD_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_GOVERNANCE_DASHBOARD_01
scope: doc_ops
parent_context: SYSTEM_WHY_LAYER_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer le futur WHY governance dashboard afin de visualiser la maturite WHY, les risques runtime, les gaps, les classes R0-R5, les surfaces externes et les gates humaines.

## 3_INITIAL_NEED

Le repo possede maintenant:
- WHY governance,
- runtime governance,
- parser WHY,
- score generator,
- worker audit,
- surfaces externes,
- runtime graph system.

Il manque un cadrage dashboard permettant de rendre ces couches visibles et reviewables.

## 4_MASTER_PROJECT_PLAN

- Definir les vues dashboard candidates.
- Definir les donnees d'entree.
- Definir les widgets/sections.
- Definir les niveaux de criticite.
- Definir les sorties review humaine.
- Definir les limites d'autonomie du dashboard.

## 6_FINAL_TARGET

Produire une specification doc-only du WHY governance dashboard, sans implementation active.

## 7_CANONICAL_STATE

Le dashboard doit rester:
- audit-oriented,
- explicable,
- non destructif,
- sans APPLY,
- sans CI active,
- sans autorite runtime autonome.

## 12_INVARIANTS

- Aucun runtime touche.
- Aucun dashboard executable cree.
- Aucun connecteur live.
- Aucun APPLY automatique.
- Aucun merge automatique.
- Aucune CI active.
- Aucune review humaine remplacee.

## 16_TODO

- Definir dashboard views.
- Definir input model.
- Definir risk panels.
- Definir review panels.
- Definir graph panels.
- Definir future lint compatibility.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_DOC_OPS_WHY_GOVERNANCE_DASHBOARD_01` pour cadrer le dashboard WHY governance.
