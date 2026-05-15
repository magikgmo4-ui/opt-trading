# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Appliquer la réconciliation du token gateway OpenClaw : définir `gateway.remote.token` égal à `gateway.auth.token` dans la config client, valider que le gateway direct fonctionne, sans exposer ni committer de valeur de token.

## 2_INITIAL_PROJECT_DOC

Ce document initialise le child GO de patch gateway token. Il reste la référence figée du cadrage initial du chantier.

## 3_INITIAL_NEED

La revue précédente a identifié que `gateway.remote.token` est absent dans la config openclaw client. Le gateway direct échoue avec `token mismatch` et retombe en embedded. Ce child applique le fix local de config.

## 4_MASTER_PROJECT_PLAN

1. Poser la gate de patch explicite.
2. Passer la gate.
3. Lire le token auth existant (sans l'imprimer).
4. Écrire `gateway.remote.token` = valeur du token auth.
5. Vérifier gateway health/probe.
6. Journaliser le résultat.
7. Fermer le child.

## 6_FINAL_TARGET

Gateway direct opérationnel — `openclaw agent --agent builder` n'affiche plus `gateway token mismatch`.

## 12_INVARIANTS

- Aucune valeur de token committée.
- Aucune valeur de token imprimée dans les logs.
- Aucune valeur de token écrite dans les docs.
- Patch limité à la config runtime locale openclaw.
- Aucune modification index global.
- Aucun SSH sans gate.
- Le fallback embedded reste disponible.

## 16_TODO

- Créer `01_PATCH_GATE.md`.
- Passer la gate.
- Appliquer le patch config.
- Vérifier gateway health.
- Écrire `02_PATCH_EXECUTION_LOG.md`.
- Fermer avec `90_CHILD_CLOSEOUT.md`.

## 17_RESUME_POINT

Reprendre à la création de `01_PATCH_GATE.md`.
