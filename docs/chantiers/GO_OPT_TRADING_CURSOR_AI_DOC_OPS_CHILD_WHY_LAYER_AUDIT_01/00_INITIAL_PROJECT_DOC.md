---
doc_id: GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01_INITIAL_PROJECT_DOC
repo: opt-trading
machine: cursor-ai
status: active
branch: go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01
parent_go: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Construire une couche documentaire explicite du WHY layer deja present dans le repo opt-trading.

## 3_INITIAL_NEED

Audit complet du trunk afin de verifier si le repo enseigne deja le "pourquoi" a une IA.

## 4_MASTER_PROJECT_PLAN

- Lire la gouvernance et les docs produit.
- Identifier les invariants, arbitrages et raisons structurelles.
- Evaluer la presence du WHY implicite et explicite.
- Produire une doctrine WHY layer centralisable.

## 6_FINAL_TARGET

Documenter une architecture WHY exploitable par humain + IA sans modifier le runtime.

## 7_CANONICAL_STATE

Le WHY existe deja principalement sous forme:
- d'invariants,
- de doctrine,
- de separation audit/apply,
- de logique PASS/FAIL,
- d'anti-derive,
- de structures de reprise.

Le gap principal est l'absence d'une couche WHY centralisee et explicitement indexee.

## 12_INVARIANTS

- Chantier doc-only.
- Aucun runtime.
- Aucun index global sauf rattachement machine explicite.
- Aucun refactor produit.
- Aucun changement de statut global.

## RISKS

- À qualifier.
