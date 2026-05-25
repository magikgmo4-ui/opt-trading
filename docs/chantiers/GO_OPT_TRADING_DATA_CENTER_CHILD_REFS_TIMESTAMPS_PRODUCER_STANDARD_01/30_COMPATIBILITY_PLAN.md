---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01_COMPAT_PLAN
doc_type: compatibility_plan
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01
created_at: 2026-05-25
---

# 30_COMPATIBILITY_PLAN

## Vérification fixtures existantes

Tous les fixtures existants passent `is_compatible_legacy()` :

| Fixture | Champ timestamp reconnu | Résultat |
|---------|------------------------|---------|
| `market_metrics_v1_minimal.json` | `metrics_ts` | ✅ COMPATIBLE |
| `vision_analysis_v1_minimal.json` | `analysis_ts` | ✅ COMPATIBLE |
| `telegram_claim_v1_minimal.json` | `claim_ts` | ✅ COMPATIBLE |
| `signal_event_v0_minimal.json` | `_ts` | ✅ COMPATIBLE |
| `desk_snapshot_minimal.json` | `snapshot_ts` | ✅ COMPATIBLE |
| `visual_context_v1_minimal.json` | `captured_at` | ✅ COMPATIBLE |

**Aucune fixture cassée.**

## Tests non-régression DC suite

```
110 passed in 0.36s
```

Suite complète DC inchangée après introduction du helper.

## Plan de migration producers (phase 2)

### Priorité 1 — `market_metrics_writer.py`

Appeler `enrich_produced_at()` sur le payload avant écriture DC :
```python
from modules.data_center.refs_timestamps import enrich_produced_at
payload = enrich_produced_at(payload)
```
Impact : ajoute `produced_at` sans casser `metrics_ts` existant.

### Priorité 2 — `spot_snapshot_dc_writer.py`

`generated_at` existe déjà dans pair_market_snapshot.
Ajouter `produced_at = generated_at` si absent dans la couche bridge.

### Priorité 3 — vision/telegram producers futurs

Tout nouveau producer doit appeler `enrich_produced_at()` avant écriture.

## Risque résiduel

Faible — le helper est purement additif et ne modifie aucun contrat existant.
