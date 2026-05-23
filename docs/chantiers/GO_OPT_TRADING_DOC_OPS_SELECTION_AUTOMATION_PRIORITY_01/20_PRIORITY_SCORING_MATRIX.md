---
doc_id: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01_SCORING_MATRIX
doc_type: scoring_matrix
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01
status: active
updated_at: 2026-05-23
---

# 20_PRIORITY_SCORING_MATRIX

## Critères de notation (1 à 5)
- **F** : Fréquence observée (5=très fréquent)
- **I** : Impact attendu (5=impact fort)
- **C** : Simplicité d'implémentation (5=très simple)
- **R** : Absence de risque de dérive (5=aucun risque)
- **V** : Capacité DOC_OPS à valider sans runtime (5=facile à valider)
- **G** : Gain sur continuité (5=gain majeur)
- **D** : Indépendance (5=aucune dépendance)
- **Rev** : Réversibilité (5=totalement réversible)

## Matrice de Score

| Candidat | F | I | C | R | V | G | D | Rev | Total |
|---|---|---|---|---|---|---|---|---|---|
| 1. GO Naming + Dir Creation | 5 | 5 | 4 | 4 | 5 | 5 | 5 | 5 | **38** |
| 2. Initial Doc Generation | 4 | 4 | 4 | 5 | 5 | 4 | 4 | 5 | **35** |
| 3. Closeout Doc Generation | 4 | 3 | 3 | 5 | 4 | 4 | 3 | 5 | **31** |
| 4. Inbox Entry Creation | 4 | 4 | 5 | 5 | 5 | 5 | 4 | 5 | **37** |
| 5. Keyword + Constraint Val | 5 | 5 | 3 | 4 | 4 | 5 | 3 | 5 | **34** |
| 6. Branch State Tracking | 2 | 2 | 3 | 5 | 5 | 3 | 2 | 5 | **27** |
| 7. Surface-Specific Val | 3 | 4 | 2 | 3 | 3 | 4 | 2 | 4 | **25** |
| 8. Deduplication | 1 | 2 | 1 | 4 | 3 | 2 | 2 | 5 | **20** |
| 9. Metrics & Dashboards | 2 | 3 | 2 | 5 | 5 | 3 | 4 | 5 | **29** |
| 10. Template Versioning | 2 | 3 | 3 | 5 | 5 | 3 | 4 | 4 | **29** |
| 11. Git State Verification | 5 | 4 | 5 | 5 | 5 | 4 | 5 | 5 | **38** |
| 12. Constraint Checking Lite | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 5 | **39** |

## Analyse des résultats
- **Top 1** : Candidat 12 (**Constraint Checking Lite**) avec un score de 39. Sa simplicité et son impact sur la sécurité/conformité le rendent prioritaire.
- **Top 2** : Candidat 1 (**GO Naming + Directory Creation**) et Candidat 11 (**Git State Verification**) avec un score de 38.
- **Top 3** : Candidat 4 (**Inbox Entry Creation**) avec un score de 37.

## Décision
Les automatisations retenues pour la shortlist sont la validation de contraintes (Lite) et la création de chantiers (Naming + Directory). La vérification de l'état Git est également un excellent candidat qui pourra être intégré dans le flux de création.
