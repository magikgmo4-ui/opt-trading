# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Écrire la documentation opérationnelle validée pour l'usage contrôlé du builder OpenClaw, à partir du plan approuvé dans le child précédent.

## 2_INITIAL_PROJECT_DOC

Ce document initialise le child GO d'écriture documentaire builder. Il reste la référence figée du cadrage initial du chantier.

## 3_INITIAL_NEED

Le plan documentaire builder a été validé avec quatre documents approuvés : guide opérateur, vue architecture, workflow contrôlé, garde-fous sécurité. Il faut maintenant produire ces documents sans modifier le runtime, sans corriger le gateway token, sans toucher aux index globaux, et sans créer d'autorisation opérationnelle implicite.

## 4_MASTER_PROJECT_PLAN

1. Produire `BUILDER_OPERATIONAL_GUIDE.md`.
2. Produire `BUILDER_ARCHITECTURE_VIEW.md`.
3. Produire `BUILDER_CONTROLLED_WORKFLOW.md`.
4. Produire `BUILDER_SECURITY_GUARDRAILS.md`.
5. Vérifier cohérence et non-duplication.
6. Fermer le child avec `90_CHILD_CLOSEOUT.md`.

## 6_FINAL_TARGET

Obtenir un pack documentaire builder complet, borné et mergeable.

## 12_INVARIANTS

- Aucun SSH.
- Aucun patch runtime.
- Aucun fix gateway token.
- Aucune modification index global.
- Aucun push avant closeout.
- Documentation uniquement.
- Les documents ne créent pas de nouvelle autorité runtime.
- Le warning `gateway token mismatch` reste documenté comme non résolu.

## 16_TODO

- Écrire les 4 documents approuvés.
- Vérifier les mentions de scope.
- Committer le pack documentaire.
- Fermer le child.

## 17_RESUME_POINT

Reprendre à l'écriture de `BUILDER_OPERATIONAL_GUIDE.md`.

## RISKS

- À qualifier.
