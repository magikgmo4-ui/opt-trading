# TRADING REALTIME V1 — RUNTIME LOOP PASS 01

Date (America/Montreal) : 2026-04-04

## RÔLE

Cette passe ajoute une boucle runtime contrôlée pour le module REALTIME.

## MODIFICATIONS

- `modules/trading_realtime_v1/app/runtime_loop_v1.py`
- `modules/trading_realtime_v1/scripts/cmd.sh`
- `modules/trading_realtime_v1/scripts/menu.sh`
- `modules/trading_realtime_v1/scripts/sanity.sh`

## CAPACITÉS

Le module sait maintenant :
- lire la dernière entrée LIVE ;
- écrire une observation runtime ;
- construire un événement runtime ;
- écrire un rapport runtime ;
- écrire un journal de boucle dans `state/trading_realtime_v1/runtime_loop_runs_v1.jsonl`.

## COMMANDES

- `cmd-trading_realtime_v1 runtime-loop-status`
- `cmd-trading_realtime_v1 runtime-loop-once [live_jsonl_path]`
- `cmd-trading_realtime_v1 show-last-runtime-loop-run`

## DÉCISION

Cette passe reste observation-only : elle pose une boucle contrôlée, sans exécution d’ordre.

## TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_REALTIME_V1_GUARDRAILS_PASS_01`
