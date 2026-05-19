---
doc_id: GO_EVENT_TAXONOMY_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_EVENT_TAXONOMY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_EVENT_TAXONOMY_01

## Résumé

- L’enveloppe canonique V1 est définie (read-only).
- Les familles et types cibles sont mappés sur les payloads existants (dataclasses + dicts).
- Aucun changement runtime requis dans ce GO.

## Lecture minimale

1. `20_CANONICAL_EVENT_ENVELOPE.md`
2. `30_EVENT_FAMILY_MAPPING.md`

## Vérif (local)

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

## Next GO (bundle)

```text
GO_TELEGRAM_EVENT_ROUTING_MAP_01
```
