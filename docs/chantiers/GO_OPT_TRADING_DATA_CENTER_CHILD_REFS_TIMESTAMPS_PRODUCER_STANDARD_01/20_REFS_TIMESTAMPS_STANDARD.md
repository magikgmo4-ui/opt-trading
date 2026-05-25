---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01_STANDARD
doc_type: canonical_standard
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01
created_at: 2026-05-25
version: REFS_TIMESTAMPS_PRODUCER_STANDARD_01
---

# 20_REFS_TIMESTAMPS_STANDARD

## Standard `REFS_TIMESTAMPS_PRODUCER_STANDARD_01`

### Objectif

Permettre la jointure entre payloads producers et la traçabilité des données
dans PF_DATA_CENTER, PF_DESK_PRO, PF_PERF_ENGINE, PF_SHEETS.

### Catégories de champs

#### REQUIRED_CORE

Tout nouveau payload producer doit inclure au moins un champ timestamp de production.
Le champ recommandé est `produced_at`.

```json
{
  "produced_at": "2026-05-25T00:00:00Z"
}
```

Règle : ISO 8601 UTC, suffixe `Z` ou `+00:00`.

#### OPTIONAL_BY_CONTRACT

Selon le contrat du payload, certains champs refs sont recommandés :

```json
{
  "refs": {
    "primary_output": "data/data_center/<family>/<producer_id>/latest.json",
    "latest": "data/data_center/views/<contract_class>/latest.json",
    "status": "data/data_center/<family>/<producer_id>/status.json",
    "source_ref": "<upstream_canonical_ref>"
  }
}
```

Règle : le champ `refs` est un objet plat ; les clés sont libres mais doivent
être documentées dans le contrat du payload.

#### LEGACY_ALLOWED

Les champs timestamp historiques sont acceptés sans migration obligatoire :

| Champ legacy | Payload | Équivalent standard |
|-------------|---------|---------------------|
| `_ts` | signal_event.v1 | → `produced_at` si migré |
| `metrics_ts` | market_metrics.v1 | timestamp des métriques sources (différent de produced_at) |
| `analysis_ts` | vision_analysis.v1 | timestamp de l'analyse |
| `claim_ts` | telegram_claim.v1 | timestamp du claim |
| `generated_at` | pair_market_snapshot.v1 | ≈ `produced_at` pour ce payload |
| `captured_at` | visual_context.v1 | timestamp de la capture |
| `snapshot_ts` | desk_snapshot.v1 | timestamp du snapshot |
| `ingested_at` | desk_snapshot.v1 | timestamp d'ingestion |

Règle : ces champs ne doivent PAS être supprimés. Les consumers peuvent
les utiliser pour la jointure temporelle.

### Helper `modules/data_center/refs_timestamps.py`

```python
now_utc_z() -> str
    # → "2026-05-25T12:00:00Z"

build_refs(primary_output=None, latest=None, status=None, **extra) -> dict
    # → {"primary_output": "...", "latest": "...", ...}

enrich_produced_at(payload: dict, produced_at=None) -> dict
    # Adds produced_at if absent. Does not overwrite. Returns new dict.

validate_iso_utc(ts: str) -> bool
    # → True if valid ISO 8601 UTC

is_compatible_legacy(payload: dict) -> (bool, list[str])
    # → (True, []) if payload has at least one recognized timestamp field
```

### Politique de migration

| Priorité | Action |
|----------|--------|
| Phase 1 (ce GO) | Standard documenté, helper créé, tests écrits |
| Phase 2 | Appeler `enrich_produced_at()` dans les nouveaux writers |
| Phase 3 | Ajouter `refs` structuré dans market_metrics_writer et spot_snapshot_dc_writer |
| Jamais | Supprimer les champs legacy existants |

### Invariants

- Le standard est additif : il ajoute des champs, n'en supprime jamais.
- `is_compatible_legacy()` retourne WARN (pas FAIL) si aucun timestamp reconnu.
- Les consumers Desk Pro ne bloquent JAMAIS sur les refs/timestamps absents.
