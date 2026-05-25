---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01_EXISTING_SURFACE
doc_type: inventory
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01
created_at: 2026-05-25
updated_at: 2026-05-25
---

# 10_EXISTING_SURFACE_READ

## Surface Desk Pro avant ce GO

### `market_metrics_reader.py` — état existant

`modules/desk_pro/service/market_metrics_reader.py` existait déjà et lit :

```text
1. data/data_center/views/market_metrics/latest.json  (DC canonical view)
2. data/deskpro/inputs/market_metrics/latest.json      (legacy fallback)
```

`read_market_metrics()` retourne `List[Metric]` — vide si aucun fichier présent.
28 tests existants validaient déjà ce reader.

Registry DC :
- `desk_pro__market_metrics.implementation_status = implemented` ✓
- `desk_pro__market_metrics.migration_needed = false` ✓

### `dry_run.py` — état avant GO

- Paramètres : `signal_event`, `visual_context`, `desk_snapshot`
- `summary` : `signal_event_present`, `visual_context_present`, `desk_snapshot_present`
- Pas de `market_metrics` dans le pipeline dry-run
- Pas de `summary.market_metrics_present`

### Gap identifié

`market_metrics.v1` était lisible mais pas intégré dans la synthèse dry-run.
Le dry-run ignorait complètement le contexte marché.

## Surface après ce GO

```python
result = run_desk_pro_dry_run(
    signal_event_payload,
    visual_context=vc,
    desk_snapshot=snap,
    market_metrics=read_market_metrics(),   # List[Metric] ou []
)

result["summary"]["market_metrics_present"]  # True / False
result["warnings"]  # contient "market_metrics missing: market-context-free synthesis" si absent
```

Absence de `market_metrics` → WARN, pas FAIL. Comportement cohérent avec `visual_context` et `desk_snapshot`.
