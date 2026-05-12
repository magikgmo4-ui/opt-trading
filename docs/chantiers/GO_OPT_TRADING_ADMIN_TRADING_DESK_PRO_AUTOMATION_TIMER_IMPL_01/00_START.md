---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01_START
doc_type: start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01
status: active
lifecycle_stage: start
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
parent_go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01
parent_commit: 567cb41
---

# 00_START - Timer Implementation

## Parent GO

`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01` — PASS, pushed as `567cb41`

## Objectif

Implementer les fichiers systemd versionnes pour automatiser Desk Pro en dry-run.

## Roadmap

1. Spec alignment
2. Implementation files (systemd)
3. Entrypoint script
4. Validation
5. Installation runbook draft
6. Closeout

## Preconditions

- [x] TIMER_SPEC complete et push
- [x] 50/50 tests pass
- [x] Spec timer validée dans 20_TIMER_SPEC.md

## Gates

- Tests must pass
- No runtime side effects (timer inactive)
- Files versionnes uniquement