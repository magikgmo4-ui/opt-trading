---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_EXTERNAL_ORCHESTRATION_SURFACES_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_EXTERNAL_ORCHESTRATION_SURFACES_01
scope: doc_ops
parent_context: SYSTEM_WHY_LAYER_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer les surfaces d'orchestration externes candidates dans la governance WHY.

## 3_INITIAL_NEED

Le systeme WHY couvre maintenant:
- parser,
- score generator,
- worker audit,
- runtime governance.

Il manque la cartographie des surfaces externes potentielles:
- ClickUp,
- Botpress,
- Knowledge Graph,
- Airtable.

## 4_MASTER_PROJECT_PLAN

- Identifier les roles possibles.
- Definir les niveaux de criticite.
- Definir les risques d'autonomie.
- Definir les relations runtime/governance.
- Definir les limites d'integration.

## 6_FINAL_TARGET

Produire un cadrage doc-only des surfaces d'orchestration externes candidates sans integration runtime active.

## 7_CANONICAL_STATE

Les surfaces externes ne sont pas encore integrees au runtime WHY.

Elles doivent etre traitees comme:
- surfaces candidates,
- dependances potentielles,
- couches governance possibles.

## 12_INVARIANTS

- Aucun connecteur runtime.
- Aucun APPLY automatique.
- Aucun sync live.
- Aucun merge automatique.
- Aucun runtime touche.
- Aucun remplacement governance humaine.

## 16_TODO

- Cartographier les surfaces externes.
- Evaluer les risques runtime.
- Evaluer les risques autonomie IA.
- Evaluer les dependances multi-machine.
- Evaluer les besoins observabilite.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_DOC_OPS_WHY_EXTERNAL_ORCHESTRATION_SURFACES_01` pour cadrer les surfaces d'orchestration externes WHY.

## RISKS

- À qualifier.
