# shared_files_sftp — serveur SFTP (surface /shared)

## But
Ce module configure/diagnostique la couche **serveur SFTP** sur `admin-trading` qui expose la surface canonique `shared`.

## Surface canonique
- Source réelle : `/srv/sftp/shared_files/shared`
- Alias local : `/shared`

## À ne pas confondre
- `shared` (module) : UX d’usage quotidien côté Linux (`cmd-shared ls|get|put|...`) pour manipuler le contenu de la surface.
- `shared_sshfs_permanent` : client Linux (systemd) qui monte `/shared` sur `db-layer` et `student`.
- `winscp_transfer` : workflow WinSCP/ops (inbox/outbox) pour transferts Windows <-> Linux.

## Entrypoints (module)
- `cmd-shared_files_sftp`
- `menu-shared_files_sftp`
- `sanity-shared_files_sftp`

