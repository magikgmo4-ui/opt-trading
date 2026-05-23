---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01_INBOX
doc_type: inbox
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01 — inbox

## Rôle

Troisième child GO du parent Data Center. Crée le module `modules/data_center/`.

```text
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: DATA_CENTER_LAYOUT_AND_REGISTRY_INIT
```

## État

- `modules/data_center/layout.py` — livré (`ensure_data_center_dirs`, `get_producer_dir`, `load_*_registry`).
- `modules/data_center/registry/producers.json` — 3 producers committés.
- `modules/data_center/registry/consumers.json` — 7 consumers committés.
- `modules/data_center/scripts/` — 4 scripts convention module présents.
- `modules/data_center/tests/test_layout.py` — **11/11 tests passent**.
- BUNDLE_TARGET atteint — child fermable.

## Contrainte clé

`data/` est gitignored. Le layout runtime `data/data_center/` est créé par `ensure_data_center_dirs()`. Les registres canoniques sont committés sous `modules/data_center/registry/`.

## Prochain geste

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01
```

## Source

`modules/data_center/` + `docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01/`
