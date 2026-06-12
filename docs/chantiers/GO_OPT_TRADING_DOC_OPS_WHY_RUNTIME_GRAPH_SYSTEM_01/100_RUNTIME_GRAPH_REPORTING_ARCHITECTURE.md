# 100_RUNTIME_GRAPH_REPORTING_ARCHITECTURE

## Objectif

Structurer les sorties reporting du WHY runtime graph.

## Sorties candidates

| Sortie | Role |
| --- | --- |
| runtime_graph_report.json | sortie machine-readable |
| runtime_graph_summary.md | synthese humaine |
| runtime_graph_risk_map.md | cartographie risques |
| runtime_graph_review_gates.md | gates humaines |
| runtime_graph_failure_chains.md | chaines critiques |

## Niveaux reporting

| Niveau | Usage |
| --- | --- |
| governance | coherence WHY/runtime |
| runtime | surfaces critiques |
| audit | verification et preuves |
| human review | validation humaine |

## Regles

- Les rapports doivent rester explicables.
- Les preuves runtime doivent etre tracables.
- Les surfaces critiques doivent rester reviewables humainement.
- Les chaines critiques doivent etre visibles.

## Invariant

Les rapports du runtime graph ne doivent jamais devenir des validations runtime autonomes.

## RISKS

- À qualifier.
