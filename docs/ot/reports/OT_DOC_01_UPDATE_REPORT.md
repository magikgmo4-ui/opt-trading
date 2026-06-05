# OT-DOC-01 — RAPPORT DE MISE À JOUR DOCUMENTAIRE

## 1. OBJECTIF
Refléter l'état post-patch du workflow `workflow_post_change_v2` dans la documentation officielle.

## 2. ACTIONS RÉALISÉES
- **Création** : `docs/status/workflow_post_change_canonique.md` (Source de vérité).
- **Mise à jour** : `docs/indexation_desk/01_inventory_modules.md` (Marquage DEPRECATED/PATCHED).
- **Vérification** : Cohérence avec le registry et le runtime `admin-trading`.

## 3. POINTS CANONIQUES ÉTABLIS
- **v2** : Module actif et corrigé (no-sudo).
- **fix3** : Correctif fusionné, module déprécié mais conservé pour archive.
- **fix1/fix2** : Obsolètes.

## 4. NUANCES
- Les dossiers `fix*` existent toujours physiquement sur le disque.
- Le wrapper `cmd-workflow_post_change_v2` est un utilitaire générique, pas l'exécutable métier.

## RISKS

- À qualifier.
