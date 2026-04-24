# trading_realtime_v1

Branche REALTIME V1 en mode observation, separee du LAB et sans passage d'ordres reels.

## Role
- charger le profil V1 et les schemas de trading associes
- observer une source live de reference
- materialiser des runs runtime, guardrails, reporting et exports
- produire des sorties d'observation sous `state/trading_realtime_v1`

## Contenu
- `app/trading_realtime_v1.py` : entrypoint principal observation-only
- `app/event_bridge_v1.py`, `reporting_v1.py`, `export_v1.py`, `runtime_loop_v1.py`, `guardrails_v1.py`, `timer_v1.py`
- `docs/README.md`, `RUNBOOK.txt`, `ETABLI.txt`
- `tests/` : tests des surfaces runtime
- `scripts/cmd.sh`, `menu.sh`, `sanity.sh`

## Integration
- lit les schemas sous `docs/ot/trading/schemas/`
- reutilise `modules/trading_lab_v1/data/sample_live_reference_v1.jsonl` comme source live par defaut
- persiste sous `state/trading_realtime_v1`
- mode strictement `observation_only`

## Statut
- actif
- verticale runtime d'observation, sans execution de trading

## Notes de consolidation
- ne pas fusionner rapidement avec `trading_lab_v1`
- `trading_realtime_v1` = observation runtime, boucle, bridge, guardrails, timer
- releve d'une verticale specialisee a traiter a part du pipeline runtime principal
