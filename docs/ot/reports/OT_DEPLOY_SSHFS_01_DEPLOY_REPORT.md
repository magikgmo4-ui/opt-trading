# OT-DEPLOY-SSHFS-01 — DEPLOY REPORT (shared_sshfs_permanent)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Machine cible identifiée et prouvée : **`db-layer`** (Ubuntu 24.04.4).
- `shared_sshfs_permanent` est **déjà déployé et actif** sur `db-layer` : service `shared-sshfs.service` actif + `/shared` réellement monté depuis `admin-trading:/srv/sftp/shared_files/shared`.
- Aucun “re-deploy” (réinstallation) n’a été exécuté : déploiement existant validé par preuves live et tests non destructifs.

## 2. MACHINE CIBLE
- Nom : `db-layer`
- Accès : SSH en user `ghost` (IP VPN 10.66.66.2)

## 3. DÉPLOIEMENT EXÉCUTÉ
- **Déploiement déjà présent avant mission** (preuves live) :
  - `/etc/systemd/system/shared-sshfs.service` : présent + enabled
  - `/etc/opt-trading/shared_sshfs_permanent.env` : présent
  - `/opt/trading/scripts/shared_sshfs_permanent_*` : présents
  - `/shared` : monté (sshfs)
- Actions réalisées pendant la mission : **validation + tests live** (voir §4)

## 4. TESTS LIVE (NON DESTRUCTIFS)

### 4.1 Wrappers installés
Statut : **PASS**
```bash
command -v cmd-shared_sshfs_permanent sanity-shared_sshfs_permanent menu-shared_sshfs_permanent
ls -l /usr/local/bin/cmd-shared_sshfs_permanent /usr/local/bin/sanity-shared_sshfs_permanent /usr/local/bin/menu-shared_sshfs_permanent
```

### 4.2 Sanity module
Statut : **PASS**
```bash
sanity-shared_sshfs_permanent || true
```

### 4.3 Service systemd
Statut : **PASS**
```bash
systemctl status shared-sshfs.service --no-pager -n 40
systemctl cat shared-sshfs.service --no-pager
```
Résultat clé (extrait) :
- Active: **active (running)**
- ExecStart: `/opt/trading/scripts/shared_sshfs_permanent_mount.sh`

### 4.4 Mount réel /shared
Statut : **PASS**
```bash
findmnt /shared
mountpoint -q /shared && echo MOUNTED || echo NOT_MOUNTED
ls -lah /shared | head -n 60
```
Résultat clé (extrait) :
- SOURCE : `ghost@admin-trading:/srv/sftp/shared_files/shared`
- FSTYPE : `fuse.sshfs`

### 4.5 Logs service (lecture)
Statut : **PASS AVEC NOTE**
```bash
journalctl -u shared-sshfs.service -n 30 --no-pager || true
```
Note : des timeouts réseau historiques existent dans les logs (évènements passés), sans invalider l’état “actif” au moment du test.

## 5. ÉTAT FINAL SSHFS
- Canonique live (prouvé) : `db-layer` exécute `shared-sshfs.service` et monte `/shared` depuis `admin-trading`.
- `admin-trading` : hôte du share (chemin serveur `/srv/sftp/shared_files/shared` ; `/shared` est un symlink).

## 6. FICHIERS MODIFIÉS
- Repo : aucun fichier de code modifié par ce report (les modifications repo associées au chantier wrappers ont déjà été livrées dans OT-PATCH/OT-RECHECK).

## 7. COMMANDES EXÉCUTÉES
- Voir sections 4.1 à 4.5.

## 8. VERDICT FINAL
`shared_sshfs_permanent` est **déployé et opérationnel en live** sur `db-layer` (service + mount `/shared` prouvés). La voie canonique “/shared” est donc prouvée côté client mount.


## RISKS

- À qualifier.
