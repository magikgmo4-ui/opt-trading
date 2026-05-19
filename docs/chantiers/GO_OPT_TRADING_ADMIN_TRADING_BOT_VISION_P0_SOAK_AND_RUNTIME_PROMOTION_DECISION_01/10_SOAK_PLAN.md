# 10_SOAK_PLAN

## Plan validé

1. Vérifier que le contenu status-aware gate est bien présent dans les consumers.
2. Exécuter 3 cycles manuels du profil smoke validé.
3. Pour chaque cycle, vérifier :
   - `status`
   - `visual_status`
   - PNG créé
   - sidecar JSON présent
   - ingestion en `vision_processed`
   - extraction `.txt` / `.md` en `vision_outbox`
   - desk downstream si applicable
   - lisibilité humaine
4. Produire une décision formelle :
   - `PROMOTE_P0_RUNTIME`
   - `PARTIAL_PROMOTE_RUNTIME`
   - `DEFER_PROMOTION_WITH_REASON`

## Vérification gate status-aware

Contenu confirmé dans la branche :

- `modules/vision_bot/app/vision_bot.py`
  - `SKIP_STATUSES`
  - `check_sidecar_status()`
  - `archive blocked orphan`
- `scripts/desk_bridge/bridge_vision_to_desk_inbox.sh`
  - `sidecar_status_ready()`
- `modules/desk_snapshot_ingest/ingest_snapshots.py`
  - `SKIP_STATUSES`
  - `Status gate: skip blocked/invalid_visual captures`
