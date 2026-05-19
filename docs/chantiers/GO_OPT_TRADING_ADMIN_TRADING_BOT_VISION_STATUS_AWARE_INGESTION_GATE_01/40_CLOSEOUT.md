# 40_CLOSEOUT

GO: `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_STATUS_AWARE_INGESTION_GATE_01`

## Livré

- [x] `vision_bot.py` : skip blocked/invalid_visual → rejected/ + orphan cleanup
- [x] `bridge_vision_to_desk_inbox.sh` : `sidecar_status_ready()` dans `pick_latest`
- [x] `ingest_snapshots.py` : skip blocked/invalid_visual → rejected/
- [x] Backward compatible : sidecar absent = legacy behavior
- [x] Aucune suppression des PNG invalides

## Invariants respectés

- `profiles.example.json` non modifié
- Aucun restart service/timer
- Aucune suppression
- Aucun archive/compression
- Aucun .env lu
- Aucun trade

## Commit

```
feat: gate bot vision ingestion by capture status
```
