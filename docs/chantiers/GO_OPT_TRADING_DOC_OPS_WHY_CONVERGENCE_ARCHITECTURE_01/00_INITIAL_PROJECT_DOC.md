---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_CONVERGENCE_ARCHITECTURE_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_CONVERGENCE_ARCHITECTURE_01
scope: doc_ops
parent_context: SYSTEM_WHY_LAYER_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer la convergence des couches WHY avant toute implementation reelle: parser, score generator, worker, runtime graph, governance dashboard et lint experimental.

## 3_INITIAL_NEED

Le repo possede maintenant les couches WHY suivantes:
- parser WHY,
- score generator,
- worker audit,
- runtime graph,
- governance dashboard,
- lint governance experimental.

Il manque une architecture de convergence qui definit comment ces couches se relient avant d'ouvrir un worker reel ou un dashboard live.

## 4_MASTER_PROJECT_PLAN

- Definir les composants de convergence.
- Definir les flux entre parser, score, worker, graph, dashboard et lint.
- Definir les sorties communes.
- Definir les limites d'autonomie.
- Definir l'ordre des futurs chantiers reels.

## 6_FINAL_TARGET

Produire une specification doc-only de convergence WHY, sans implementation active.

## 7_CANONICAL_STATE

Le WHY est maintenant une architecture governance IA-oriented complete mais encore documentaire.

La convergence doit rester:
- doc-only,
- audit-oriented,
- non destructive,
- sans APPLY,
- sans CI active,
- sans runtime autonome.

## 12_INVARIANTS

- Aucun runtime touche.
- Aucun worker executable cree.
- Aucun dashboard live cree.
- Aucun lint executable cree.
- Aucun APPLY automatique.
- Aucune CI active.
- Aucune review humaine remplacee.

## 16_TODO

- Definir convergence map.
- Definir data flow.
- Definir shared report model.
- Definir runtime/governance boundaries.
- Definir future implementation order.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_DOC_OPS_WHY_CONVERGENCE_ARCHITECTURE_01` pour cadrer la convergence des couches WHY avant implementation reelle.
