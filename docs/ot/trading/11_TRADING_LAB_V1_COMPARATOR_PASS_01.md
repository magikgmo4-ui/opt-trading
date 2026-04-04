# TRADING LAB V1 — COMPARATOR PASS 01

Date (America/Montreal) : 2026-04-03

## RÔLE

Cette passe matérialise un comparateur simple entre sorties LAB et référence LIVE JSONL.

## MODIFICATIONS

- `modules/trading_lab_v1/app/comparator_v1.py`
- `modules/trading_lab_v1/data/sample_live_reference_v1.jsonl`
- `modules/trading_lab_v1/scripts/cmd.sh`
- `modules/trading_lab_v1/scripts/sanity.sh`

## CAPACITÉS

Le module sait maintenant :
- charger une référence LIVE JSONL ;
- comparer LAB et LIVE par `local_date + session_name` ;
- détecter `matched`, `lab_only`, `live_only` ;
- mesurer les écarts de variante, direction, entrée, stop et RR ;
- écrire les détails dans `state/trading_lab_v1/comparator_pairs_v1.jsonl` ;
- écrire un résumé dans `state/trading_lab_v1/comparator_reports_v1.jsonl`.

## COMMANDES

- `cmd-trading_lab_v1 show-live-reference`
- `cmd-trading_lab_v1 comparator-status`
- `cmd-trading_lab_v1 compare-live [live_jsonl_path] [session_id] [start_date] [end_date]`
- `cmd-trading_lab_v1 show-last-comparator-report`

## DÉCISION

Cette passe reste minimale : pas encore de vrai runner live, mais une couche exploitable de validation croisée LAB/LIVE.

## LIMITES

- pas encore de runner live natif ;
- pas encore d’export dédié du comparateur ;
- pas encore de comparaison continue.

## TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_LIVE_OBSERVATION_PASS_01`
