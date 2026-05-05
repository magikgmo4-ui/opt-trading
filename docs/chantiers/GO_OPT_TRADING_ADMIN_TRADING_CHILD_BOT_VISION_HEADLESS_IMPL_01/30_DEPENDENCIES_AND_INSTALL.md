---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01_DEPS
doc_type: dependencies_install
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_DEPENDENCIES_AND_INSTALL

## Pre-requis

| Outil | Version | Statut |
| --- | --- | --- |
| Node.js | v18.20.4 | OK |
| npm | 9.2.0 | OK |
| npx | present | OK |
| Playwright | 1.59.1 | INSTALLE |
| Chromium | 147.0.7727.15 | INSTALLE (~/cache/ms-playwright/) |
| FFmpeg | 1011 (playwright) | INSTALLE |
| Headless Shell | 147.0.7727.15 | INSTALLE |

## Commandes d'installation

```bash
cd /opt/trading/modules/bot_vision/headless_capture

# Installer Playwright (npm)
npm install

# Installer Chromium (170 MB download)
npx playwright install chromium
```

## Disk usage

| Composant | Taille |
| --- | --- |
| node_modules/ | ~2 MB |
| ~/.cache/ms-playwright/chromium-1217/ | ~300 MB |
| ~/.cache/ms-playwright/ffmpeg-1011/ | ~5 MB |
| ~/.cache/ms-playwright/chromium_headless_shell-1217/ | ~200 MB |
| Total | ~507 MB |
| Libre / | 185 GB (amplement suffisant) |

## Pas de dependances systeme

Aucun apt install necessaire. Playwright gere Chromium de maniere autonome.
Pas de Xvfb requis (Playwright headless natif).
Pas de librairies systeme supplementaires (Node.js suffit).
