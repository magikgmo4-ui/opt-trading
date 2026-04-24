# trading_lab_v1

Branche LAB V1 pour experimentation locale, batchs d'analyse et exports autour du dual stack XAUUSD.

## Role
- charger le profil V1 et les schemas de trading associes
- materialiser des echantillons `event` et `trade`
- executer des runs unitaires, batchs, extractions de features et comparaisons live
- produire des sorties d'observation et de reporting sous `state/trading_lab_v1`

## Contenu
- `app/trading_lab_v1.py` : runner principal du LAB
- `app/report_export_v1.py`, `comparator_v1.py`, `live_observation_v1.py`, `live_export_v1.py`
- `docs/README.md`, `RUNBOOK.txt`, `ETABLI.txt`
- `data/` : exemples locaux (`sample_xauusd_m1.csv`, `sample_live_reference_v1.jsonl`)
- `tests/` : tests du runner et des surfaces de reporting
- `scripts/cmd.sh`, `menu.sh`, `sanity.sh`

## Integration
- lit les schemas sous `docs/ot/trading/schemas/`
- persiste sous `state/trading_lab_v1`
- sert de pendant analytique a `modules/trading_realtime_v1`

## Statut
- actif
- verticale experimentale et analytique, sans execution live

## Notes de consolidation
- ne pas fusionner rapidement avec `trading_realtime_v1`
- `trading_lab_v1` = exploration, batch, comparaison, export
- releve d'une verticale specialisee a traiter a part du pipeline runtime principal
