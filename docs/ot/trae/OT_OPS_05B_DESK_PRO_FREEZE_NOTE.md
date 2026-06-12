# OT-OPS-05B — NOTE DE GEL DESK PRO

**DATE :** 2026-03-12
**STATUT :** FROZEN (GELÉ)
**PORTÉE :** Famille Desk Pro (Scripts & Modules)

## 1. CLARIFICATION DES ENTRYPOINTS
Pour mettre fin à la confusion entre les multiples scripts "desk_pro", les règles suivantes sont édictées :

*   **L'ENTRYPOINT UTILISATEUR EST `menu-ops_menu_hub`**.
    *   C'est le seul point d'entrée garanti maintenu pour l'usage quotidien.

*   **L'ENTRYPOINT ADMIN EST `scripts/admin_trading/desk_pro_cmd.sh`**.
    *   C'est lui qui détient la logique d'orchestration locale (logs, checklist, runner).

*   **LES SCRIPTS RACINE (`scripts/desk_pro_*.sh`) SONT GELÉS**.
    *   Ils sont maintenus en l'état pour compatibilité historique.
    *   **INTERDIT** d'ajouter de nouvelles fonctionnalités dans ces scripts racine.
    *   Toute nouvelle feature admin doit aller dans `scripts/admin_trading/`.

## 2. INTERDICTIONS
1.  **INTERDIT** de supprimer `scripts/desk_pro_cmd.sh` (risque de casser des habitudes ou crons).
2.  **INTERDIT** de fusionner `scripts/admin_trading/` avec `modules/desk_pro/` sans refactor majeur.
3.  **INTERDIT** d'utiliser le module `modules/desk_pro/` comme un exécutable métier (c'est une coquille).

## 3. PROCHAINE ÉTAPE
Aucune action de migration n'est requise. La coexistence est validée tant que la hiérarchie d'usage est respectée.

## RISKS

- À qualifier.
