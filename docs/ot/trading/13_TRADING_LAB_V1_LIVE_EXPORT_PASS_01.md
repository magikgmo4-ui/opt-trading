# TRADING LAB V1 — LIVE EXPORT PASS 01

Date (America/Montreal) : 2026-04-03

## RÔLE

Cette passe ajoute un export lisible pour la branche LIVE observation.

## MODIFICATIONS

- `modules/trading_lab_v1/app/live_export_v1.py`
- `modules/trading_lab_v1/scripts/cmd.sh`
- `modules/trading_lab_v1/scripts/sanity.sh`

## CAPACITÉS

Le module sait maintenant :
- exporter la dernière observation LIVE ;
- exporter une observation LIVE filtrée depuis une source JSONL ;
- produire des exports `.json` et `.md` dans `state/trading_lab_v1/live_exports/`.

## COMMANDES

- `cmd-trading_lab_v1 live-export-status`
- `cmd-trading_lab_v1 export-last-live-observation`
- `cmd-trading_lab_v1 export-live-observation [live_jsonl_path] [session_id] [start_date] [end_date]`

## DÉCISION

Le rendu LIVE est séparé du runner d’observation : observation et export restent deux responsabilités distinctes.

## TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_REALTIME_V1_SKELETON_PASS_01`

## RISKS

- À qualifier.
