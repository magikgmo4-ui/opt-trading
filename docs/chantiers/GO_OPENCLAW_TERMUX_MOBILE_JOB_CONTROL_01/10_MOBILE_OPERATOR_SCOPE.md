---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01_MOBILE_OPERATOR_SCOPE
doc_type: scope_doc
go_id: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01
status: open
updated_at: 2026-05-21
---

# 10_MOBILE_OPERATOR_SCOPE

## Objet

Definir ce que mobile/Termux peut faire dans le perimetre OpenClaw non-trading.

## Role mobile retenu

Mobile/Termux est une surface operateur. Il peut servir a :

- consulter l'etat des jobs non-trading ;
- consulter les sorties ledger/report/LocalCMS ;
- declencher un job read-only ou dry-run deja inscrit au registre ;
- recevoir un digest d'etat ;
- participer a un gate HITL comme validation humaine ;
- demander un preflight avant execution machine.

## Ce que mobile n'est pas

Mobile/Termux n'est pas :

- une source canonique ;
- un runtime autonome ;
- une surface de write externe libre ;
- un pont secret/env ;
- une surface de trading live ;
- une couche de bypass pour HITL ;
- une console Git destructive.

## Surfaces autorisees au depart

| Surface | Statut mobile | Notes |
|---|---|---|
| OpenClaw status | allowed | lecture et controle borne |
| Jobs register | allowed | lecture et selection de jobs deja enregistres |
| Phase packets | allowed | lecture et dry-run |
| Ledger | allowed | lecture et ajout via runner controle uniquement |
| Reports | allowed | lecture + generation locale bornee |
| LocalCMS snapshot | allowed | lecture + refresh local-only |
| HITL packets | allowed | validation humaine selon gate |
| External app writes | forbidden initially | Phase 08 seulement, write-gated |
| Signal/trading | forbidden | hors scope du GO |

## Mode d'operation initial

Le mode initial est `MOBILE_CONTROL_DRY_RUN` :

1. mobile demande un statut ;
2. OpenClaw lit le registre ;
3. OpenClaw propose les jobs autorises ;
4. mobile choisit un job autorise ;
5. preflight local ;
6. execution read-only/dry-run/local-only ;
7. ledger/report ;
8. LocalCMS snapshot si applicable.

## Evidence attendue

Chaque action mobile doit laisser au moins une preuve :

- stdout capture ou JSON report ;
- ledger event ;
- chemin d'artefact ;
- verdict PASS / PRECHECK_PASS / BLOCKED_WITH_REASON ;
- si gate humain : decision packet relisible.

## Garde-fou principal

Le mobile ne decide jamais seul de la mutation. Il peut demander, consulter, valider selon gate, ou declencher une action allowlistee. OpenClaw et les phase packets arbitrent l'action effective.
