---
doc_id: WHY_AUDIT_AUTOMATION_01
repo: opt-trading
status: draft
scope: governance
orientation: IA_AND_HUMAN
parent: SYSTEM_WHY_LAYER_01
---

# WHY_AUDIT_AUTOMATION_01

## Objectif

Cadrer une future automatisation d'audit WHY documentaire.

## Vision

Un worker documentaire pourrait:
- scanner les GO,
- evaluer le WHY score,
- detecter les gaps,
- detecter les surfaces critiques sans invariants,
- produire des rapports de gouvernance.

## Capacites candidates

| Capacite | But |
| --- | --- |
| scan markdown | detecter sections WHY |
| score WHY | evaluer maturite |
| detection gaps | trouver documents incomplets |
| correlation produit | verifier coherence parent |
| audit reprise | verifier resume points |

## Limites

- ne pas autoriser APPLY automatique,
- ne pas inferer des intentions produit non prouvees,
- ne pas remplacer les reviews critiques humaines.

## Risques

- faux positifs documentaires,
- hallucination semantique IA,
- score WHY trompeur,
- enforcement excessif.

## Invariant

L'automatisation WHY reste une aide d'audit et non une autorite autonome.
