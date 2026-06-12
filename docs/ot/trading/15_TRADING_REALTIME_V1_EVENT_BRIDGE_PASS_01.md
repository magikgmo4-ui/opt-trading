# TRADING REALTIME V1 — EVENT BRIDGE PASS 01

Date (America/Montreal) : 2026-04-04

## RÔLE

Cette passe relie les observations runtime REALTIME au format d’événements partagé.

## MODIFICATIONS

- `modules/trading_realtime_v1/app/event_bridge_v1.py`
- `modules/trading_realtime_v1/scripts/cmd.sh`
- `modules/trading_realtime_v1/scripts/menu.sh`
- `modules/trading_realtime_v1/scripts/sanity.sh`

## CAPACITÉS

Le module sait maintenant :
- lire la dernière observation runtime ;
- construire un événement runtime compatible avec le cadre V1 ;
- écrire `state/trading_realtime_v1/runtime_events_v1.jsonl` ;
- écrire `state/trading_realtime_v1/runtime_bridge_runs_v1.jsonl`.

## COMMANDES

- `cmd-trading_realtime_v1 bridge-status`
- `cmd-trading_realtime_v1 bridge-latest`
- `cmd-trading_realtime_v1 show-last-runtime-event`

## DÉCISION

Cette passe reste observation-only : elle pose un pont événementiel sans exécution d’ordre.

## TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_REALTIME_V1_REPORTING_PASS_01`

## RISKS

- À qualifier.
