# OT-SHARED-MIGRATE-01 — REPORT (MIGRATION DOUCE LOT 1 /shared)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Mission : premier rangement doux de `/shared` (surface canonique inter-machines), sans toucher aux dossiers réservés/pipeline ni aux cas ambigus.
- Actions réalisées :
  - Création des dossiers cibles : `_bundles/`, `_ops/`, `_refs/`, `_archives/`.
  - Déplacement du lot 1 : **76 fichiers `.zip` à plat** (non-dot) déplacés vers `_bundles/`.
- Exclusions explicites (ambigus/sensibles) : `.ssh.zip`, `.venv.zip` laissés à la racine.
- Gain : racine allégée **91 → 15 fichiers** (dossiers + nouveaux dossiers cibles ajoutés).

## 2. BASELINE AVANT MIGRATION
Source : `admin-trading` (chemin réel `/srv/sftp/shared_files/shared`)
- Dossiers (maxdepth 1) : 11
- Fichiers à plat (maxdepth 1) : 91
- Zips à plat : 78 (`*.zip`), dont 76 zips “non-dot” (`! -name ".*.zip"`)
- Cas ambigus présents : `.ssh.zip`, `.venv.zip`

## 3. DOSSIERS CRÉÉS
Créés à la racine (si absents) :
- `_bundles/`
- `_ops/`
- `_refs/`
- `_archives/`

Permissions appliquées :
- `chmod 2775` (setgid + group writable)
- groupe : `sftp_shared_files`

## 4. FICHIERS DÉPLACÉS

### 4.1 Vers `_bundles/` (A. DÉPLACÉ)
Déplacés : 76 fichiers (tous les `*.zip` à plat, hors `.ssh.zip` et `.venv.zip`) :
- `OPT_TRADING_CONTINUITE_PACK_V3.zip`
- `bot_vision_step2_allowlist_fix_patch_20260302.zip`
- `bot_vision_step2_analyze_local_patch.zip`
- `bot_vision_step2_cmd_no_venv_patch_20260303.zip`
- `bot_vision_step2_indent_fix.zip`
- `bot_vision_step2_patch_20260302_v5.zip`
- `bot_vision_step2_student_sanity_patch_20260303.zip`
- `bot_vision_step2_tg_stability_patch_20260302.zip`
- `bv2_patch_v2.zip`
- `bv2_scripts.zip`
- `desk_analyze_build_prompt_fix.zip`
- `desk_analyze_build_vision_prompt_fix_v3.zip`
- `desk_analyze_compact_fr_patch.zip`
- `desk_analyze_promptfix_v2.zip`
- `desk_analyze_stepB.zip`
- `desk_analyze_vision_stepC_patch (1).zip`
- `desk_analyze_vision_stepC_patch (2).zip`
- `desk_analyze_vision_stepC_patch.zip`
- `desk_bridge.zip`
- `desk_bridge_fix.zip`
- `desk_bridge_timer_pack.zip`
- `desk_capture_inputs_stepD.zip`
- `desk_retention_step0.zip`
- `desk_snapshot_ingest_stepA.zip`
- `desk_snapshot_ingest_symlink_fix_patch.zip`
- `desk_state_stepE.zip`
- `indexation_desk_bundle.zip`
- `indexation_desk_prefill_01_04_bundle.zip`
- `indexation_desk_prefill_bundle.zip`
- `install_module_cmd_fix_patch_v2.zip`
- `install_module_listpackages_sync_patch.zip`
- `install_module_listpackages_sync_patch (1).zip`
- `install_module_root_fix_patch.zip`
- `install_module_step0.zip`
- `install_module_sync_validate_patch.zip`
- `machines_registry_consume_central_bundle.zip`
- `menus_symlink_fix_patch.zip`
- `module_contextuals_shell.zip`
- `module_repo_hygiene_v1.zip`
- `module_repo_local_artifacts_v1.zip`
- `module_repo_ownership_guard_v1.zip`
- `module_ssh_keys_inventory_v3_bundle.zip`
- `modules_registry_consume_central_bundle.zip`
- `operator_surface_standardization_bundle.zip`
- `ops_menu_hub.zip`
- `ops_super_menu_none_filters_patch.zip`
- `ops_super_menu_none_filters_patch_v2.zip`
- `ops_super_menu_numbered_patch.zip`
- `ops_super_menu_step0.zip`
- `ops_wrappers_shortcuts_fix_patch.zip`
- `ops_wrappers_step0.zip`
- `perm_fix_student_bundle.zip`
- `registry_install_shortcuts_bundle.zip`
- `registry_meta_index_bundle.zip`
- `registry_router_landing_menu_bundle.zip`
- `registry_source_of_truth_bundle.zip`
- `shared_sshfs_permanent_bundle.zip`
- `shared_sshfs_permanent_install_bundle_v1.zip`
- `shared_sshfs_permanent_step1_patch_v1.zip`
- `shared_sshfs_permanent_step1b_patch_v1.zip`
- `ssh_keys_inventory_v2_bundle.zip`
- `toolbox_msi_bundle.zip`
- `ui_indexation_bundle.zip`
- `ui_indexation_prefill_bundle.zip`
- `ui_registry_msi_bundle.zip`
- `ui_registry_msi_consume_central_bundle.zip`
- `ui_screenshots_bundle.zip`
- `ui_screenshots_prefill_bundle.zip`
- `ui_screenshots_registry_bundle.zip`
- `ui_screenshots_registry_bundle (1).zip`
- `vision_bot_patch_20260302.zip`
- `vision_bot_service_patch_20260302.zip`
- `vision_bot_symlink_fix_patch_20260302.zip`
- `winscp_transfer_bundle.zip`
- `wrappers_registry_reader_bundle.zip`
- `wrappers_registry_source_of_truth_bundle.zip`

