# OT-PROMPT-01 — RAPPORT DE RAFRAÎCHISSEMENT MASTER PACK

## 1. OBJECTIF
Mettre à jour le "cerveau documentaire" pour qu'il intègre les leçons des missions récentes (Workflow, Runtime, Wrappers).

## 2. ACTIONS RÉALISÉES
- **Création** : `docs/master_pack/00_current_state_and_standards.md` (Nouvelle référence absolue).
- **Mise à jour** : `docs/desk_pro_trae_master_prompt_pack.md` (Introduction de la section 1.1 et correction des noms de scripts).

## 3. VÉRITÉS INTÉGRÉES
- **Workflow** : `v2` est canonique (no-sudo patché). `fix3` est merged.
- **Maintenance** : Ne pas supprimer physiquement sans preuve croisée.
- **Standards** : Préférence pour `scripts/cmd.sh` et `registry/wrappers_registry.yaml`.

## 4. IMPACT FUTUR
Tout nouveau prompt généré suivra ces standards, évitant la réintroduction de dette technique (comme les vieux noms `<module>_cmd.sh` ou les `sudo` inutiles).

## RISKS

- À qualifier.
