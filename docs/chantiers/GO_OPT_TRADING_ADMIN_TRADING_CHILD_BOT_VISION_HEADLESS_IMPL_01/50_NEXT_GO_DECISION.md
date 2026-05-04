---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_NEXT_GO_DECISION — Bot Vision Headless Implementation

## Verdict

**PASS** — Module V1 fonctionnel. Capture headless Playwright/Chromium operationnelle. Pipeline end-to-end valide.

## Prochain GO recommande (P1)

### GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01

**Objectif**: Automatiser la capture headless avec un timer systemd.

La capture manuelle fonctionne. Le prochain pas est l'automatisation:
- Creer bot_vision_headless.service (oneshot)
- Creer bot_vision_headless.timer (intervalle configurable)
- Installer wrappers globaux (cmd, menu, sanity)
- Valider le cycle automatique

## Backlog

| GO | Priorite | Description |
| --- | --- | --- |
| GO_BOT_VISION_HEADLESS_SYSTEMD_01 | P1 | Timer systemd + wrappers |
| GO_BRIDGE_GUARD_ADD_01 | P2 | Garde-fou [ -s ] dans bridge |
| GO_DESK_PRO_SHARED_REFRESH_01 | P3 | Rafraichir /shared/desk_pro/latest |
| GO_TIMERS_RESTORE_01 | P3 | Reviser timers desactives |
