# 10_RUNTIME_SURFACES_MAP

## Objectif

Lister les surfaces runtime connues et les rattacher a une classe de criticite WHY preliminaire.

## Classes

| Classe | Sens |
| --- | --- |
| R0 | doc-only |
| R1 | tooling local non critique |
| R2 | runtime observable |
| R3 | orchestration multi-machine |
| R4 | trading live / execution critique |
| R5 | impact financier direct automatise |

## Surfaces preliminaires

| Surface | Machine principale | Classe candidate | Note WHY |
| --- | --- | --- | --- |
| docs/chantiers | toutes | R0 | documentation et reprise |
| docs/governance | toutes | R0 | doctrine et gates |
| scripts locaux d'operation | cursor-ai / student | R1 | outils non critiques |
| dashboards observateurs | cursor-ai / admin-trading | R2 | lecture / observation |
| OpenClaw orchestration | db-layer | R3 | orchestration multi-composants |
| Telegram bot vision | admin-trading | R3 | pont multi-systeme |
| webhook TradingView | admin-trading | R4 | signal trading live |
| ingestion snapshots desk | admin-trading | R3 | dependance vision / desk |
| execution financiere automatique | non ouverte | R5 | doit rester gatee |

## Invariant

Cette carte est preliminaire et ne change aucun statut runtime.
