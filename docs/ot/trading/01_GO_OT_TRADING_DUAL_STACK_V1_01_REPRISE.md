# GO_OT_TRADING_DUAL_STACK_V1_01 — REPRISE

Date (America/Montreal) : 2026-04-06

## OBJET
Point de reprise opératoire court pour la suite du chantier trading dual stack.

## BASE
- `docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`
- `docs/ot/trading/02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`
- `docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml`
- `docs/ot/trading/schemas/trading_event_v1.schema.json`
- `docs/ot/trading/schemas/trading_trade_v1.schema.json`
- `modules/trading_lab_v1/`
- `modules/trading_realtime_v1/`

## ÉTABLI
- dual stack Lab + Real-Time cadré ;
- noyau partagé exigé ;
- focus V1 = `XAUUSD`, timezone `America/Montreal`, fenêtres `18:00` et `00:00` ;
- schémas V1 matérialisés ;
- chaîne LAB posée ;
- comparator LAB/LIVE posé ;
- live observation posée ;
- live export posé ;
- squelette REALTIME V1 posé ;
- event bridge REALTIME posé ;
- reporting REALTIME posé ;
- export REALTIME posé ;
- runtime loop REALTIME posée ;
- guardrails REALTIME posés ;
- timer REALTIME posé ;
- closeout REALTIME V1 posé.

## COUVERT
- schéma commun ;
- config V1 ;
- schéma event V1 ;
- schéma trade V1 ;
- chaîne LAB ;
- comparator LAB/LIVE ;
- live observation ;
- live export ;
- squelette REALTIME V1 ;
- event bridge REALTIME ;
- reporting REALTIME ;
- export REALTIME ;
- runtime loop REALTIME ;
- guardrails REALTIME ;
- timer REALTIME ;
- closeout REALTIME V1.

## SUITE
Aucun nouveau chantier n’est recommandé par défaut.

## POINT DE REPRISE UNIQUE
`GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01`

## FORMULE COURTE
La chaîne minimale REALTIME V1 est fermée proprement au niveau repo et continuité canonique. Reprendre uniquement depuis `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` si un nouveau chantier réel doit être ouvert.
