# OT-FIX-SSHFS-01 — DIAGNOSTIC (shared_sshfs_permanent)

Date (America/Montreal) : 2026-03-12

## 1. RÉSUMÉ EXÉCUTIF
- Le module `shared_sshfs_permanent` est **conçu (repo)** pour déployer un montage `/shared` via **SSHFS + systemd** (`shared-sshfs.service`) et un fichier de config `/etc/opt-trading/shared_sshfs_permanent.env`.
- Sur `admin-trading` (preuve live OT-LIVE-01), l’unité systemd `shared-sshfs.service` est **absente**, `/shared` n’est **pas monté**, mais des wrappers existent.
- L’incohérence principale est une **combinaison** :
  - **déploiement incomplet / non effectué** (artefacts install absents),
  - **packaging hybride** (scripts “installés” vs scripts “module wrappers”),
  - **wrappers cassés via symlink** (scripts `cmd.sh` / `sanity_check.sh` non robustes à `/usr/local/bin`).

## 2. PREUVES RELUES
- Live (admin-trading) : [OT_LIVE_01_MACHINE_DRILL.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_LIVE_01_MACHINE_DRILL.md), [OT_LIVE_01_REPORT.md](file:///c:/Users/ghost/opt-trading/docs/ot/reports/OT_LIVE_01_REPORT.md)
- Repo : [README.md](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/README.md), [INSTALL.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/INSTALL.sh), [shared-sshfs.service.template](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/systemd/shared-sshfs.service.template)
- Repo wrappers “module wrappers” : [cmd.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/cmd.sh), [menu.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/menu.sh), [sanity_check.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/sanity_check.sh)
- Repo scripts “installés / opérationnels” : [shared_sshfs_permanent_cmd.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/shared_sshfs_permanent_cmd.sh), [shared_sshfs_permanent_menu.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/shared_sshfs_permanent_menu.sh), [shared_sshfs_permanent_mount.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/shared_sshfs_permanent_mount.sh)

## 3. DIAGNOSTIC REPO (PACKAGING)

### 3.1 Hypothèse de base du module (repo)
- Objectif explicite : “monter `/shared` de façon permanente via SSHFS (systemd)”. Voir [README.md](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/README.md#L1-L29).
- Modèle systemd : `shared-sshfs.service.template` → produit `shared-sshfs.service` (installé sous `/etc/systemd/system/`). Voir [shared-sshfs.service.template](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/systemd/shared-sshfs.service.template#L1-L18).
- Installateur : `INSTALL.sh` installe dépendances, crée `/etc/opt-trading/shared_sshfs_permanent.env`, copie des scripts dans `/opt/trading/scripts/`, et crée des wrappers globaux. Voir [INSTALL.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/INSTALL.sh#L4-L115).

### 3.2 Deux “familles” de scripts (packaging hybride)
- **Famille A — module wrappers** (génériques) : `modules/shared_sshfs_permanent/scripts/{cmd.sh,menu.sh,sanity_check.sh}`.
  - Ces scripts déduisent le chemin du module depuis `$0` et ne résolvent pas le cas symlink `/usr/local/bin`.
  - Exemple : [cmd.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/cmd.sh#L1-L29), [sanity_check.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/sanity_check.sh#L1-L13).
- **Famille B — scripts installés / opérationnels** : `shared_sshfs_permanent_{cmd,menu,mount,umount}.sh`.
  - Ils pilotent explicitement `shared-sshfs.service`, lisent `/etc/opt-trading/shared_sshfs_permanent.env` et appellent `/opt/trading/scripts/shared_sshfs_permanent_mount.sh`. Voir [shared_sshfs_permanent_cmd.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/shared_sshfs_permanent_cmd.sh#L1-L113).

### 3.3 Intention repo (réponse Q1)
- **Oui, au repo** le module est pensé pour être un **service live** (systemd) sur une machine cible, via installateur.
- Le repo ne prouve pas que ce service est effectivement déployé sur `admin-trading`.

## 4. DIAGNOSTIC LIVE (ADMIN-TRADING)

### 4.1 Preuves live sur systemd / mount
- `shared-sshfs.service` : **absent** (unit not found). Preuve : [OT_LIVE_01_MACHINE_DRILL.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_LIVE_01_MACHINE_DRILL.md).
- `/shared` : **non monté** (`findmnt /shared` vide). Preuve : [OT_LIVE_01_MACHINE_DRILL.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_LIVE_01_MACHINE_DRILL.md).

### 4.2 Preuves live sur wrappers
- `menu/cmd/sanity-shared_sshfs_permanent` : **présents** en `/usr/local/bin` et pointent vers `modules/shared_sshfs_permanent/scripts/*`. Preuve : [OT_LIVE_01_MACHINE_DRILL.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_LIVE_01_MACHINE_DRILL.md).
- Exécution : `cmd-shared_sshfs_permanent info` retourne `name=local path=/usr/local`. Preuve : [OT_LIVE_01_MACHINE_DRILL.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_LIVE_01_MACHINE_DRILL.md).
- Sanity : `sanity-shared_sshfs_permanent` retourne `FAIL: scripts missing`. Preuve : [OT_LIVE_01_MACHINE_DRILL.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_LIVE_01_MACHINE_DRILL.md).

### 4.3 Interprétation “name=local path=/usr/local” (réponse Q3)
- Ce comportement est **un symptôme de mauvais contexte** : les scripts “module wrappers” déduisent la racine module depuis le chemin du wrapper (`/usr/local/bin/...`), donc “module = /usr/local”.
- Ce n’est pas cohérent avec l’intention du module (monter `/shared` via systemd + config).

### 4.4 Origine du FAIL “scripts missing” (réponse Q4)
- Ce FAIL est cohérent avec le même mécanisme : `MOD=/usr/local`, donc `/usr/local/scripts` n’existe pas → `FAIL: scripts missing`.
- Il s’agit d’un **bug de robustesse symlink** de la famille A (`cmd.sh` / `sanity_check.sh`), pas d’une preuve que le module entier est inutilisable.

## 5. CAUSE PROBABLE RETENUE
- `admin-trading` semble avoir reçu des **wrappers “module wrappers”** (famille A) sans avoir reçu le **déploiement systemd** prévu par `INSTALL.sh` (famille B + `shared-sshfs.service` + env file).
- Donc : **déploiement incomplet + packaging hybride mal documenté + wrapper non symlink-safe**.

## 6. CLASSIFICATION CANONIQUE (shared_sshfs_permanent)
- **A. ÉTABLI REPO** : module = installer systemd SSHFS (`shared-sshfs.service`) + config `/etc/opt-trading/...` + scripts `/opt/trading/scripts/...`.
- **B. ÉTABLI LIVE (admin-trading)** : wrappers présents, mais pointent vers la mauvaise famille de scripts et ne fonctionnent pas via symlink.
- **D. ÉCART REPO/LIVE** : service absent, mount absent, wrappers installés d’une manière non conforme à l’intention de l’installateur.

## 7. RÉPONSES (QUESTIONS OBLIGATOIRES)
1. Service live attendu sur admin-trading ? **Attendu au repo**, **non observé live** sur admin-trading.
2. Wrappers live cohérents avec le design du module ? **Non**, ils pointent vers la famille A (générique) au lieu de la famille B (opérationnelle).
3. “name=local path=/usr/local” attendu ? **Non**, symptôme de symlink non résolu.
4. FAIL “scripts missing” : bug wrapper vs mauvais chemin vs déploiement incomplet ? **Bug symlink + mauvais ciblage des wrappers**, dans un contexte de **déploiement incomplet**.
5. Statut canonique correct dans runtime map ? **Repo: Service (installable)** ; **Live admin-trading: absent/non déployé + wrappers incohérents**.
6. Schedule live desk_retention prouvé sur admin-trading ? **Daily 03:00** (preuve `systemctl cat desk_retention.timer` dans OT-LIVE-01).


## RISKS

- À qualifier.
