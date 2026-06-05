# 30_CONVERGENCE_SHARED_REPORT_MODEL

## Objectif

Definir les modeles de reporting partages entre les couches WHY.

## Sorties candidates

| Sortie | Producteur |
| --- | --- |
| parser_report.json | WHY parser |
| score_report.json | score generator |
| lint_report.json | lint experiment |
| runtime_graph_report.json | runtime graph |
| worker_audit_report.json | worker audit |
| governance_dashboard_summary.md | dashboard |

## Champs candidats

| Champ | Usage |
| --- | --- |
| why_score | maturite WHY |
| runtime_class | criticite R0-R5 |
| warnings | gaps documentaires |
| recovery_paths | reprise runtime |
| review_required | governance humaine |
| observability_status | preuves runtime |

## Regles

- Les rapports doivent rester explicables.
- Les surfaces critiques doivent rester reviewables humainement.
- Les warnings doivent rester contextualises.
- Les preuves runtime doivent etre tracables.

## Invariant

Les rapports WHY ne doivent jamais devenir des validations runtime autonomes.

## RISKS

- À qualifier.
