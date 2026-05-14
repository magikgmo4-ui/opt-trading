---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_VIEW_REAL_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_VIEW_REAL_01
scope: doc_ops
parent_context: SYSTEM_WHY_LAYER_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer le premier render graph reel local du WHY/runtime graph, en lecture seule, non destructif, sans runtime live et sans connecteurs live.

## 3_INITIAL_NEED

La PR #414 a canonise la specification static view. Le prochain pas logique est de preparer le premier render local reel a partir de sources documentaires statiques autorisees.

## 4_MASTER_PROJECT_PLAN

- Definir le perimetre du local view real.
- Definir les sources autorisees.
- Definir les contraintes d'execution locale.
- Definir les artefacts produits.
- Definir les gates avant tout script executable.
- Definir la reprise vers export JSON reel.

## 6_FINAL_TARGET

Produire le cadrage initial du premier render graph local reel WHY/runtime avant implementation executable.

## 7_CANONICAL_STATE

Ce chantier est le premier pas vers un render local reel, mais reste initialement doc-first.

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

- Definir local view scope.
- Definir local view inputs.
- Definir local execution constraints.
- Definir local view outputs.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_VIEW_REAL_01` pour cadrer le premier render graph local reel WHY/runtime.
