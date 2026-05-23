---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01_INBOX
doc_type: inbox
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01 — inbox

## Rôle

Second child GO du parent Data Center. Formalise les contrats consumers.

```text
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: CONSUMER_CONTRACTS_FORMALIZED_V1
```

## État

- `00_INITIAL_PROJECT_DOC.md` — ouvert.
- `10_CONSUMER_CONTRACT_SPEC.md` — livré.
- `20_CONSUMER_INVENTORY.md` — livré (7 consumers : Desk Pro ×2, Strategy, Perf, Telegram, Sheets, LocalCMS).
- BUNDLE_TARGET atteint — child fermable.
- Aucun runtime modifié. Aucun index global modifié.

## Point clé

Desk Pro est le seul consumer implémenté (`market_metrics_reader.py`). Migration vers path Data Center : `migration_needed: true`.

## Prochain geste

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01
```

## Source

`docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01/`
