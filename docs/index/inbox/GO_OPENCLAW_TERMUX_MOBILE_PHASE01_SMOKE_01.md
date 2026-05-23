---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01
parent_go: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01
status: open
surface: index_inbox
source_kind: pointer
updated_at: 2026-05-23
topic_keys:
  - openclaw
  - mobile
  - termux
  - smoke
  - validation
links:
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01/10_MACHINE_SMOKE_RESULTS.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01/20_TERMUX_SMOKE_RESULTS.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01/30_LEDGER_AND_REPORT_EVIDENCE.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01/40_BLOCKED_WITH_REASON_TEST.md
---

# GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01

Validation smoke test du wrapper `openclaw_mobile_control.py` depuis machine et Termux.

## Scope

- Test des commandes `status`, `list-jobs`, `preflight`, `run-dry`.
- Vérification du ledger et des rapports.
- Test de la logique de blocage (sécurité).

## Verdict actuel

Machine Smoke: **PASS**
Blocking Logic: **PASS**
Termux Smoke: **PENDING**
