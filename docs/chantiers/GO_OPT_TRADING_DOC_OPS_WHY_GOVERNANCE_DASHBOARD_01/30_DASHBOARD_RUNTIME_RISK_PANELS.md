# 30_DASHBOARD_RUNTIME_RISK_PANELS

## Objectif

Definir les panneaux risques runtime du futur WHY governance dashboard.

## Panneaux candidats

| Panel | Role |
| --- | --- |
| R0-R5_RISK_MAP | cartographie criticite runtime |
| FAILURE_CHAINS | chaines de defaillance |
| OBSERVABILITY_ALERTS | pertes observabilite |
| MULTI_MACHINE_RISKS | risques cross-machine |
| EXTERNAL_SURFACE_RISKS | risques surfaces externes |
| GOVERNANCE_GAPS | gaps WHY critiques |

## Regles

- Les risques critiques doivent etre visibles.
- Les surfaces R4/R5 doivent etre explicites.
- Les dependances critiques doivent etre tracables.
- Les chaines de propagation doivent rester lisibles.

## Observation

Les panneaux doivent aider a:
- comprendre les risques,
- comprendre les dependances,
- comprendre les gaps governance,
- preparer les reviews humaines.

## Invariant

Les panneaux risques ne doivent jamais devenir des validations runtime autonomes.
