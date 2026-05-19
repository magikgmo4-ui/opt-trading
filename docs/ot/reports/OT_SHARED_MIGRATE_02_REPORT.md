# OT-SHARED-MIGRATE-02 — REPORT (MIGRATION DOUCE LOT 2 /shared)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Mission : reclasser prudemment les scripts opératoires et références restés à la racine de `/shared` vers `_ops/` et `_refs/`.
- Actions réalisées (admin-trading, surface canonique) :
  - Déplacement de **8 scripts** vers `/shared/_ops/`.
  - Déplacement de **2 fichiers de référence** vers `/shared/_refs/`.
- Exclusions respectées : `.ssh.zip` et `.venv.zip` laissés à la racine.
- Gain : racine `/shared` allégée **15 → 5 fichiers** (tout en conservant `README.txt`, `boot_test.txt`, et un script glue).

## 2. BASELINE AVANT MIGRATION
Source : `admin-trading` (chemin réel `/srv/sftp/shared_files/shared`)

Fichiers présents à la racine (après OT-SHARED-MIGRATE-01) :
- Références : `audit_opt_trading_branches.md`, `README.txt`, `module_repo_modules_v1.sha256`
- Scripts : `bridge_vision_to_desk_inbox.sh`, `bv2_*`, `check_*`, `install_desk_bridge_timer.sh`, `prep_commit_admin_trading.sh`
- Sentinelles/ambigus : `boot_test.txt`, `.ssh.zip`, `.venv.zip`

Comptes (racine) :
- `*.sh` : 9
- `*.md` : 1
- `*.txt` : 2
- `*.sha256` : 1
- `*.zip` : 2 (dotfiles) — exclus

## 3. SÉLECTION DU LOT 2 (LOGIQUE)

### A. Déplacer vers `_ops/`
Critère : scripts `.sh` manifestement opératoires/diagnostic/install (pas de preuve d’usage systemd/cron via chemin `/shared/<script>`).
- `bv2_inspect_analyze.sh`
- `bv2_patch_analyze_local.sh`
- `bv2_patch_analyze_local_v2.sh`
- `bv2_rescue_restore.sh`
- `check_menus_all.sh`
- `check_shortcuts_targets.sh`
- `install_desk_bridge_timer.sh`
- `prep_commit_admin_trading.sh`

### B. Déplacer vers `_refs/`
Critère : références/documentation non-consommées par pipeline.
- `audit_opt_trading_branches.md`
- `module_repo_modules_v1.sha256`

### E. Laisser en place (hors lot 2 / prudence)
- `bridge_vision_to_desk_inbox.sh` : script glue ; laissé à la racine pour ne pas déplacer un élément potentiellement “pipeline-like” dans les usages humains.
- `README.txt` : doc d’entrée opératoire ; conservée à la racine.
- `boot_test.txt` : sentinelle runtime ; conservée à la racine.

### D. Exclusions (ambigus/sensibles)
- `.ssh.zip`
- `.venv.zip`

## 4. MIGRATION DOUCE LOT 2 (RÉALISÉE)
- `mv -n` vers `_ops/` pour 8 scripts.
- `mv -n` vers `_refs/` pour 2 références.
- Aucun overwrite, aucun renommage.

## 5. VALIDATION APRÈS MIGRATION

### 5.1 Snapshot admin-trading
Racine `/shared` contient désormais :
- `boot_test.txt`
- `README.txt`
- `bridge_vision_to_desk_inbox.sh`
- `.ssh.zip`
- `.venv.zip`

Comptes :
- racine : 5 fichiers
- `_ops/` : 8 fichiers
- `_refs/` : 2 fichiers

### 5.2 Contrôle côté clients montés
Sur `db-layer` et `student` :
- racine `/shared` : mêmes 5 fichiers
- `_ops_files=8`, `_refs_files=2`

## 6. FICHIERS MODIFIÉS (REPO)
- `OT_SHARED_MIGRATE_02_REPORT.md`
- `OT_SHARED_MIGRATE_02_CLOSING.txt`

## 7. COMMANDES EXÉCUTÉES
- Baseline : `find ... -maxdepth 1`, comptage par type
- Safety check (non destructif) : recherche de références `/shared/<script>` dans `/etc/systemd/system`, `/etc/cron*`, `/opt/trading`, `/home/ghost`
- Migration : `mv -n <file> _ops/` et `mv -n <file> _refs/`
- Validation :
  - `find /shared -maxdepth 1 -type f ...`
  - comptage `_ops/_refs` sur `admin-trading`, `db-layer`, `student`

## 8. VERDICT FINAL
**PASS** : lot 2 exécuté, racine `/shared` très lisible, réservés intacts, ambigus exclus.

## 9. POINT DE REPRISE SUIVANT (LOT 3 POSSIBLE)
- Option A (très prudent) : s’arrêter ici (racine déjà minimale).
- Option B : déplacer `bridge_vision_to_desk_inbox.sh` vers `_ops/` uniquement après décision opérateur explicite.
- Option C : traiter séparément `.ssh.zip` et `.venv.zip` (qualification + décision).

