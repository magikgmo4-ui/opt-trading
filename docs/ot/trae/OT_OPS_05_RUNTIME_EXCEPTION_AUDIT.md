# OT-OPS-05 — AUDIT DES EXCEPTIONS RUNTIME

## 1. OBJECTIF
Identifier et qualifier toutes les zones du repository où l'exécution réelle diverge de la structure modulaire théorique, au-delà du cas `student` déjà traité.

## 2. RÉSULTATS DU SCAN

### A. Cas Confirmés (Exceptions Lourdes)
1.  **Student AI** (Déjà traité)
    *   **Runtime** : `scripts/student/`
    *   **Module** : `modules/deepseek_student/` (Incomplet)
    *   **Statut** : **GELÉ**.

2.  **Reseau SSH**
    *   **Runtime** : `scripts/reseau_ssh/`
        *   Contient `reseau_ssh_cmd.sh`, `lib/common.sh`.
        *   C'est le code exécuté pour la configuration réseau.
    *   **Module** : `modules/reseau_ssh/`
        *   Structure complexe et imbriquée (`modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step1`).
        *   Semble être une archive de déploiement ou une source non aplatie.
    *   **Conclusion** : Le runtime actif est dans `scripts/reseau_ssh/`. Le module est une source théorique.

### B. Cas "Machine Runtime" (Architecture Valide mais Atypique)
Ces dossiers ne sont pas des modules mais des couches d'adaptation pour des machines spécifiques. Ils ne sont pas des "erreurs" mais doivent être distingués des modules.

1.  **Admin Trading Layer**
    *   **Runtime** : `scripts/admin_trading/`
    *   **Rôle** : Wrapper opérationnel pour la machine `admin-trading`.
    *   **Comportement** : Appelle les modules (`desk_pro_runner`) via Python ou Bash.
    *   **Statut** : **VALIDE**. C'est la couche d'intégration machine.

2.  **DB Layer Runtime**
    *   **Runtime** : `scripts/db_layer/`
    *   **Rôle** : Scripts autonomes pour la machine `msi_db_layer`.
    *   **Module associé** : `modules/ui_registry_msi` (pour l'UI), mais pas de module "db" global.
    *   **Statut** : **VALIDE**. Runtime spécifique machine.

### C. Cas Ambigus (Risque de Confusion)
1.  **Root Legacy Scripts**
    *   **Fichiers** : `scripts/desk_pro_cmd.sh`, `scripts/desk_pro_menu.sh`, `scripts/desk_pro_sanity.sh`.
    *   **Problème** : Ces scripts à la racine de `scripts/` entrent en conflit visuel avec `modules/desk_pro/scripts/`.
    *   **Usage** : Semblent être des points d'entrée historiques ou des raccourcis globaux.
    *   **Risque** : L'utilisateur peut lancer `scripts/desk_pro_cmd.sh` en pensant utiliser le module `desk_pro`, alors que le comportement peut différer.

2.  **Git Ops**
    *   **Runtime** : `scripts/git_ops/`
    *   **Module** : `modules/repo_hygiene` (connexe mais distinct).
    *   **Statut** : **ACCEPTABLE**. `git_ops` est une boîte à outils scripts, `repo_hygiene` est un module de conformité. Distinction claire par le nom.

## 3. CONCLUSION
Le repository n'est pas "tout modulaire". Il est **Hybride** :
- **Noyau Modulaire** : `modules/` (Logique métier, Moteurs).
- **Couche Runtime Machine** : `scripts/admin_trading/`, `scripts/student/`, `scripts/db_layer/` (Orchestration locale).
- **Exceptions Historiques** : `scripts/reseau_ssh/` (Divergence de structure).
- **Ambiguïtés** : `scripts/desk_pro_*.sh` (Doublons apparents).

La sécurité opérationnelle exige de reconnaître officiellement cette structure hybride plutôt que de forcer une modularisation impossible à court terme.
