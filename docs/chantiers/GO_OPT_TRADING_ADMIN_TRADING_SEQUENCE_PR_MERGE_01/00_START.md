---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01_START
doc_type: start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01
parent_go: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
previous_go: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 00_START - Sequence PR Merge

## GO ID

`GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01`

## Previous GO

`GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01` — verdict `PASS` @ `1456b91`

## Base branch

```
origin/go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01 @ 1456b91
```

## Objectif

Canoniser la séquence admin-trading producer/consumer vers `sot/mainline` via PR. Documenter le plan de merge, les fichiers impactés, les risques et la stratégie.

## Invariants

- Documentation + PR seulement
- Ne pas modifier runtime/service systemd
- Ne pas forcer le merge sans validation
- Le merge nécessite un `GO_MERGE` explicite après revue

## Runtime side effects attendus

`NONE` (documentation + PR creation only)
