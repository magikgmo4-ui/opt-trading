# OT-OPS-01 — AUDIT DE SURFACE OPÉRATEUR (RÉVISÉ V2)

## 1. CONTEXTE
Audit de gisement réel des modules Desk Pro avant expansion. Focus sur la distinction entre ce qui est prouvé (ÉTABLI) et ce qui est supposé (À CONFIRMER).

## 2. INVENTAIRE RÉEL (SYNTHÈSE QUALITATIVE)
- **Couverture Registry** : ~50% des modules dossiers sont absents du registry.
- **État de Santé** : Globalement sain, mais présence de dettes techniques critiques (Workflow, Reseau SSH).
- **Modules Critiques Non-Registrés** : 3 modules essentiels (`prompt_factory`, `sshfs`, `validator`) fonctionnent "sous le radar".

## 3. ÉCARTS MAJEURS (PROUVÉS)

### A. WORKFLOW POST CHANGE (PREUVE DESTRUCTIVE)
L'analyse comparative des scripts `post_change.sh` entre `v2` et `v2_fix3` montre une divergence critique :
- `v2` utilise `sudo` pour copier chez `student` (incompatible avec la configuration actuelle).
- `fix3` retire le `sudo`.
**Conclusion** : Le module canonique `v2` est CASSÉ (BROKEN). Le module temporaire `fix3` est ACTIF.
**Action Sûre** : Remplacer le contenu de `v2` par `fix3`.

### B. SHARED SSHFS PERMANENT (AUDIT COMPLET)
Le module dispose de tous les attributs "Registry-Ready" :
- Scripts `cmd/menu/sanity`.
- Template Systemd.
- Documentation d'installation.
**Conclusion** : Il peut être intégré au Registry sans risque.

### C. MANQUE DE WRAPPERS
Les modules `desk_analyze`, `desk_capture_inputs`, `vision_bot` sont marqués "ACTIF" dans le registry mais leurs wrappers globaux (`/usr/local/bin/...`) n'ont pas été vérifiés présents sur `admin-trading`.
**Risque** : L'opérateur ne peut pas les lancer facilement.

## 4. MATRICE DE DÉCISION RÉVISÉE (EXTRAIT)
*Voir OT_OPS_01_OPERATOR_MATRIX.md pour le détail.*

| Module | Statut Révisé | Action Sûre |
| :--- | :--- | :--- |
| validated_prompt_factory | **PARTIEL** | Ajouter Registry + Wrapper |
| workflow_post_change_v2 | **BROKEN** | Patcher avec fix3 |
| shared_sshfs_permanent | **PARTIEL** | Ajouter Registry |
| reseau_ssh | **À CONFIRMER** | Ne pas toucher (structure complexe) |

## 5. RECOMMANDATIONS (PLAN D'ACTION SÛR)

### ÉTAPE 1 : RÉPARATION (OT-OPS-02)
1. **Workflow Fix** : Copier `v2_fix3/scripts/*` vers `v2/scripts/`. Supprimer `v2_fix*`.
2. **Archivage** : Déplacer les modules clairement identifiés comme LEGACY (`perm_fix_student` ?) vers `_archive/`.

### ÉTAPE 2 : MISE À JOUR REGISTRY (OT-REG-02)
1. Ajouter `validated_prompt_factory`.
2. Ajouter `shared_sshfs_permanent`.
3. Ajouter `trae_module_validator`.

### ÉTAPE 3 : DÉPLOIEMENT (OT-WRAP-01)
1. Exécuter `install_shortcuts.sh` pour tous les modules actifs du registry.

## 6. ZONES D'OMBRE (INTERDICTIONS)
- Interdit de modifier la structure de `reseau_ssh` sans audit dédié.
- Interdit de supprimer `deepseek_*` sans audit dédié.
- Interdit de toucher à `desk_pro_orchestrator` (cœur système).

## RISKS

- À qualifier.
