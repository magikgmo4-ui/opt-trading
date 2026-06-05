# TRADING DUAL STACK V1 — SYNTHÈSE CANONIQUE PRODUIT

## Lecture canonique

- lire cette synthese apres `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- recroiser `docs/governance/MATRICE_GOUVERNANTE_V2.md` seulement comme annexe stable secondaire si utile

## 1. Objet
Ce document synthétise le produit **Trading Dual Stack V1** dans un format court et opposable, figeant son objectif final et son état réel.

## 2. Besoin initial
Éviter d'avoir un laboratoire (LAB) d'un côté et un environnement de production (REALTIME) de l'autre qui divergent.

## 3. Objectif final visé
Framework trading unique avec un même noyau LAB/REALTIME, imposant la discipline au trader, forçant la validation avant l'autonomie, et produisant une journalisation exploitable.

## 4. Plan validé
- Unification LAB + REALTIME autour d'un noyau commun (frame / strategy / execution / analytics).
- Périmètre V1 étroit et borné : XAUUSD, America/Montreal, 18:00 à 20:00.
- REALTIME limité à l'observation puis validation (full auto-trading hors périmètre pour la V1).

## 5. État obtenu
- Schémas et configuration V1 établis.
- Chaîne LAB et comparateur opérationnels.
- Chaîne REALTIME minimale posée.
- V1 close de manière repo-sourcée et canonique.

## 6. Gap restant
- V1 close mais bornée : sans broker connecté, sans passage d'ordre réel, sans auto-trading.

## 7. Prochain GO recommandé
> GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01 (uniquement si besoin d'extension réelle identifié)

## RISKS

- À qualifier.
