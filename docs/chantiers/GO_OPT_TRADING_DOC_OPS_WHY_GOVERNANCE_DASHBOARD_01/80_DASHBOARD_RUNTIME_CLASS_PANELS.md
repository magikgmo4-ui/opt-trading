# 80_DASHBOARD_RUNTIME_CLASS_PANELS

## Objectif

Definir les panneaux classes runtime R0-R5 du futur WHY governance dashboard.

## Panneaux candidats

| Panel | Role |
| --- | --- |
| R0_INFORMATION | surfaces informationnelles |
| R1_LOW_CRITICALITY | faible criticite |
| R2_MODERATE_RUNTIME | orchestration moderee |
| R3_CRITICAL_CONTEXTUAL | orchestration critique contextualisee |
| R4_CRITICAL_RUNTIME | runtime critique |
| R5_MAX_CRITICAL_RUNTIME | criticite maximale |

## Regles

- Chaque surface critique doit afficher sa classe runtime.
- Les surfaces R4/R5 doivent afficher review humaine et observabilite.
- Les promotions de criticite doivent etre explicables.
- Les classes runtime doivent rester contextualisees.

## Observation

Les panneaux doivent aider a:
- comprendre les niveaux de criticite,
- comprendre les dependances runtime,
- comprendre les besoins review humaine.

## Invariant

Les panneaux R0-R5 ne doivent jamais devenir une autorite runtime autonome.

## RISKS

- À qualifier.
