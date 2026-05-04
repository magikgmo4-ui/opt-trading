---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_NEXT_GO_DECISION — Bot Vision Headless Review

## Verdict

**PASS** — La chaine existante est cartographiee, la faisabilite headless est confirmee.
Node.js et npm sont presents. Playwright/Chromium est l'option recommandee.
La chaine existante est compatible sans modification.

## Resume

- **3 modules vision** cartographies: bot_vision (legacy), vision_bot (actif), bot_vision_step2 (actif)
- **Chaine ShareX/SFTP** documentee: 4 problemes, 2 resolus, 2 en attente
- **Contrat desk_bridge** compatible: seul un garde-fou manque
- **Playwright/Chromium**: faisable, Node.js present, ~1h d'effort
- **Risques**: 5 identifies, tous maitrisables
- **Aucune modification requise** des modules existants

## Prochain GO recommande (P1)

### GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01

**Objectif**: Implementer la capture headless Playwright/Chromium sur admin-trading.

**Phases**:
1. Installer Playwright + Chromium (npm)
2. Creer capture.js (page.goto + screenshot + atomic write)
3. Creer systemd timer (intervalle configurable)
4. Creer wrappers (cmd, menu, sanity)
5. Validation: capture -> vision_inbox -> vision_bot -> desk_bridge

**Pre-requis**:
- admin-trading operationnel (OK)
- Node.js + npm (OK)
- vision_inbox propre (OK)
- Espace disque suffisant (a verifier)

## Alternatives

| GO | Priorite | Description |
| --- | --- | --- |
| GO_BRIDGE_GUARD_ADD_01 | P2 | Ajouter garde-fou [ -s ] dans bridge |
| GO_SHARED_REFRESH_01 | P3 | Rafraichir /shared/desk_pro/latest |
| GO_TIMERS_RESTORE_01 | P3 | Reviser timers desactives |
