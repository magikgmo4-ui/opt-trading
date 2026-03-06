# Journal de bord — 2026-03-05 (America/Montreal)
## Session: shared_sshfs_permanent — patch 1b

1) Constat
- Sur **student**: `/shared` déjà monté → `chown /shared: Permission non accordée` pendant INSTALL.
- Sur **db-layer**: service actif et monté, mais le sanity affichait `FAIL: systemd unit missing` (faux négatif lié au check `list-unit-files`).

2) Fix (patch 1b)
- `INSTALL.sh`: si `/shared` est déjà un mountpoint, **skip** mkdir/chown/chmod (tolérant).
- `sanity.sh`: check de l’unité via `systemctl cat shared-sshfs.service` (plus fiable).

3) Actions
- Appliquer patch sur admin-trading, commit/push.
- Sur student + db-layer: `git pull --ff-only` puis relancer `sudo bash modules/shared_sshfs_permanent/INSTALL.sh` (met à jour /opt/trading/scripts) puis `sanity-shared_sshfs_permanent`.
