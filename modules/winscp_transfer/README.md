# winscp_transfer — Shared inbox/outbox + push/pull to machines

## But
Faciliter le workflow:
Windows (WinSCP) -> admin-trading:/srv/sftp/shared_files/shared/inbox -> push vers student (ou autre hôte)
et récupération inverse via outbox.

Note : sur `admin-trading`, `/shared` est un alias de `/srv/sftp/shared_files/shared`.

## Dossiers standard (créés par `cmd-winscp_transfer init`)
- /srv/sftp/shared_files/shared/inbox   : dépôt WinSCP (upload)
- /srv/sftp/shared_files/shared/outbox  : fichiers à télécharger (download)
- /srv/sftp/shared_files/shared/modules : zips de modules (optionnel)
- /srv/sftp/shared_files/shared/_logs   : logs

## Installation (sur admin-trading)
```bash
unzip winscp_transfer_bundle.zip -d /tmp/wst
sudo bash /tmp/wst/APPLY.sh
sanity-winscp_transfer
sudo cmd-winscp_transfer init
menu-winscp_transfer
```

## Usage rapide
1) Sur Windows (WinSCP): upload dans `.../shared/inbox`
2) Sur admin-trading:
- Lister: `cmd-winscp_transfer ls inbox`
- Envoyer vers student: `cmd-winscp_transfer send student <fichier>`
- Déployer un zip module sur student: `cmd-winscp_transfer deploy student <zip>`
- Récupérer depuis student vers outbox: `cmd-winscp_transfer fetch student <remote_path>`

## Windows (chemin local recommandé)
- Dossier local canonique (établi sur poste) : `C:\Users\ghost\Downloads\SHARED\`

## À ne pas confondre
- `shared` (module) : UX Linux générique pour lister/déposer/récupérer sur la surface (`cmd-shared ls|get|put|...`).
- `shared_files_sftp` : couche serveur SFTP (comptes/sshd) qui expose la surface.
- `shared_sshfs_permanent` : client Linux (systemd) qui monte `/shared` sur `db-layer` et `student`.

## Configuration hôtes
Par défaut:
- student host = "student"
Tu peux override:
- `STUDENT_HOST=192.168.16.103 cmd-winscp_transfer send student file.zip`

## Statut de suite
- workflow Windows <-> Linux de transfert sur la surface `shared`
- adjacent a `reseau_ssh`, mais non inclus dans la lignée `reseau_ssh*`
- specialise dans l'inbox/outbox et le push/pull operatoire, pas dans la baseline SSH ni le montage `sshfs`
