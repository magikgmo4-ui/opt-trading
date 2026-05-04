---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: open
lifecycle_stage: plan
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_INITIAL_PROJECT_DOC — Bot Vision Headless Capture Parent

## GO

GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Besoin initial

La chaine de capture Vision -> Desk Pro depend actuellement de ShareX sur Windows.
Le produit final vise depuis la gouvernance : un pipeline vision cross-platform ou un
provider headless browser unifie `bot_vision` entre Windows et Linux sans dependre
de ShareX.

L'inbox est regulierement polluee par des fichiers 0-byte et .uploading partiels (SFTP
interrompu). Le GO_VISION_INBOX_REPAIR_01 a nettoye l'inbox, mais la cause racine
(fragilite SFTP Windows -> Linux) n'est pas resolue.

## Etat actuel

| Composant | Statut | Machine |
| --- | --- | --- |
| vision_bot.service | ACTIF (watch loop OCR) | admin-trading |
| bot_vision_step2.service | ACTIF (Telegram + OpenAI Vision) | admin-trading |
| desk_bridge.timer | ACTIF (every 10 min) | admin-trading |
| vision_inbox | CLEAN (0 fichiers) | admin-trading |
| ShareX | Absent de la machine | Windows/cursor-ai |
| Playwright/Chromium/Xvfb | ABSENT | admin-trading |
| Node.js | v18.20.4 | admin-trading |
| npm | present | admin-trading |
| Python | 3.11.2 | admin-trading |

## Objectif bot_vision_headless

Remplacer la dependance ShareX/SFTP Windows -> Linux par une capture headless
autonome sur admin-trading, utilisant Playwright/Chromium en mode headless,
produisant des screenshots directement dans vision_inbox avec ecriture atomique.

## Limites

- Ce parent est documentaire. L'implementation est dans un child GO dedie.
- Aucun runtime modifie dans ce parent.
- Aucune installation d'outils dans ce parent.
- La cible est admin-trading uniquement (pas db-layer, pas student).

## Invariants

- vision_bot et bot_vision_step2 restent les modules de traitement
- desk_bridge reste le bridge vision -> Desk Pro
- /shared/desk_pro/latest/ reste la sortie canonique
- Aucun trading reel
- PAPER mode preserve
