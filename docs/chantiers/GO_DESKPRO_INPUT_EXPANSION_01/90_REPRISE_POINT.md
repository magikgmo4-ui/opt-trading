---
doc_id: GO_DESKPRO_INPUT_EXPANSION_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_DESKPRO_INPUT_EXPANSION_01

## Résumé

- inputs réels Desk Pro recensés (desk_snapshot, signal_event, visual_context)
- classes d’inputs cibles posées (vision_analysis, market_metrics, telegram_claim)
- contraintes de jointure et preuves minimales fixées

## Lecture minimale

1. `20_TARGET_INPUT_CLASSES.md`
2. `30_PROOF_MATRIX_AND_CONSTRAINTS.md`
3. `40_GAPS_AND_NEXT_GO.md`

## Vérif (local)

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

## Next GO bundle

```text
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
```
