# TRADING REALTIME V1 — TIMER PASS 01

Date (America/Montreal) : 2026-04-05

## RÔLE

Cette passe ajoute un timer contrôlé au module REALTIME.

## MODIFICATIONS

- `modules/trading_realtime_v1/app/timer_v1.py`
- `modules/trading_realtime_v1/scripts/cmd.sh`
- `modules/trading_realtime_v1/scripts/menu.sh`
- `modules/trading_realtime_v1/scripts/sanity.sh`

## CAPACITÉS

Le module sait maintenant :
- exposer un plan de timer contrôlé ;
- déclencher un tick unique ;
- enchaîner runtime loop puis check guardrails ;
- écrire `state/trading_realtime_v1/runtime_timer_runs_v1.jsonl`.

## COMMANDES

- `cmd-trading_realtime_v1 timer-status`
- `cmd-trading_realtime_v1 show-timer-plan`
- `cmd-trading_realtime_v1 timer-tick-once [live_jsonl_path]`
- `cmd-trading_realtime_v1 show-last-timer-run`

## DÉCISION

Cette passe reste contrôlée et observation-only : aucun daemon système, aucun scheduler externe, aucun ordre réel.

## TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_REALTIME_V1_CLOSEOUT_01`
