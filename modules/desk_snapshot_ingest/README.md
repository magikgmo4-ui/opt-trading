# desk_snapshot_ingest — Step A (admin-trading)
Ingest screenshots dropped via SFTP into an inbox folder, archive them by symbol, and maintain:
- latest.json (latest snapshot per symbol)
- history.jsonl (append-only ingest log)

Default paths (override via env or args):
- INBOX_DIR: /srv/sftp/shared_files/shared/inbox
- DEST_DIR:  /opt/trading/desk/snapshots
- INDEX_FILE: /opt/trading/desk/snapshots/latest.json
- HISTORY_FILE: /opt/trading/desk/snapshots/history.jsonl
- PROCESSED_DIR: /srv/sftp/shared_files/shared/inbox/_processed

Filename convention (recommended):
SYMBOL_TF_YYYYMMDD_HHMMSS.png
Example: BTCUSDT.P_H1_20260303_140855.png

Optional sidecar metadata JSON (same basename + .json) overrides parsing.

Quick run (from /opt/trading):
- sanity: modules/desk_snapshot_ingest/scripts/sanity_check.sh
- ingest: modules/desk_snapshot_ingest/scripts/cmd.sh ingest_once
- menu:   modules/desk_snapshot_ingest/scripts/menu.sh

Optional: install global shortcuts (sudo):
modules/desk_snapshot_ingest/scripts/install_shortcuts.sh
Installs:
- /usr/local/bin/menu-desk_snapshot_ingest
- /usr/local/bin/cmd-desk_snapshot_ingest
- /usr/local/bin/sanity-desk_snapshot_ingest

## Statut de stack
- satellite d'ingestion en amont de Desk Pro
- adjacent a la stack, sans etre un substitut a `desk_pro_runner`, `desk_pro_orchestrator` ou `desk_pro_dashboard`
