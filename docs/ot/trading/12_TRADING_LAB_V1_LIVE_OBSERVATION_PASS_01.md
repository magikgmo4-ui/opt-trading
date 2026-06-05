# TRADING LAB V1 — LIVE OBSERVATION PASS 01

Date (America/Montreal) : 2026-04-03

## RÔLE

Cette passe ouvre une branche LIVE native en mode observation.

## MODIFICATIONS

- `modules/trading_lab_v1/app/live_observation_v1.py`
- `modules/trading_lab_v1/scripts/cmd.sh`
- `modules/trading_lab_v1/scripts/sanity.sh`

## CAPACITÉS

Le module sait maintenant :
- lire une source LIVE JSONL ;
- normaliser ces entrées en observations ;
- écrire `state/trading_lab_v1/live_observations_v1.jsonl` ;
- écrire `state/trading_lab_v1/live_observation_runs_v1.jsonl`.

## COMMANDES

- `cmd-trading_lab_v1 live-observation-status`
- `cmd-trading_lab_v1 show-live-observation-source`
- `cmd-trading_lab_v1 observe-live [live_jsonl_path] [session_id] [start_date] [end_date]`
- `cmd-trading_lab_v1 show-last-live-observation-run`

## DÉCISION

Observation seulement : pas d’ordre réel, pas encore de runner live complet.

## TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_LIVE_EXPORT_PASS_01`

## RISKS

- À qualifier.
