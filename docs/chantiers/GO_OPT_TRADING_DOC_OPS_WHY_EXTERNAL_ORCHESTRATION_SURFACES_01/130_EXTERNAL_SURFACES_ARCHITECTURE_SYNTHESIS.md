# 130_EXTERNAL_SURFACES_ARCHITECTURE_SYNTHESIS

## Objectif

Synthétiser l'architecture WHY des surfaces d'orchestration externes candidates.

## Synthese

Le chantier cadre les surfaces externes comme:
- couches assistives,
- surfaces governance potentielles,
- sources de propagation de statut,
- dependances multi-machine candidates,
- composants auditables avant toute integration runtime.

## Surfaces couvertes

| Surface | Role candidat | Classe candidate |
| --- | --- | --- |
| ClickUp | suivi / priorisation | R2/R3 |
| Botpress | orchestration conversationnelle | R3 |
| Knowledge Graph | coherence relationnelle | R3 |
| Airtable | structuration operations | R2/R3 |

## Architecture retenue

| Couche | Role |
| --- | --- |
| classification | positionner les surfaces candidates |
| runtime risk | identifier risques runtime |
| autonomy risk | limiter derive IA |
| governance relation | relier au WHY layer |
| multi-machine impact | evaluer propagation cross-machine |
| observability | exiger tracabilite |
| runtime boundaries | verrouiller limites |
| human review gates | preserver gouvernance humaine |
| runtime alignment | relier R0-R5 |
| autonomy limits | bloquer autonomie critique |
| reporting architecture | preparer audit |
| integration roadmap | ordonner futures integrations |

## Resultat structurel

Le repo dispose maintenant d'un cadrage WHY pour evaluer ClickUp, Botpress, KG et Airtable avant toute integration active.

## Invariant final

Aucune surface externe ne doit devenir source runtime autonome, orchestrateur implicite ou autorite governance sans WHY explicite, observabilite, reprise et review humaine.

## RISKS

- À qualifier.
