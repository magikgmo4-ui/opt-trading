---
doc_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01

## Résumé

- Inventaire repo posé pour la chaîne "signal monitoring" : webhook + workers + Desk Pro + dispatcher + Telegram outbound + Sheets daily sync.
- Les surfaces "NEXT" du bundle qui restent à ouvrir ensuite sont surtout transverses (taxonomie/routing), pas du code d'exécution live.

## Lecture minimale

1. `10_CHAIN_SURFACE_PROOF_MAP.md`
2. `20_REUSE_MATRIX_AND_CONSTRAINTS.md`

## Commandes de vérification (local)

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

## Next GO (bundle)

```text
GO_EVENT_TAXONOMY_01
```
