# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Évaluer si le pack documentaire OpenClaw builder adopté localement doit être référencé dans une surface d'indexation plus globale, sans modifier les index globaux dans ce child.

## 2_INITIAL_PROJECT_DOC

Ce document initialise le child GO de revue d'indexation documentaire builder. Il reste la référence figée du cadrage initial du chantier.

## 3_INITIAL_NEED

La chaîne builder documentation est complète et mergée. Le pack documentaire a été adopté localement. Il faut maintenant décider si une indexation globale est nécessaire, utile et sûre, sans agir directement sur les index globaux.

## 4_MASTER_PROJECT_PLAN

1. Relire la décision d'adoption locale.
2. Identifier les surfaces d'indexation candidates.
3. Évaluer les risques de duplication ou de mauvaise autorité.
4. Produire une matrice d'indexation.
5. Statuer : NO_INDEXATION / LOCAL_REFERENCE_ONLY / INDEXATION_RECOMMENDED.
6. Fermer le child avec un NEXT_GO seulement si une action d'indexation est réellement validée.

## 6_FINAL_TARGET

Produire une décision claire sur l'indexation du pack documentaire builder, sans modifier `GO_INDEX`, `ACTIVE_STREAMS`, `NEXT_GO`, `REPRISE`, `BRANCH_STATE` ou équivalent global.

## 12_INVARIANTS

- Aucun SSH.
- Aucun patch runtime.
- Aucun fix gateway token.
- Aucune modification des index globaux.
- Aucune modification de `ACTIVE_STREAMS`.
- Aucune modification de `GO_INDEX`.
- Aucune modification de `NEXT_GO`.
- Aucune modification de `REPRISE`.
- Aucune modification de `BRANCH_STATE`.
- Ce child est une revue de décision seulement.

## 16_TODO

- Créer `01_INDEXATION_CANDIDATE_MATRIX.md`.
- Créer `02_INDEXATION_DECISION.md`.
- Fermer avec `90_CHILD_CLOSEOUT.md`.

## 17_RESUME_POINT

Reprendre à la rédaction de `01_INDEXATION_CANDIDATE_MATRIX.md`.
