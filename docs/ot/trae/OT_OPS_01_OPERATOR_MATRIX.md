# OT-OPS-01 — MATRICE OPÉRATEUR DESK PRO (RÉVISÉE V2)

## 1. LÉGENDE DES STATUTS
- **ÉTABLI** : Module prouvé, actif, registré.
- **À CONFIRMER** : Module présent mais rôle exact ou périmètre à valider.
- **PARTIEL** : Module actif manquant de wrapper ou d'entrée registry.
- **LEGACY CANDIDATE** : Module obsolète ou cassé, candidat à suppression/archivage.
- **BROKEN** : Module dont le code est prouvé incompatible avec l'env actuel.

## 2. MATRICE CANONIQUE (ÉTAT RÉEL AUDITÉ)

| Module | Rôle / Domaine | Machine Cible | Mode | Scripts Présents | Wrapper Global | Registry | Statut | Action Requise |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **validated_prompt_factory** | Outil Dev (Prompt Gen) | Any | On-Demand | cmd, menu, sanity | OUI (récent) | NON | **PARTIEL** | Ajouter au Registry |
| **ops_menu_hub** | Point d'entrée MSI | msi_db_layer | On-Demand | cmd, menu, sanity | OUI (menu-ops_menu_hub) | OUI | **ÉTABLI** | RAS |
| **ops_super_menu** | Point d'entrée Admin | admin-trading | On-Demand | cmd, menu, sanity | NON | NON | **À CONFIRMER** | Clarifier vs ops_menu_hub |
| **desk_pro_runner** | Façade Opérateur Trading | admin-trading | On-Demand | cmd, menu, sanity | OUI (cmd-desk_pro_runner) | OUI | **ÉTABLI** | RAS |
| **desk_pro_orchestrator** | Moteur Pipeline | admin-trading | Library | cmd, menu, sanity | NON | NON | **ÉTABLI (INTERNE)** | Confirmer non-exposition |
| **desk_pro_dashboard** | Visu Trading | msi_db_layer | On-Demand | cmd, menu, sanity | OUI (cmd-desk_pro_dashboard) | OUI | **ÉTABLI** | RAS |
| **desk_state** | Monitoring Rapide | msi_db_layer | On-Demand | cmd, menu, sanity | NON | OUI | **PARTIEL** | Créer wrapper global |
| **desk_capture_inputs** | Saisie Signaux | admin-trading | On-Demand | cmd, menu, sanity | NON | OUI | **PARTIEL** | Créer wrapper global |
| **desk_analyze** | Analyse Unitaire | admin-trading | On-Demand | cmd, menu, sanity | NON | OUI | **PARTIEL** | Créer wrapper global |
| **reseau_ssh** | Infra / Install | admin-trading | One-Shot | cmd, menu, sanity | NON | NON | **À CONFIRMER** | Structure imbriquée anormale |
| **shared_sshfs_permanent** | Service Infra | admin-trading | Service | cmd, menu, sanity | NON | NON | **PARTIEL** | Ajouter au Registry |
| **vision_bot** | Service Capture | admin-trading | Service | cmd, menu, sanity | NON | OUI | **PARTIEL** | Créer wrapper global |
| **workflow_post_change_v2** | Outil CI/CD | Any | Hook | cmd, menu, sanity | NON | NON | **BROKEN** | Utilise sudo (incompatible env) |
| **workflow_post_change_v2_fix3** | Outil CI/CD | Any | Hook | cmd, menu, sanity | NON | NON | **ACTIF CANDIDATE** | Version correcte (no-sudo) |
| **ui_registry_msi** | Outil Registry UI | msi_db_layer | On-Demand | cmd, menu, sanity | OUI | OUI | **ÉTABLI** | RAS |
| **trae_module_validator** | Outil CI/CD | Any | On-Demand | cmd, menu, sanity | NON | NON | **PARTIEL** | Ajouter au Registry |

## 3. ANALYSE DES FAMILLES

### A. FAMILLE DESK PRO
La séparation est claire et documentée (voir Note Rôles).

### B. FAMILLE RESEAU SSH
Structure imbriquée (`modules/reseau_ssh/modules/...`) confirmée.
**Statut** : Fonctionnel mais structurellement "sale". Pas de refactor immédiat requis, mais surveillance.

### C. FAMILLE WORKFLOW (PREUVE DESTRUCTIVE)
Comparaison effectuée entre `v2` et `fix3`.
- `v2` tente un `sudo` sur la machine student -> **FAIL**.
- `fix3` retire le `sudo` -> **PASS**.
**Conclusion** : `fix3` est la version active réelle. `v2` est une version obsolète/cassée.
**Action Sûre** : Promouvoir `fix3` en écrasant `v2`, puis supprimer `fix3`.

### D. FAMILLE DEEPSEEK
`deepseek_hub` semble centraliser les appels.
**Statut** : À confirmer par audit dédié ultérieur.

## 4. ÉCARTS CRITIQUES (BLOCKERS)
1. **Absence de validated_prompt_factory du registry**.
2. **État cassé de workflow_post_change_v2** (canonique).
3. **Manque de Wrappers** pour modules actifs (`desk_analyze`, etc.).

## 5. RECOMMANDATIONS (POUR PASS 4)
1. **Registry Update** : Ajouter `validated_prompt_factory`, `shared_sshfs_permanent`, `trae_module_validator`.
2. **Wrapper Install** : Générer les wrappers manquants.
3. **Workflow Fix** : Appliquer le patch `fix3` sur `v2` (Promotion) et supprimer le dossier temporaire.
