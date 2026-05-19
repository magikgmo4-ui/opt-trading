# 00_INITIAL_PROJECT_DOC

GO: `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_STATUS_AWARE_INGESTION_GATE_01`

## Objectif

Adapter l'ingestion downstream du bot vision (`vision_bot`, `desk_bridge`, `desk_snapshot_ingest`) pour respecter les nouveaux statuts sidecar produits par `capture_headless.js`.

## Contexte

- Commit failure classification: `d313a66f`
- `capture_headless.js` produit maintenant des statuts `ready`, `blocked`, `invalid_visual`
- Les consommateurs aval ne filtrent pas encore ces statuts
- Risque: une capture `invalid_visual` (spinner) ou `blocked` (timeout sans PNG) peut être promue vers Desk

## Invariants

1. Ne pas modifier `profiles.example.json`
2. Ne pas promouvoir P0 vers timer
3. Ne pas redémarrer service/timer
4. Ne rien supprimer
5. Ne pas archiver/comprimer durablement
6. Ne pas lire .env
7. Ne pas trader

## Livrables

1. `vision_bot.py` : skip blocked/invalid_visual, rejected dir
2. `bridge_vision_to_desk_inbox.sh` : status gate dans pick_latest
3. `ingest_snapshots.py` : skip blocked/invalid_visual
4. Docs chantier (00-40) + index inbox
