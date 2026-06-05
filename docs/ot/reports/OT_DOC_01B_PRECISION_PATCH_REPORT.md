# OT-DOC-01B — RAPPORT DE PRÉCISION DOCUMENTAIRE

## 1. OBJECTIF
Affiner la documentation pour lever toute ambiguïté sur le statut des variantes `fix*`.

## 2. CORRECTIONS APPORTÉES
- **Fichier** : `docs/status/workflow_post_change_canonique.md`
- **Correction** : Distinction explicite entre `fix3` (Merged) et `fix1/fix2` (Obsolete).
- **Raison** : Éviter de laisser croire que `fix1` et `fix2` ont contribué au code final.

## 3. ÉTAT FINAL VALIDÉ
- **v2** : Canonique, Patché (Source: fix3).
- **fix3** : Déprécié, Merged (Code source du patch).
- **fix1/fix2** : Déprécié, Obsolete (Code inutile).
- **Runtime** : Aligné sur v2.

## RISKS

- À qualifier.
