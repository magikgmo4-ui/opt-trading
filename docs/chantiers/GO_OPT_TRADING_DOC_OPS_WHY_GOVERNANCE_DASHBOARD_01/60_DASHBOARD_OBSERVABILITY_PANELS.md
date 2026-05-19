# 60_DASHBOARD_OBSERVABILITY_PANELS

## Objectif

Definir les panneaux observabilite du futur WHY governance dashboard.

## Panneaux candidats

| Panel | Role |
| --- | --- |
| LOG_SOURCES | journaux runtime |
| ENDPOINT_HEALTH | endpoints critiques |
| SNAPSHOT_FRESHNESS | freshness runtime |
| ALERT_STATUS | alertes critiques |
| REVIEW_PROOFS | preuves review humaine |
| OBSERVABILITY_GAPS | trous observabilite |

## Regles

- Les preuves runtime doivent etre visibles.
- Les surfaces critiques doivent etre observables.
- Les pertes observabilite doivent etre detectables.
- Les preuves review humaine doivent etre accessibles.

## Invariant

Les panneaux observabilite ne doivent jamais remplacer une validation runtime humaine.
