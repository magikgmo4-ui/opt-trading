---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01_VALIDATION_PLAN
doc_type: validation_plan
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 30_VALIDATION_PLAN

## Validation git

```bash
git diff --check
```

## Validation tests (fixtures-first)

Priorité : réutiliser les tests existants Desk Pro, puis ajouter un test minimal si wrapper ajouté.

Commandes proposées :

```bash
python -m pytest -q tests/test_signal_event_adapter.py tests/test_desk_pro_dry_run.py -p no:cacheprovider
```

Si wrappers supplémentaires ajoutés :

```bash
python -m pytest -q tests/test_desk_pro_readonly_wrappers.py -p no:cacheprovider
```

## Garde-fous

- pas d’écriture hors `tmp_path` pytest
- pas d’accès réseau
- pas de Telegram live
- pas de Google Sheets

