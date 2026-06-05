---
doc_id: SYSTEM_WHY_LAYER_01
repo: opt-trading
status: draft
scope: governance
orientation: IA_AND_HUMAN
---

# SYSTEM_WHY_LAYER_01

## Objectif

Centraliser les raisons structurelles qui gouvernent les decisions du repo opt-trading.

Le but n'est pas seulement de documenter des procedures mais:
- l'intention,
- les invariants,
- les risques,
- les arbitrages,
- les limites d'autonomie.

## Pourquoi ce repo existe

Le repo sert a construire un systeme operatoire multi-machine orienté:
- trading,
- orchestration,
- gouvernance documentaire,
- reprise robuste,
- execution controlee.

## Pourquoi etat reel > memoire

La memoire humaine ou IA peut diverger.

Le repo impose:
- preuve runtime,
- preuve Git,
- preuve documentaire,
comme sources d'autorite.

## Pourquoi produit > parent > GO > Git

Une branche Git ne prouve pas une intention produit.

L'ordre protege:
- la coherence fonctionnelle,
- la continuite produit,
- l'anti-derive documentaire.

## Pourquoi le patch minimal existe

Un refactor massif peut:
- casser des consommateurs,
- introduire des regressions invisibles,
- melanger plusieurs surfaces runtime.

Le patch minimal protege la stabilite.

## Pourquoi les gates PASS/FAIL existent

Empêcher:
- les validations floues,
- les demi-etats,
- les runtime non verifies,
- les merges prematures.

## Pourquoi le split machine existe

Eviter:
- collisions Git,
- confusion runtime,
- melange des responsabilites,
- contamination multi-machine.

## Pourquoi la separation AUDIT/APPLY existe

Une IA peut proposer une action sans comprendre tous les impacts.

La separation force:
- observation,
- verification,
- arbitrage,
avant execution.

## Failure modes critiques

- hallucination documentaire,
- optimisation naive IA,
- confusion branche = produit,
- convergence artificielle,
- runtime non cadre,
- derive autonome.

## Tradeoffs structurels

- stabilite > vitesse,
- semantique reelle > convergence artificielle,
- auditabilite > automatisation totale,
- reprise robuste > simplification excessive.

## Direction future

Le WHY layer doit devenir:
- transversal,
- indexable,
- opposable,
- lisible par humain + IA,
- exploitable avant toute phase APPLY.

## RISKS

- À qualifier.
