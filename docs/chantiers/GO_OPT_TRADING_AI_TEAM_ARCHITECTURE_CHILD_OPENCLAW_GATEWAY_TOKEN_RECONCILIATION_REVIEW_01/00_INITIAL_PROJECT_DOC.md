# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Analyser le warning `gateway token mismatch` observé pendant la chaîne builder docs, identifier la cause exacte, et décider de l'action : NO_ACTION / CONFIG_DOC_ONLY / TOKEN_RECONCILIATION_NEEDED / RUNTIME_HARDENING_GO_NEEDED.

## 2_INITIAL_PROJECT_DOC

Ce document initialise le child GO de revue du token gateway OpenClaw. Il reste la référence figée du cadrage initial du chantier.

## 3_INITIAL_NEED

Pendant la chaîne builder documentation, chaque invocation `openclaw agent --agent builder` produit un warning `gateway token mismatch`, puis retombe en mode embedded. L'exécution réussit, mais le gateway direct n'est pas utilisé. La cause est documentée ici pour décision.

## 4_MASTER_PROJECT_PLAN

1. Lire les artefacts source du warning.
2. Inspecter les configs gateway concernées.
3. Identifier la cause exacte (config manquante, token absent, mauvais user).
4. Produire une matrice de diagnostic.
5. Statuer sur l'action requise.
6. Ne rien patcher dans ce child sauf si la décision est TOKEN_RECONCILIATION_NEEDED et que la gate le permet.

## 6_FINAL_TARGET

Décision documentée et traçable sur le gateway token mismatch, avec action clairement bornée.

## 12_INVARIANTS

- Aucun SSH sans gate explicite.
- Aucun patch runtime sans gate explicite.
- Aucune modification index global.
- Ce child est une revue d'abord — toute action de patch doit être gatée séparément si la décision le demande.

## 16_TODO

- Créer `01_GATEWAY_TOKEN_DIAGNOSTIC.md`.
- Créer `02_GATEWAY_TOKEN_DECISION.md`.
- Fermer avec `90_CHILD_CLOSEOUT.md`.

## 17_RESUME_POINT

Reprendre à la rédaction de `01_GATEWAY_TOKEN_DIAGNOSTIC.md`.

## RISKS

- À qualifier.
