---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01_IMPL_PLAN
doc_type: implementation_plan
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01
status: open
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_IMPLEMENTATION_PLAN — Bot Vision Headless

## Prochain GO

GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01

## Phases d'implementation

### Phase 1: Installation outils

1. Installer Playwright: `npm install -g playwright`
2. Installer Chromium: `npx playwright install chromium`
3. Verifier: `npx playwright --version`

### Phase 2: Script de capture

1. Creer `modules/bot_vision_headless/capture.js`
   - page.goto(TARGET_URL) avec config TradingView/Coinglass
   - page.screenshot() fullPage ou viewport
   - Sauvegarde atomique vers vision_inbox
2. Config: `modules/bot_vision_headless/config.json`
   - URLs cibles
   - Intervalle capture
   - Resolution viewport

### Phase 3: Systemd

1. Creer `modules/bot_vision_headless/systemd/bot_vision_headless.service`
   - Type=oneshot
   - User=ghost
   - ExecStart=/usr/bin/node .../capture.js
2. Creer `modules/bot_vision_headless/systemd/bot_vision_headless.timer`
   - Intervalle configurable (ex: 5 min)

### Phase 4: Wrappers

1. `cmd-bot_vision_headless` — lancement manuel
2. `menu-bot_vision_headless` — menu interactif
3. `sanity-bot_vision_headless` — verifications

### Phase 5: Validation

1. Lancer capture.js manuellement
2. Verifier screen_*.png dans vision_inbox (taille > 0)
3. Verifier vision_bot traite l'image (watch loop detecte)
4. Verifier desk_bridge croppe 2x2
5. Verifier Desk Pro recoit snapshots

## Ordre

1. GO_IMPL_01: Installation + script + systemd + validation
2. GO_CLEANUP: Nettoyer les wrappers/scripts obsoletes apres migration

## Non-scope

- Ne pas supprimer ShareX (fallback)
- Ne pas modifier vision_bot
- Ne pas modifier bot_vision_step2
- Ne pas modifier desk_bridge
- Ne pas toucher Desk Pro
- Ne pas activer trading reel
