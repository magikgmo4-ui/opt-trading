# OT-SVC-01 — CANONICAL RUNTIME MAP (REVISITED)

Ce document définit la stratégie d'exécution canonique pour chaque module du système.
Il sert de référence pour le déploiement et le monitoring.

## 1. DÉFINITIONS CANONIQUES
- **ON-DEMAND** : Exécuté manuellement par un opérateur ou un script parent. Pas de persistance.
- **SERVICE** : Processus long-running géré par Systemd (Restart=always).
- **TIMER** : Tâche périodique gérée par Systemd Timer (Cron-like).
- **MOUNT** : Unité Systemd de montage (Filesystem).

## 2. CARTE D'EXÉCUTION (RUNTIME MAP)

### A. OPERATOR TOOLS (ON-DEMAND)
Ces modules sont des outils CLI/Menu invoqués à la demande. Ils ne tournent pas en fond.

| Module | Mode | Entrypoint | Cible | Preuve |
| :--- | :--- | :--- | :--- |
| **validated_prompt_factory** | ON-DEMAND | `cmd/menu/sanity-*` | Any | Live (admin-trading) partiel + repo |
| **trae_module_validator** | ON-DEMAND | `cmd/menu/sanity-*` | Any | Live (admin-trading) présence + repo |
| **workflow_post_change_v2** | ON-DEMAND | `scripts/post_change.sh` | Any | Repo |
| **ops_menu_hub** | ON-DEMAND | `menu-ops_menu_hub` | MSI/Admin | Live (admin-trading) |
| **desk_pro_runner** | ON-DEMAND | `cmd-desk_pro_runner` | Admin | Live (admin-trading) |
| **desk_capture_inputs** | ON-DEMAND | `cmd-*` | Admin | Repo |
| **desk_analyze** | ON-DEMAND | `cmd-*` | Admin | Repo |
| **desk_pro_dashboard** | ON-DEMAND | `cmd-desk_pro_dashboard` | MSI | Live (admin-trading) présence |

### B. ANALYSIS ENGINES (ON-DEMAND)
Moteurs de calcul invoqués par le Runner ou manuellement.

| Module | Mode | Entrypoint | Cible | Preuve |
| :--- | :--- | :--- | :--- |
| **derivatives_analyzer** | ON-DEMAND | `cmd-*` | Admin | Repo |
| **probability_engine** | ON-DEMAND | `cmd-*` | Admin | Repo |
| **decision_engine** | ON-DEMAND | `cmd-*` | Admin | Repo |
| **risk_engine** | ON-DEMAND | `cmd-*` | Admin | Repo |
| **portfolio_engine** | ON-DEMAND | `cmd-*` | Admin | Repo |

### C. SERVICES (LONG-RUNNING)
Processus qui doivent tourner en permanence.

| Module | Mode | Unité Systemd | Cible | Preuve | Note |
| :--- | :--- | :--- | :--- | :--- |
| **vision_bot** | SERVICE | `vision_bot.service` | Admin | Live (admin-trading) | Watch Loop (ShareX inbox) |
| **shared_sshfs_permanent** | SERVICE | `shared-sshfs.service` | Clients Linux | Live (db-layer + student) + repo | Mount SSHFS `/shared` depuis `admin-trading` (live admin-trading : pas de service local) |
| **tv-bitget-runner** | SERVICE | `tv-bitget-runner.service` | Admin | Live (admin-trading) | Service infra (non cartographié comme module) |
| **tv-webhook** | SERVICE | `tv-webhook.service` | Admin | Live (admin-trading) | Service infra (FastAPI/Uvicorn) |

### D. TIMERS (PÉRIODIQUES)
Tâches de maintenance récurrentes.

| Module | Mode | Unité Systemd | Fréquence | Cible | Preuve |
| :--- | :--- | :--- | :--- | :--- |
| **desk_retention** | TIMER | `desk_retention.timer` | Repo: 10min ; Live(admin-trading): daily 03:00 | Admin | Repo + Live (admin-trading) |

### E. HYBRIDE (WATCH vs ONCE)
Modules supportant les deux modes.

| Module | Mode | Entrypoint | Preuve | Note |
| :--- | :--- | :--- | :--- |
| **desk_snapshot_ingest** | HYBRIDE | `cmd/menu/sanity-*` | Live (admin-trading) wrappers présents | Service systemd dédié non observé sur admin-trading |

## 3. ÉCARTS CONSTATÉS (DOC vs RÉEL)
1. **desk_retention** : le repo versionne un timer “every 10 minutes”, mais le live observé sur `admin-trading` est “daily 03:00”. Ne pas confondre packaging repo et override live.
2. **shared_sshfs_permanent** : le repo fournit un INSTALL + template systemd. Sur `admin-trading`, aucun service local `shared-sshfs.service` n'est observé (normal si `admin-trading` est l'hôte du share, pas le client mount).
3. **shared_sshfs_permanent** : sur `db-layer` et `student`, le service `shared-sshfs.service` et le montage `/shared` sont actifs (preuve live OT-DEPLOY-SSHFS-01 + OT-ROLL-SSHFS-02).
4. **shared_sshfs_permanent** : bug wrappers symlink observé sur `admin-trading` (OT-LIVE-01 : `name=local path=/usr/local`, `FAIL: scripts missing`) puis corrigé et revalidé (OT-PATCH-SSHFS-01 + OT-RECHECK-SSHFS-01 : `cmd ... info` et `sanity ...` OK). Le déploiement install (`/opt/trading/scripts/shared_sshfs_permanent_*`) reste absent sur `admin-trading`.
5. **desk_snapshot_ingest** : wrappers présents sur `admin-trading`, aucune unité systemd dédiée observée.
6. **tv-webhook / tv-bitget-runner** : services actifs observés sur `admin-trading` (snapshot infra). Ne pas inférer une normalisation “module” sans mission dédiée.

## 4. RÈGLE DE DÉPLOIEMENT
- Tout **SERVICE** ou **TIMER** doit avoir son fichier `.service`/`.timer` dans un sous-dossier `systemd/` du module.
- L'installation se fait via `sudo install` vers `/etc/systemd/system/`.