### 4.2 Vers `_ops/` (A. DÉPLACÉ)
- Aucun fichier déplacé dans ce lot 1 (prudence : scripts `.sh` laissés à la racine).

### 4.3 Vers `_refs/` (A. DÉPLACÉ)
- Aucun fichier déplacé dans ce lot 1 (prudence : `README.txt` et `audit_opt_trading_branches.md` laissés à la racine).

### 4.4 Vers `_archives/` (A. DÉPLACÉ)
- Aucun fichier déplacé dans ce lot 1.

## 5. FICHIERS LAISSÉS EN PLACE

### B. LAISSÉ EN PLACE (RÉSERVÉ)
Dossiers réservés inchangés :
- `inbox/`, `outbox/`, `modules/`, `_logs/`, `vision_inbox/`, `vision_outbox/`, `vision_processed/`, `desk_pro/`, `documents/`, `windows/`, `_git_archives/`

### C. LAISSÉ EN PLACE (AMBIGU)
- `.ssh.zip`
- `.venv.zip`

### D. LAISSÉ EN PLACE (HORS LOT 1)
Fichiers restés à la racine par prudence :
- `boot_test.txt`, `README.txt`, `audit_opt_trading_branches.md`
- scripts `.sh` : `bridge_vision_to_desk_inbox.sh`, `install_desk_bridge_timer.sh`, `prep_commit_admin_trading.sh`, `bv2_*.sh`, `check_*.sh`
- `module_repo_modules_v1.sha256`

## 6. CAS AMBIGUS EXCLUS
Exclus explicitement du lot 1 (aucun déplacement) :
- `.ssh.zip` : potentiellement sensible (risque secrets/clé).
- `.venv.zip` : volumineux, non canonique ; à requalifier.

## 7. SNAPSHOT APRÈS MIGRATION
Source : `admin-trading` (chemin réel `/srv/sftp/shared_files/shared`)
- Dossiers (maxdepth 1) : 15 (11 existants + 4 nouveaux)
- Fichiers à plat (maxdepth 1) : 15
- `_bundles/` : 76 fichiers
Contrôle cohérence clients :
- `db-layer` et `student` voient `/shared/_bundles` avec 76 fichiers.

## 8. FICHIERS MODIFIÉS (REPO)
- `OT_SHARED_MIGRATE_01_REPORT.md`
- `OT_SHARED_MIGRATE_01_CLOSING.txt`

## 9. COMMANDES EXÉCUTÉES
- Baseline : `find ... -maxdepth 1`, `wc -l`, `du -sh`, inventaire `*.zip`
- Création dirs : `mkdir -p _bundles _ops _refs _archives`, `chmod 2775`, `chgrp sftp_shared_files`
- Migration : loop `mv -n -- <file>.zip _bundles/` (excluant `.ssh.zip`, `.venv.zip`)
- Validation : recomptage + `find /shared/_bundles -type f | wc -l` sur `admin-trading`, `db-layer`, `student`

## 10. VERDICT FINAL
**PASS** : arbo cible minimale créée et premier lot reclassable déplacé sans toucher aux réservés ni aux ambigus.

## 11. POINT DE REPRISE SUIVANT
- Lot 2 (optionnel, prudent) :
  - déplacer des scripts `.sh` clairement opératoires vers `_ops/`
  - déplacer les docs “référence” vers `_refs/` (si aucun flux ne les consomme)
  - traiter séparément `.ssh.zip` et `.venv.zip` (décision explicite + procédure contrôlée)

