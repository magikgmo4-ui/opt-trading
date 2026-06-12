# OT-DEPLOY-SSHFS-01 — CLEANUP REPORT (VARIANTES “SHARED”)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Déploiement live `/shared` via `shared_sshfs_permanent` est **prouvé** sur `db-layer`.
- Une variante legacy de montage sshfs vers `~/Téléchargements/SHARED` a été identifiée comme **redondante** et retirée de façon **réversible** (disable + mask + remplacement par symlink vers `/shared`).
- Les autres mécanismes “shared” (serveur SFTP, WinSCP Windows, scripts d’orchestration) restent **conservés** car encore utiles ou non prouvés obsolètes.

## 2. MACHINE CIBLE (CLEANUP LIVE)
- `db-layer` (Ubuntu 24.04.4, user `ghost`)

## 3. INVENTAIRE DES VARIANTES “SHARED” (REPO + LIVE)

### 3.1 shared_sshfs_permanent (canonique)
- **A. ÉTABLI LIVE** : `shared-sshfs.service` actif + `/shared` monté sur `db-layer`.
- **B. ÉTABLI REPO** : module installable (`INSTALL.sh`, template systemd, scripts /opt/trading/scripts).

### 3.2 shared_files_sftp (serveur)
- **E. ENCORE UTILISÉ / À CONSERVER** : fournit le répertoire serveur `/srv/sftp/shared_files/shared` utilisé par Windows (WinSCP) et comme source de vérité du share.

### 3.3 winscp_transfer (Windows)
- **E. ENCORE UTILISÉ / À CONSERVER** : sert au flux Windows → serveur SFTP ; non remplacé par sshfs (Windows n’est pas client sshfs ici).

### 3.4 Variante legacy sur db-layer : user unit sshfs vers ~/Téléchargements/SHARED
- **F. CANDIDAT AU RETRAIT** → **D. OBSOLÈTE PROUVÉ** après preuve de redondance.
- Preuves live :
  - Unit user : `shared-files-sftp-mount.service` (systemd --user) montait `sftp_db_layer@192.168.16.155:/shared` vers `~/Téléchargements/SHARED`.
  - En parallèle, `/shared` est déjà monté via `shared_sshfs_permanent`.
  - Sur `admin-trading`, `/shared` est un symlink vers `/srv/sftp/shared_files/shared` : la source est la même.

## 4. ÉLÉMENTS RETIRÉS (RÉVERSIBLE)

### 4.1 Retrait live (db-layer) — shared-files-sftp-mount.service
Statut : **RETIRÉ (réversible)**
- Action :
  - arrêt + disable du user service,
  - renommage du fichier unit en backup `*.retired_<timestamp>`,
  - mask via symlink vers `/dev/null` pour empêcher un redémarrage involontaire.
- Résultat :
  - plus de mount sshfs sur `~/Téléchargements/SHARED`,
  - `~/Téléchargements/SHARED` devient un symlink vers `/shared` (un seul share).

## 5. ÉLÉMENTS CONSERVÉS
- `shared_sshfs_permanent` (service systemd + wrappers) : canonique client mount.
- `shared_files_sftp` : serveur de dépôt / point d’entrée Windows.
- `winscp_transfer` : utile côté Windows, non remplacé par sshfs.
- Tous les autres scripts/docs “shared” : conservés faute de preuve d’obsolescence.

## 6. FICHIERS MODIFIÉS
- Repo : aucun fichier supprimé dans ce cleanup report (cleanup live uniquement).

## 7. COMMANDES EXÉCUTÉES (LIVE)
- Inspection :
  - `systemctl --user cat shared-files-sftp-mount.service`
  - `systemctl --user status shared-files-sftp-mount.service`
  - `findmnt /shared` et `findmnt ~/Téléchargements/SHARED`
  - `fuser -m ~/Téléchargements/SHARED`
- Retrait réversible :
  - `systemctl --user stop|disable shared-files-sftp-mount.service`
  - déplacement du fichier unit + `systemctl --user mask shared-files-sftp-mount.service`
  - remplacement par symlink `~/Téléchargements/SHARED -> /shared`

## 8. VERDICT FINAL
Cleanup conforme aux règles : une seule variante a été retirée, uniquement car redondance prouvée, et de façon réversible. Le reste est conservé par prudence.


## RISKS

- À qualifier.
