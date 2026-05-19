# 110_RUNTIME_OBSERVABILITY_REQUIREMENTS

## Objectif

Documenter les exigences minimales d'observabilite runtime.

## Exigences minimales

| Surface | Observabilite requise |
| --- | --- |
| webhook TradingView | endpoints + logs + freshness |
| Telegram bot vision | logs + validation messages |
| ingestion snapshots | timestamps + etat latest.json |
| OpenClaw orchestration | supervision providers + sessions |
| dashboards observateurs | verification freshness |

## Exigences par classe

| Classe | Observabilite minimale |
| --- | --- |
| R0 | aucune |
| R1 | logs optionnels |
| R2 | logs obligatoires |
| R3 | logs + freshness |
| R4 | supervision critique |
| R5 | supervision forte + verification humaine |

## Observation

Une surface critique non observable devient:
- difficilement auditables,
- difficilement recuperable,
- dangereuse pour l'automatisation IA.

## Invariant

Toute surface R3/R4/R5 devrait produire des preuves runtime exploitables.
