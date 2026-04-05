# TRADING REALTIME V1 — GUARDRAILS PASS 01

Date (America/Montreal) : 2026-04-05

## RÔLE

Cette passe ajoute des garde-fous explicites au module REALTIME.

## MODIFICATIONS

- `modules/trading_realtime_v1/app/guardrails_v1.py`
- `modules/trading_realtime_v1/scripts/cmd.sh`
- `modules/trading_realtime_v1/scripts/menu.sh`
- `modules/trading_realtime_v1/scripts/sanity.sh`

## CAPACITÉS

Le module sait maintenant :
- vérifier que les derniers artefacts runtime restent en `observation_only` ;
- vérifier que les événements runtime restent en `mode=observation` ;
- vérifier qu’aucun indicateur d’exécution n’apparaît ;
- écrire `state/trading_realtime_v1/runtime_guardrails_reports_v1.jsonl`.

## COMMANDES

- `cmd-trading_realtime_v1 guardrails-status`
- `cmd-trading_realtime_v1 check-guardrails`
- `cmd-trading_realtime_v1 show-last-guardrails-report`

## DÉCISION

Cette passe renforce la sécurité fonctionnelle du runtime sans ouvrir l’exécution d’ordre.

## TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_REALTIME_V1_TIMER_PASS_01`
