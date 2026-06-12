# OT-OPS-05B — AUDIT DES ENTRYPOINTS DESK PRO

## 1. OBJECTIF
Clarifier la jungle des entrypoints de la famille "Desk Pro" pour établir une vérité opérationnelle indiscutable.

## 2. INVENTAIRE DES ENTRYPOINTS

### A. Le "Desk Pro Root" (Scripts à la racine)
*   **Fichiers** : `scripts/desk_pro_cmd.sh`, `scripts/desk_pro_menu.sh`, `scripts/desk_pro_sanity.sh`
*   **Rôle Réel** : Interface historique / alias rapide pour lancer l'API ou checker la santé globale.
*   **État** : **AMBIGU**. Il prétend être "Desk Pro" mais ne fait que des appels génériques (`sanity`, `ui`, `logs`).
*   **Risque** : Confusion avec l'orchestrateur réel.

### B. Le "Admin Trading Layer" (Machine Specific)
*   **Fichiers** : `scripts/admin_trading/desk_pro_cmd.sh`
*   **Rôle Réel** : **WRAPPER D'ORCHESTRATION**. C'est lui qui pilote le module `desk_pro_runner`.
*   **Preuve** : Appelle `python3 -m modules.desk_pro_runner.app.desk_pro_runner`.
*   **Usage** : Contient des commandes vitales (`checklist`, `run-logged`, `copy-latest-to-shared`).
*   **Statut** : **CRITIQUE**. C'est le véritable outil de l'opérateur sur la machine admin.

### C. Le Module "Desk Pro" (Théorique)
*   **Fichiers** : `modules/desk_pro/scripts/cmd.sh`
*   **Rôle Réel** : Wrapper générique de module (info, readme, ls).
*   **Contenu** : Vide de logique métier.
*   **Statut** : **COQUILLE VIDE**. Ce module sert de conteneur, pas d'exécutable.

### D. Les Wrappers Globaux (Registry)
*   `cmd-desk_pro_runner` -> Pointe vers `modules/desk_pro_runner`. (Backend).
*   `cmd-desk_pro_dashboard` -> Pointe vers `modules/desk_pro_dashboard`. (Frontend).
*   `menu-ops_menu_hub` -> Point d'entrée global recommandé.

## 3. ANALYSE DE LA CONFUSION
L'ambiguïté vient du fait que :
1.  `scripts/desk_pro_cmd.sh` (Root) s'appelle "Desk Pro" mais ne gère que des utilitaires génériques.
2.  `scripts/admin_trading/desk_pro_cmd.sh` (Admin) s'appelle aussi "Desk Pro" (dans le nom du fichier) mais gère l'orchestration réelle.
3.  L'utilisateur ne sait pas lequel lancer s'il tape juste "desk pro" dans sa tête.

## 4. CONCLUSION
*   **Entrypoint Opérateur Recommandé** : `menu-ops_menu_hub` (qui centralise tout).
*   **Outil Admin Réel** : `scripts/admin_trading/desk_pro_cmd.sh`.
*   **Legacy à Geler** : `scripts/desk_pro_*.sh` (ne pas supprimer, mais ne pas recommander).
*   **Module à Ignorer** : `modules/desk_pro/` (Coquille structurelle).

## RISKS

- À qualifier.
