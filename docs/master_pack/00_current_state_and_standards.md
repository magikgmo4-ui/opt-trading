# DESK PRO — CURRENT STATE & STANDARDS (2026-03-12)

Ce document définit l'état canonique du projet pour toute nouvelle génération de module ou maintenance.
Il supplante les anciennes conventions si elles diffèrent.

## 1. WORKFLOW POST-CHANGE
- **Module Canonique** : `modules/workflow_post_change_v2`
- **Statut** : ACTIVE / PATCHED (no-sudo).
- **Entrée Métier** : `scripts/post_change.sh` (appelé directement).
- **Wrapper CLI** : `cmd-workflow_post_change_v2` (Générique: info/readme/ls).
- **Dépréciés** : `fix3` (Merged), `fix1/fix2` (Obsolete/Conservés). Ne plus utiliser.

## 2. CONVENTIONS WRAPPERS
Tout nouveau module standard DOIT exposer :
- `menu-<module>` -> Pointe vers `modules/<module>/scripts/menu.sh`
- `cmd-<module>` -> Pointe vers `modules/<module>/scripts/cmd.sh`
- `sanity-<module>` -> Pointe vers `modules/<module>/scripts/sanity_check.sh`

Exception admise :
- certaines surfaces canoniques operateur top-level peuvent etre enregistrees comme `entrypoint`
- elles ne sont utilisees que lorsqu'elles ne se reduisent pas proprement a `cmd/menu/sanity`
- cas actuel : `desk-pro`

**Regle d'Or** : Les scripts internes doivent utiliser `readlink -f` pour supporter l'invocation via symlink `/usr/local/bin`.

## 3. RUNTIME ADMIN-TRADING
- Le runtime est la source de vérité finale.
- `workflow_post_change_v2` y a été patché physiquement (OT-OPS-02B).
- `validated_prompt_factory` et `trae_module_validator` y sont déployés et validés.

## 4. REGISTRY
- Tout module doit être déclaré dans `registry/modules_registry.yaml`.
- Tout wrapper doit être déclaré dans `registry/wrappers_registry.yaml`.
- Statuts valides : `active`, `deprecated_merged`, `broken`, `active_candidate`.

## 5. DÉVELOPPEMENT
- **Ne pas supprimer** physiquement de dossiers sans validation croisée (Repo + Runtime).
- **Ne pas utiliser sudo** dans les scripts destinés à `student` ou `admin-trading` (sauf installateur système explicite).

## 6. EXCEPTIONS RUNTIME (GELÉES)
Certaines zones du repo divergent de la structure modulaire standard pour des raisons historiques ou de production active.

### A. Student Runtime (GELÉ)
- **Runtime Actif** : `scripts/student/` (Contient IA/Reporting).
- **Module Incomplet** : `modules/deepseek_student/` (Ne pas utiliser).
- **Note** : Voir `docs/ot/reports/OT_OPS_04B_FREEZE_REPORT.md`.

### B. Reseau SSH (EXCEPTION)
- **Runtime Actif** : `scripts/reseau_ssh/` (Contient `reseau_ssh_cmd.sh`).
- **Module Source** : `modules/reseau_ssh/` (Archive/Source théorique).
- **Action** : Utiliser `scripts/reseau_ssh/` pour les opérations réseau.

### C. Runtime Layers (VALIDE)
Les dossiers suivants sont des couches d'intégration machine valides, pas des modules :
- `scripts/admin_trading/` : Orchestration spécifique Admin.
- `scripts/db_layer/` : Scripts autonomes DB Layer.
- `scripts/git_ops/` : Outillage Git transversal.

## 7. ENTRYPOINTS CANONIQUES (DESK PRO)
Pour clarifier l'usage des multiples scripts "desk_pro" :
- **Opérateur** : `menu-ops_menu_hub` (Point d'entrée unique).
- **Admin** : `scripts/admin_trading/desk_pro_cmd.sh` (Couteau suisse orchestration).
- **Legacy** : `scripts/desk_pro_*.sh` (Compatibilité, ne plus développer).
- **Module** : `modules/desk_pro/` (Librairie Core API/Models - Ne pas exécuter directement).

## 8. STANDARD TRANSFERT INTER-MACHINES (/shared)
- **Surface canonique** : `/shared`
- **Source (serveur)** : `admin-trading` expose `/srv/sftp/shared_files/shared` (alias local `/shared`).
- **Clients Linux** : `db-layer` et `student` montent `/shared` via `shared_sshfs_permanent` (systemd `shared-sshfs.service`).
- **Windows/GUI (cursor-ai)** : accès via WinSCP/SFTP vers `/shared` (chroot SFTP) sur `admin-trading`.
- **Chemin local Windows canonique (établi sur poste)** : `C:\\Users\\ghost\\Downloads\\SHARED\\`.
- **Doctrine (V1)** :
  - Tout fichier utile au projet va par défaut dans `shared` (dépôt/récupération/transfert/livraison).
  - La racine doit rester légère ; utiliser les sous-dossiers canoniques.
  - Ne pas déplacer automatiquement les cas ambigus/sensibles.
- **Sous-dossiers canoniques** : `_bundles/` (zips), `_ops/` (scripts), `_refs/` (références), `_archives/` (anciens/doublons).
- **UX minimale (Linux)** : `cmd-shared ls|get|put|cat|status|path` (module `shared`).
