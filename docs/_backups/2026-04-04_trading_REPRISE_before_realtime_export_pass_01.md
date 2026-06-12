# GO_OT_TRADING_DUAL_STACK_V1_01 — REPRISE

Date (America/Montreal) : 2026-04-04

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
- reporting REALTIME posé.

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
- reporting REALTIME avec `runtime_reports_v1.jsonl`.

## SUITE
Suite recommandée immédiate : ouvrir une passe **REALTIME export** pour produire un rendu lisible/transportable des rapports runtime.

## TRIGGER NATUREL SUIVANT
`GO_OT_TRADING_REALTIME_V1_EXPORT_PASS_01`

## FORMULE COURTE
Reprendre depuis les docs `docs/ot/trading/`, les fichiers `schemas/`, puis `modules/trading_lab_v1/` et `modules/trading_realtime_v1/`, et ouvrir la passe REALTIME export avant toute montée en charge runtime.

## RISKS

- À qualifier.
