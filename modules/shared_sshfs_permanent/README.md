# shared_sshfs_permanent (module)

But: monter **/shared** de façon permanente via **SSHFS** (systemd) depuis `admin-trading`.

À ne pas confondre :
- `shared` (module) : UX d’usage quotidien pour lister/déposer/récupérer des fichiers sur la surface (`cmd-shared ls|get|put|...`).
- `shared_files_sftp` : couche serveur SFTP sur `admin-trading` (expose `/srv/sftp/shared_files/shared`).

## Usage rapide (après install)
- `sanity-shared_sshfs_permanent`
- `cmd-shared_sshfs_permanent status`
- `cmd-shared_sshfs_permanent mount`
- `cmd-shared_sshfs_permanent logs`
- `menu-shared_sshfs_permanent`

Note : ces wrappers globaux sont conçus pour pointer vers les scripts installés dans `/opt/trading/scripts/`. Si un wrapper pointe vers `modules/shared_sshfs_permanent/scripts/*`, il reste utilisable pour inspection et délègue vers `/opt/trading/scripts/` quand ces scripts existent.

## Config
Fichier: `/etc/opt-trading/shared_sshfs_permanent.env`

Champs clés:
- `REMOTE_HOST` (défaut: admin-trading)
- `REMOTE_USER` (défaut: ghost)
- `REMOTE_PATH` (défaut: /srv/sftp/shared_files/shared)
- `MOUNT_POINT` (défaut: /shared)
- `IDENTITY_FILE` (défaut: /home/<local_user>/.ssh/id_ed25519)

## Installer (sur une machine cible)
Depuis `/opt/trading` (après `git pull`):
```bash
sudo bash modules/shared_sshfs_permanent/INSTALL.sh
sanity-shared_sshfs_permanent
cmd-shared_sshfs_permanent mount
cmd-shared_sshfs_permanent status
```

## Statut de suite
- client Linux de montage permanent de la surface `shared`
- adjacent a `reseau_ssh_step2`, mais non inclus dans la lignée `reseau_ssh*`
- complement naturel de `shared_files_sftp` :
  - `shared_files_sftp` expose
  - `shared_sshfs_permanent` monte
