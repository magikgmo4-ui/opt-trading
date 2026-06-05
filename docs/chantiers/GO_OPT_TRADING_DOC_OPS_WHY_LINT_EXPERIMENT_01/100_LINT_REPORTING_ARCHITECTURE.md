# 100_LINT_REPORTING_ARCHITECTURE

## Objectif

Structurer les sorties reporting du WHY lint experimental.

## Sorties candidates

| Sortie | Role |
| --- | --- |
| lint_report.json | sortie machine-readable |
| lint_summary.md | synthese humaine |
| lint_runtime_alignment.md | coherence runtime/governance |
| lint_warning_map.md | cartographie warnings |
| lint_review_gates.md | review humaine requise |

## Niveaux reporting

| Niveau | Usage |
| --- | --- |
| governance | coherence WHY/runtime |
| runtime | surfaces critiques |
| audit | verification documentaire |
| human review | preparation validation humaine |

## Regles

- Les rapports doivent rester explicables.
- Les warnings doivent rester contextualises.
- Les surfaces critiques doivent rester reviewables humainement.
- Les preuves runtime doivent etre tracables.

## Invariant

Les rapports lint ne doivent jamais devenir des validations runtime autonomes.

## RISKS

- À qualifier.
