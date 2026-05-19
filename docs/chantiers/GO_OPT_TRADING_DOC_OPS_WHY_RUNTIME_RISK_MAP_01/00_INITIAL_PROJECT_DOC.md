---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_RISK_MAP_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_RISK_MAP_01
scope: governance
orientation: IA_AND_HUMAN
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Construire une cartographie runtime critique multi-machine orientee WHY afin de classifier les surfaces selon leur criticite, leurs invariants et leurs risques.

## 3_INITIAL_NEED

Le WHY layer est maintenant merge dans `sot/mainline`. La prochaine etape logique est de cartographier les surfaces runtime critiques avant toute automatisation WHY.

## 4_MASTER_PROJECT_PLAN

- Identifier les surfaces runtime critiques.
- Identifier les machines impliquees.
- Identifier les invariants critiques.
- Identifier les failure modes runtime.
- Identifier les dependances multi-machine.
- Construire une classification R0-R5 exploitable par gouvernance WHY.

## 6_FINAL_TARGET

Produire une carte runtime critique exploitable par:
- reviews,
- CI governance futures,
- lint WHY,
- audit IA,
- orchestration multi-machine.

## 7_CANONICAL_STATE

Le repo contient deja:
- des invariants,
- des gates,
- un split machine,
- des surfaces runtime critiques.

Mais:
- la criticite runtime n'est pas encore cartographiee globalement.

## 12_INVARIANTS

- Chantier doc-only.
- Aucun runtime.
- Aucun GO_INDEX.
- Aucun BRANCH_STATE.
- Aucune CI active.
- Aucune automatisation runtime.

## 16_TODO

- Cartographier admin-trading.
- Cartographier db-layer.
- Cartographier student.
- Cartographier cursor-ai.
- Evaluer criticite R0-R5.
- Evaluer dependances croisées.

## 17_RESUME_POINT

Reprendre depuis `go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_RISK_MAP_01` pour construire la premiere carte runtime critique WHY-oriented du repo.
