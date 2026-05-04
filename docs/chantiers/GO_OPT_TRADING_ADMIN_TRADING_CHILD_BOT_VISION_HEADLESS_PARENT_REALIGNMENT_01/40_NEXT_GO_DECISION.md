---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_NEXT_GO_DECISION — Parent Realignment

## Verdict

**PASS** — Realignement documentaire complet. Aucun index a patcher.

## Prochain GO recommande (P1)

### GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01

| Propriete | Valeur |
| --- | --- |
| Type | Child implementation |
| Parent | GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 |
| Objectif | Installer Playwright/Chromium, creer capture.js, systemd timer |
| Source | Review headless (GO_CHILD_BOT_VISION_HEADLESS_REVIEW_01, PASS) |
| Estimation | ~1h |

**Phases**:
1. Installer Playwright + Chromium (npm)
2. Creer capture.js (page.goto + screenshot + atomic write vers vision_inbox)
3. Creer systemd timer (intervalle configurable)
4. Creer wrappers (cmd, menu, sanity)
5. Validation end-to-end

## Backlog

| GO | Priorite | Description |
| --- | --- | --- |
| GO_BRIDGE_GUARD_ADD_01 | P2 | Garde-fou [ -s ] dans bridge |
| GO_SHARED_REFRESH_01 | P3 | Rafraichir /shared/desk_pro/latest |
| GO_TIMERS_RESTORE_01 | P3 | Reviser timers desactives |

## Arbre admin-trading final

```
GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)
  |
  +-- GO_PARENT_REVIEW_01 (PASS)
  +-- GO_DESK_PRO_RUNTIME_REVIEW_01 (PASS)
  +-- GO_VISION_INBOX_REPAIR_01 (PASS)
  +-- GO_DESK_BRIDGE_RETRY_01 (PASS)
  +-- GO_DESK_PRO_SMOKE_01 (PASS)
  +-- GO_CHILD_BOT_VISION_HEADLESS_REVIEW_01 (PASS)
  +-- GO_CHILD_BOT_VISION_HEADLESS_REALIGNMENT_01 (PASS, ce GO)
  +-- GO_CHILD_BOT_VISION_HEADLESS_IMPL_01 (NEXT P1)
  +-- GO_BRIDGE_GUARD_ADD_01 (BACKLOG P2)
```
