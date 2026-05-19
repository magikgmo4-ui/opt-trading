# 10_CONSUMER_FLOW_FINDINGS

## Architecture

```
capture_headless.js
    → vision_inbox/ screen_*.png + screen_*.json

vision_bot.py (poll vision_inbox)
    → images traitées → vision_outbox/
    → images déplacées → vision_processed/

bridge_vision_to_desk_inbox.sh (pick latest)
    → lit depuis vision_processed/ ou vision_inbox/
    → crop 2x2 → desk_inbox/ (shared/inbox)

ingest_snapshots.py (poll desk_inbox)
    → copie/déplace → desk/snapshots/<symbol>/
    → index latest.json
```

## Findings par consumer

### 1. `vision_bot.py`

- **Sélection**: `list_images()` liste tous les fichiers image triés par mtime
- **Sidecar utilisé**: non (ignoré)
- **Risque**: traite les PNG `invalid_visual` et produit des OCR inutiles
- **Orphelins**: les JSON `blocked` sans PNG s'accumulent dans l'inbox

### 2. `bridge_vision_to_desk_inbox.sh`

- **Sélection**: `pick_latest()` prend le plus récent `screen_*.png`
- **Sidecar utilisé**: non
- **Risque**: crop et promeut un PNG `invalid_visual` vers Desk

### 3. `ingest_snapshots.py`

- **Sélection**: `iter_images()` liste fichiers image
- **Sidecar utilisé**: oui (lit `symbol`, `tf`, `ts`) mais pas `status`
- **Risque**: ingère des snapshots même si `status=invalid_visual`

## Modifications

| Fichier | Gate ajoutée |
|---|---|
| `vision_bot.py` | `check_sidecar_status()` → skip si blocked/invalid_visual → rejected/ |
| `bridge_vision_to_desk_inbox.sh` | `sidecar_status_ready()` via `jq` → skip si status != ready |
| `ingest_snapshots.py` | `meta.get("status")` → skip si blocked/invalid_visual → rejected/ |
