# OT-OPS-05B — MATRICE DES ENTRYPOINTS DESK PRO

Cette matrice définit le statut officiel de chaque point d'entrée de la famille Desk Pro.

## 1. ENTRYPOINTS CANONIQUES (RECOMMANDÉS)

| Nom | Chemin / Commande | Rôle | Machine | Statut |
| :--- | :--- | :--- | :--- | :--- |
| **OPS MENU HUB** | `menu-ops_menu_hub` | **Menu Principal**. Point d'entrée unique pour l'opérateur. | Admin | **CANONIQUE** |
| **RUNNER CLI** | `cmd-desk_pro_runner` | Interface CLI directe vers l'orchestrateur. | Admin | **BACKEND** |
| **DASHBOARD CLI** | `cmd-desk_pro_dashboard` | Interface CLI directe vers le dashboard. | Admin | **FRONTEND** |

## 2. COUCHE D'INTÉGRATION (MACHINE SPECIFIC)

| Nom | Chemin | Rôle | Statut | Note |
| :--- | :--- | :--- | :--- | :--- |
| **Admin Wrapper** | `scripts/admin_trading/desk_pro_cmd.sh` | **Outil Admin**. Pilote le runner + logs + checklist. | **ACTIF** | C'est le "couteau suisse" de l'admin. |

## 3. ZONES DE COMPATIBILITÉ (NON RECOMMANDÉES)

| Nom | Chemin | Problème | Statut | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Root Script** | `scripts/desk_pro_cmd.sh` | Nom ambigu. Fonctionnalités limitées (sanity/ui). | **LEGACY** | Garder pour compatibilité, ne pas promouvoir. |
| **Root Menu** | `scripts/desk_pro_menu.sh` | Doublon partiel du Hub. | **LEGACY** | Garder, mais le Hub est prioritaire. |

## 4. ZONES STRUCTURELLES (NE PAS EXÉCUTER)

| Nom | Chemin | Rôle | Statut | Note |
| :--- | :--- | :--- | :--- | :--- |
| **Module Shell** | `modules/desk_pro/scripts/cmd.sh` | Wrapper standard vide. | **STRUCTURE** | Ne fait rien de métier. |

## 5. RÈGLE D'USAGE
1. **Opérateur** : Utiliser `menu-ops_menu_hub`.
2. **Admin/Debug** : Utiliser `scripts/admin_trading/desk_pro_cmd.sh` ou `cmd-desk_pro_runner`.
3. **Scripts Root** : À éviter pour les nouvelles procédures.
