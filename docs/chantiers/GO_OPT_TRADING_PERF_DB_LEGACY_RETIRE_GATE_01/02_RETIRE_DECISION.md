---
doc_id: GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01_RETIRE_DECISION
doc_type: retire_decision
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01
status: draft_for_review
lifecycle_stage: child_retire_decision
parent_go_id: GO_OPT_TRADING_PERF_DB_PATH_SWITCH_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - db
  - retire
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01/02_RETIRE_DECISION.md
point_de_reprise: "Décider explicitement quand le legacy peut être retiré."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01/01_GATE_CONDITIONS.md
---

# 02_RETIRE_DECISION

## 1_DECISION

```text
Legacy DB path must remain available until all gate conditions are proven.
No time-based retirement.
Only proof-based retirement.
```

## 2_NEXT_GO

```text
GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01
```

Condition :

```text
toutes les preuves du gate sont collectées et validées.
```
