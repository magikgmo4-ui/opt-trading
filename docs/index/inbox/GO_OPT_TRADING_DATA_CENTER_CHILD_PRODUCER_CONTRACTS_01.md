---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01_INBOX
doc_type: inbox
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01 — inbox

## Rôle

Premier child GO du parent Data Center. Formalise les contrats producers.

```text
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: PRODUCER_CONTRACTS_FORMALIZED_V1
```

## État

- `00_INITIAL_PROJECT_DOC.md` — ouvert.
- `10_PRODUCER_CONTRACT_SPEC.md` — livré (format canonique contrat producer).
- `20_PRODUCER_INVENTORY.md` — livré (3 producers : bitget, binance, binance_spot).
- BUNDLE_TARGET atteint — child fermable.
- Aucun runtime modifié. Aucun index global modifié.

## Prochain geste

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01
```

## Source

`docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01/`
