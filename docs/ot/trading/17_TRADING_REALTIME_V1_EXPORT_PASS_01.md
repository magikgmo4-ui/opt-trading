# TRADING REALTIME V1 — EXPORT PASS 01

Date (America/Montreal) : 2026-04-04

## RÔLE

Cette passe ajoute un export lisible pour le reporting du module REALTIME.

## MODIFICATIONS

- `modules/trading_realtime_v1/app/export_v1.py`
- `modules/trading_realtime_v1/scripts/cmd.sh`
- `modules/trading_realtime_v1/scripts/menu.sh`
- `modules/trading_realtime_v1/scripts/sanity.sh`

## CAPACITÉS

Le module sait maintenant :
- exporter le dernier rapport runtime ;
- générer puis exporter un rapport runtime filtré ;
- produire des exports `.json` et `.md` dans `state/trading_realtime_v1/runtime_exports/`.

## COMMANDES

- `cmd-trading_realtime_v1 export-status`
- `cmd-trading_realtime_v1 export-last-runtime-report`
- `cmd-trading_realtime_v1 export-runtime-report [session_id] [start_date] [end_date]`

## DÉCISION

Le rendu runtime est séparé du reporting : agrégation et export restent deux responsabilités distinctes.

## TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_REALTIME_V1_RUNTIME_LOOP_PASS_01`
