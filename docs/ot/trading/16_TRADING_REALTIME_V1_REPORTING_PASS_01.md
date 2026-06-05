# TRADING REALTIME V1 — REPORTING PASS 01

Date (America/Montreal) : 2026-04-04

## RÔLE

Cette passe ajoute une couche de reporting dédiée au module REALTIME.

## MODIFICATIONS

- `modules/trading_realtime_v1/app/reporting_v1.py`
- `modules/trading_realtime_v1/scripts/cmd.sh`
- `modules/trading_realtime_v1/scripts/menu.sh`
- `modules/trading_realtime_v1/scripts/sanity.sh`

## CAPACITÉS

Le module sait maintenant :
- agréger les observations runtime ;
- agréger les runs runtime ;
- agréger les événements runtime ;
- agréger les runs du bridge ;
- écrire `state/trading_realtime_v1/runtime_reports_v1.jsonl`.

## COMMANDES

- `cmd-trading_realtime_v1 reporting-status`
- `cmd-trading_realtime_v1 report-runtime [session_id] [start_date] [end_date]`
- `cmd-trading_realtime_v1 show-last-runtime-report`

## DÉCISION

Cette passe reste observation-only : elle ajoute l’agrégation runtime, sans ouvrir l’exécution.

## TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_REALTIME_V1_EXPORT_PASS_01`

## RISKS

- À qualifier.
