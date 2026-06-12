---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: review
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_START — Admin Trading Parent Review

## GO

GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Objectif

Auditer admin-trading comme machine runtime trading reelle, en read-only, sans modifier le runtime.

## Contexte

- Apres fermeture gouvernance / matrice / naming
- db-layer, cursor-ai, fantome et student consolides
- admin-trading = derniere machine runtime trading differee
- Cet audit est le premier pas avant tout GO runtime trading

## Regles strictes

- Patch prioritairement documentaire
- Aucun changement runtime
- Aucun redemarrage service
- Aucun stop/start service
- Aucun changement config
- Aucun secret expose
- Aucun token Telegram expose
- Aucun .env affiche integralement
- Aucun trading reel declenche
- Aucun webhook declenche volontairement
- Les controles doivent rester read-only

## Methode

1. Lire les index canoniques (GO_INDEX, GO_CLOSED_INDEX, GO_PARENT_THREAD_MAP, REPRISE, ACTIVE_STREAMS, NEXT_GO_CANDIDATES, BRANCH_STATE)
2. Lire les chantiers parents admin-trading
3. Scanner le repo pour les references admin-trading
4. Tenter SSH read-only vers admin-trading
5. En cas d'echec SSH, documenter l'etat observable depuis le repo et les autres machines
6. Cartographier les surfaces trading attendues
7. Identifier les gaps et recommander les prochains GO

## Resultat

Voir 90_CLOSEOUT.md

## RISKS

- À qualifier.
