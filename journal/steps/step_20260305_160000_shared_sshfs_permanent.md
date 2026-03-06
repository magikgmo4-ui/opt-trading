# Journal de bord — 2026-03-05 (America/Montreal)
## Session: go shared_sshfs_permanent

1) Objectif
- Transformer le bundle `shared_sshfs_permanent` en module versionné (scripts + menu/cmd/sanity), prêt à installer sur **student** et **db-layer**.
- Assurer un montage **permanent** de `/shared` via **SSHFS + systemd** (auto-start + reconnect).
- Ajouter commandes de validation et logs, puis **commit/push** sur `sot/mainline`.

2) Livrables (Step 1)
- Nouveau module: `modules/shared_sshfs_permanent/`
- Installateur: `modules/shared_sshfs_permanent/INSTALL.sh`
- Scripts standards: `shared_sshfs_permanent_menu.sh`, `shared_sshfs_permanent_cmd.sh`, `shared_sshfs_permanent_sanity.sh`
- Service systemd: `shared-sshfs.service` + env `/etc/opt-trading/shared_sshfs_permanent.env`

3) Commandes exécutées (à compléter côté machine)
- admin-trading: apply patch → git add/commit/push
- student + db-layer: git pull → install → sanity → mount check

4) Décisions
- Montage géré par service systemd `shared-sshfs.service` (Type=simple, sshfs -f, restart on failure).
- Config centralisée dans `/etc/opt-trading/shared_sshfs_permanent.env` (remote host/user/path, mountpoint, identity file, options).

5) Next
- Valider montage sur student et db-layer (mountpoint, écriture/lecture, permissions, auto-reconnect).
- (Option) ajuster `REMOTE_PATH` si le dossier partagé change.
