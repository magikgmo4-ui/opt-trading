---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01_STATE
doc_type: parent_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: open
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 90_PARENT_STATE — Bot Vision Headless Capture

## Statut

**OPEN** — Parent documentaire cree. Implementation differee au child GO.

## Fichiers

1. 00_INITIAL_PROJECT_DOC.md — Besoin, etat, objectif
2. 10_EXISTING_CAPTURE_REVIEW.md — Chaine ShareX/SFTP/vision_bot/bridge
3. 20_HEADLESS_CAPTURE_OPTIONS.md — Comparaison 5 options
4. 30_TARGET_ARCHITECTURE.md — Architecture cible headless
5. 40_DATA_CONTRACT.md — Contrat vision_inbox atomique
6. 50_IMPLEMENTATION_PLAN.md — Phases GO_IMPL_01
7. 60_RISKS_AND_GUARDRAILS.md — 7 risques + mitigations
8. 90_PARENT_STATE.md (ce fichier)

## Enfants

### Child review (en cours)

GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01
- Review complet de la chaine existante
- Validation faisabilite headless
- Decision next GO

### Child impl (futur)

GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01
- Installation Playwright/Chromium
- Script capture.js
- Systemd timer
- Wrappers
- Validation

## Dependances

- admin-trading operationnel (PASS)
- Desk Pro operationnel (PASS)
- Desk bridge deverrouille (PASS)
- vision_inbox propre (PASS)
- Node.js 18.20.4 present
- npm present
