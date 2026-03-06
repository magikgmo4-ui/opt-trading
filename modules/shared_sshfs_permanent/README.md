# shared_sshfs_permanent (module)

But: monter **/shared** de façon permanente via **SSHFS** (systemd) depuis `admin-trading`.

## Usage rapide (après install)
- `sanity-shared_sshfs_permanent`
- `cmd-shared_sshfs_permanent status`
- `cmd-shared_sshfs_permanent mount`
- `cmd-shared_sshfs_permanent logs`
- `menu-shared_sshfs_permanent`

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
