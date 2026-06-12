# OT-ROLL-SSHFS-02 — DEPLOY REPORT (LINUX CLIENTS)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Objectif : aligner les clients Linux sur `/shared` monté via `shared_sshfs_permanent`.
- Résultat : `db-layer` et `student` sont **déjà alignés** (service actif + mount /shared). Aucun (re)déploiement n’a été nécessaire, uniquement des preuves live.

## 2. DOCTRINE CANONIQUE RETENUE
- Source : `admin-trading:/srv/sftp/shared_files/shared`
- Clients Linux : montent sur `/shared` via systemd `shared-sshfs.service` (module `shared_sshfs_permanent`)

## 3. MACHINE(S) CIBLE(S)
- `db-layer` (10.66.66.2)
- `student` (10.66.66.3)

## 4. ÉTAT LIVE PAR MACHINE (COMMANDES + RÉSULTATS)

### 4.1 db-layer — ÉTABLI LIVE
```bash
systemctl is-active shared-sshfs.service
findmnt /shared
sanity-shared_sshfs_permanent
```
Résultats clés :
- service : `active`
- mount : `/shared` ← `ghost@admin-trading:/srv/sftp/shared_files/shared` (fuse.sshfs)
- sanity : PASS

### 4.2 student — ÉTABLI LIVE
```bash
systemctl status shared-sshfs.service --no-pager -n 25
findmnt /shared
sanity-shared_sshfs_permanent
cmd-shared_sshfs_permanent status
```
Résultats clés :
- service : active (running)
- mount : `/shared` ← `ghost@admin-trading:/srv/sftp/shared_files/shared` (fuse.sshfs)
- sanity : PASS

## 5. DÉPLOIEMENTS EFFECTUÉS
- Aucun déploiement exécuté pendant OT-ROLL-SSHFS-02 (standard déjà en place sur les deux clients Linux).

## 6. RÉSERVES RESTANTES
- Test de reconnexion réseau contrôlé (stabilité long-terme) : à exécuter dans une fenêtre autorisée (voir OT-SOAK-SSHFS-01).
- Extension à d’autres machines Linux : à décider explicitement machine par machine (hors périmètre si non prouvé nécessaire).

## 7. COMMANDES EXÉCUTÉES
- Voir §4.


## RISKS

- À qualifier.
