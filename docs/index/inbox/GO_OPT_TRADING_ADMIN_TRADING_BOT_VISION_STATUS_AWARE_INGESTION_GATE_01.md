# GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_STATUS_AWARE_INGESTION_GATE_01

Status: `in_progress`

Objectif: Adapter l'ingestion downstream (vision_bot, desk_bridge, desk_snapshot_ingest) pour filtrer les captures non-ready.

Livrables:
- `vision_bot.py` : gate + rejected dir
- `bridge_vision_to_desk_inbox.sh` : gate jq dans pick_latest
- `ingest_snapshots.py` : gate sur meta.status

Voir: `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_STATUS_AWARE_INGESTION_GATE_01/`
