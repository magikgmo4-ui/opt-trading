---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01_REFS_INVENTORY
doc_type: inventory
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01
created_at: 2026-05-25
---

# 10_EXISTING_REFS_INVENTORY

## Inventaire des refs/timestamps par payload (pré-GO)

| Payload | Champs timestamp | Champs refs |
|---------|-----------------|-------------|
| `signal_event.v1` | `_ts` (legacy) | aucun |
| `desk_snapshot.v1` | `snapshot_ts`, `ingested_at` | aucun |
| `visual_context.v1` | `captured_at` | aucun |
| `market_metrics.v1` | `metrics_ts` | `primary_output`, `meta_output`, `latest`, `status` |
| `vision_analysis.v1` | `analysis_ts` | aucun |
| `telegram_claim.v1` | `claim_ts` | `telegram_message_ref` |
| `pair_market_snapshot.v1` | `generated_at`, `window_open_at`, `window_close_at` | aucun |

## Analyse des gaps

### Timestamps

- Pas de champ commun `produced_at` dans les payloads.
- Les noms de champs sont hétérogènes : `_ts`, `metrics_ts`, `analysis_ts`, etc.
- `generated_at` existe dans `pair_market_snapshot.v1` — le plus proche du standard cible.
- La jointure temporelle entre payloads est difficile sans champ commun.

### Refs

- Seul `market_metrics.v1` a un objet `refs` structuré (4 champs).
- `visual_context_ref` / `desk_snapshot_ref` dans `signal_event.v1` sont absents.
- `telegram_claim.v1` a `refs.telegram_message_ref` mais pas de ref au producer DC.
- `vision_analysis.v1` n'a aucune ref au fichier source.

## Conséquences pour la jointure Desk Pro

Les `join_checks` dans `dry_run.py` produisent WARN si `visual_context_ref` est absent,
jamais FAIL. Ce comportement est correct et n'est pas modifié par ce GO.

## Conclusion

Le standard doit être addif (add `produced_at` si absent) et backward-compatible.
Les champs legacy (`_ts`, `metrics_ts`, etc.) restent ALLOWED.
