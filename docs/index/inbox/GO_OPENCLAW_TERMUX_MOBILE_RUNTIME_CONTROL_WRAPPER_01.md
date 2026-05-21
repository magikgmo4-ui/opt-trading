---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01
parent_go: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01
status: open
surface: index_inbox
source_kind: pointer
updated_at: 2026-05-21
topic_keys:
  - openclaw
  - termux
  - mobile
  - runtime
  - wrapper
  - job_control
links:
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01/10_RUNTIME_SCOPE_AND_GATES.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01/20_WRAPPER_CONTRACT.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01/30_PHASE01B_IMPLEMENTATION_PLAN.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01/40_TEST_AND_EVIDENCE_PLAN.md
---

# GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01

Runtime GO to implement a bounded `openclaw_mobile_control` wrapper after the doc-only mobile control GO was merged.

## Scope

- define runtime scope and gates
- define wrapper contract
- prepare Phase 01B implementation
- prepare tests and evidence

## Exclusions

- no scheduler activation
- no external write
- no signal/trading
- no secrets
- no daemon/service install
- no global index edits
