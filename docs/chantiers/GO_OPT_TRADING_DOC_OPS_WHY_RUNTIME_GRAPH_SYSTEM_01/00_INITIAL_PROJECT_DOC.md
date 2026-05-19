---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_SYSTEM_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_SYSTEM_01
scope: doc_ops
parent_context: SYSTEM_WHY_LAYER_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer le futur WHY runtime graph system afin de relier surfaces runtime, machines, dependances, classes R0-R5, surfaces externes et gouvernance WHY.

## 3_INITIAL_NEED

Le repo possede maintenant:
- WHY governance,
- runtime risk map,
- parser WHY,
- score generator,
- worker audit,
- surfaces externes candidates.

Il manque une architecture de graphe runtime WHY pour representer les relations entre ces couches.

## 4_MASTER_PROJECT_PLAN

- Definir les noeuds du graphe.
- Definir les relations du graphe.
- Definir les classes runtime R0-R5 dans le graphe.
- Definir les machines et surfaces externes.
- Definir les invariants et gates associes.
- Definir les limites d'autonomie et reporting futur.

## 6_FINAL_TARGET

Produire une specification doc-only du runtime graph system WHY, sans implementation active.

## 7_CANONICAL_STATE

Le WHY est devenu une architecture de governance documentaire IA-oriented.

Le runtime graph doit rester:
- audit-oriented,
- explicable,
- non destructif,
- sans APPLY,
- sans autorite runtime autonome.

## 12_INVARIANTS

- Aucun runtime touche.
- Aucun graphe executable cree.
- Aucun connecteur live.
- Aucun APPLY automatique.
- Aucun merge automatique.
- Aucune CI active.

## 16_TODO

- Definir graph nodes.
- Definir graph edges.
- Definir runtime classes mapping.
- Definir multi-machine relations.
- Definir external surfaces relations.
- Definir future dashboard compatibility.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_SYSTEM_01` pour cadrer le runtime graph system WHY.
