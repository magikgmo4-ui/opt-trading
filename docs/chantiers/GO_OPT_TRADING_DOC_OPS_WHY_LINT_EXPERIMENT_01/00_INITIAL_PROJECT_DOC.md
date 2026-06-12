---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
scope: doc_ops
parent_context: SYSTEM_WHY_LAYER_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer un lint WHY experimental non destructif, warning-only, lecture seule, sans auto-fix et sans CI bloquante.

## WHY

Ce cadrage existe pour verifier les gaps documentaires avant toute extension du systeme, en gardant la lecture seule, le warning-only et la separation stricte d'avec le runtime.

## 3_INITIAL_NEED

Le repo possede maintenant:
- WHY governance,
- runtime governance,
- parser WHY,
- score generator,
- worker audit,
- runtime graph,
- governance dashboard.

Il manque un cadrage de lint experimental pour verifier les gaps documentaires et la coherence runtime/governance sans modifier le systeme.

## 4_MASTER_PROJECT_PLAN

- Definir le scope du lint WHY.
- Definir les regles warning-only.
- Definir les surfaces documentaires cibles.
- Definir les gaps detectables.
- Definir les limites d'autonomie.
- Preparer une future governance CI experimentale non bloquante.

## 6_FINAL_TARGET

Produire une specification doc-only du WHY lint experiment.

## 7_CANONICAL_STATE

Le lint WHY doit rester:
- non destructif,
- warning-only,
- lecture seule,
- sans auto-fix,
- sans CI bloquante,
- sans APPLY automatique.

## 12_INVARIANTS

- Aucun runtime touche.
- Aucun lint executable cree.
- Aucune CI active.
- Aucun auto-fix.
- Aucun FAIL runtime autonome.
- Aucun merge automatique.
- Aucune review humaine remplacee.

## 16_TODO

- Definir lint scope.
- Definir lint rules.
- Definir warning levels.
- Definir target documents.
- Definir runtime/governance coherence checks.
- Definir output reports.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01` pour cadrer le WHY lint experimental non destructif.

## RISKS

- À qualifier.
