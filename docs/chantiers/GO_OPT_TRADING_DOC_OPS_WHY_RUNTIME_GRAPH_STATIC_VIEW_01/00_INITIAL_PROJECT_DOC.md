---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_STATIC_VIEW_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_STATIC_VIEW_01
scope: doc_ops
parent_context: SYSTEM_WHY_LAYER_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer le premier rendu graph local du WHY/runtime graph sous forme de vue statique, lecture seule, non destructive et audit-oriented.

## 3_INITIAL_NEED

Le repo possede maintenant une architecture complete de prototype graph statique WHY/runtime. Le prochain pas est de cadrer le premier rendu local effectif a partir de sources documentaires autorisees.

## 4_MASTER_PROJECT_PLAN

- Definir le perimetre de la vue statique locale.
- Definir les inputs strictement autorises.
- Definir les formats de sortie.
- Definir les controles lecture seule.
- Definir les gates avant tout code executable.
- Definir le point de reprise vers export JSON reel.

## 6_FINAL_TARGET

Produire un cadrage initial du premier rendu graph local WHY/runtime, sans runtime live et sans connecteurs live.

## 7_CANONICAL_STATE

Le chantier represente le premier pas operationnel vers une visualisation locale, mais reste initialement doc-first.

Aucun runtime live, connecteur live, traversal decisionnel, dashboard live ou CI active n'est autorise.

## 12_INVARIANTS

- Lecture seule.
- Non destructif.
- Aucun runtime live.
- Aucun connecteur live.
- Aucun APPLY runtime.
- Aucun traversal decisionnel.
- Aucun dashboard live.
- Aucune CI active.
- Review humaine conservee.

## 16_TODO

- Definir static view scope.
- Definir static view inputs.
- Definir static view renderer constraints.
- Definir static view outputs.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_STATIC_VIEW_01` pour cadrer le premier rendu graph local WHY/runtime.
