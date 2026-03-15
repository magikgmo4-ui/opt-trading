# OT-OPS-05 — MATRICE DES EXCEPTIONS RUNTIME

Cette matrice classifie les zones où le modèle "1 Module = 1 Runtime" ne s'applique pas.

## 1. EXCEPTIONS STRUCTURELLES (DIVERGENCE)
Zones où le code actif n'est pas dans le module attendu.

| Zone | Machine | Runtime Actif (Vérité) | Module Théorique | Statut | Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Student AI** | student | `scripts/student/` | `modules/deepseek_student/` | **GELÉ** | Ne pas toucher (Voir OT-OPS-04B) |
| **Reseau SSH** | admin/all | `scripts/reseau_ssh/` | `modules/reseau_ssh/` | **EXCEPTION** | Documenter `scripts/` comme source active |

## 2. COUCHES RUNTIME MACHINE (INTEGRATION)
Zones valides servant d'adaptateur entre la machine et les modules.

| Zone | Machine | Point d'Entrée | Modules Appelées | Statut | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Admin Layer** | admin-trading | `scripts/admin_trading/` | `desk_pro_runner`, `desk_pro` | **VALIDE** | Orchestration spécifique admin |
| **DB Layer** | msi_db_layer | `scripts/db_layer/` | `ui_registry_msi` | **VALIDE** | Scripts autonomes + UI Module |
| **Git Ops** | any | `scripts/git_ops/` | `repo_hygiene` (partiel) | **VALIDE** | Outillage transversal |

## 3. ZONES AMBIGUËS (RISQUE)
Zones où plusieurs points d'entrée concurrents existent.

| Zone | Fichiers Scripts | Module Concurrent | Risque | Recommandation |
| :--- | :--- | :--- | :--- | :--- |
| **Desk Pro Root** | `scripts/desk_pro_*.sh` | `modules/desk_pro/` | Confusion d'usage | Préférer les Wrappers (`cmd-desk_pro`) ou le Hub |

## 4. DÉFINITION DES PRIORITÉS
1.  **Respecter le Runtime Machine** : Ne jamais supprimer `scripts/<machine>/`.
2.  **Méfiance sur les Modules Complexes** : Pour `reseau_ssh` et `student`, le module est une archive ou un brouillon, pas l'exécutable.
3.  **Usage des Wrappers** : Toujours privilégier les commandes `/usr/local/bin/` (`menu-ops_menu_hub`, `cmd-desk_pro`) qui sont censées pointer vers la bonne cible (validée par le registry).
