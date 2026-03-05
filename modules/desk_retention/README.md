# desk_retention — Step 0 (prune old files / avoid stale buildup)

Objectif: éviter l’accumulation de vieilles captures/fichiers et réduire les risques de “stale data”.

Prune (mtime) sur des dossiers configurables:
- /opt/trading/desk/snapshots
- /srv/sftp/shared_files/shared/inbox
- /srv/sftp/shared_files/shared/vision_processed
- /srv/sftp/shared_files/shared/vision_outbox
- /opt/trading/_work/bot_vision_step2

Safe-by-default:
- `dry_run` liste ce qui serait supprimé
- rétention uniquement par jours (KEEP_DAYS)

## Install
1) unzip au root du repo `/opt/trading`
2) `bash INSTALL.sh`
3) `modules/desk_retention/scripts/sanity_check.sh`
4) `modules/desk_retention/scripts/cmd.sh dry_run`
5) `modules/desk_retention/scripts/cmd.sh prune_now`

## Timer (optionnel)
`modules/desk_retention/scripts/cmd.sh install_timer`
