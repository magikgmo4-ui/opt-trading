---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01_FEASIBILITY
doc_type: feasibility_assessment
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_HEADLESS_FEASIBILITY — Evaluation

## Pre-requis techniques

| Outil | Statut | Action |
| --- | --- | --- |
| Node.js | v18.20.4 (present) | OK |
| npm | present | OK |
| Playwright | ABSENT | npm install |
| Chromium | ABSENT | npx playwright install chromium |
| Xvfb | ABSENT | Non requis (Playwright headless natif) |
| ffmpeg | ABSENT | Non requis |
| Espace disque | ~1.5 GB libre necessaire | A verifier |

## Compatibilite avec la chaine existante

| Composant | Impact | Modification requise |
| --- | --- | --- |
| vision_bot | Aucun | Non |
| bot_vision_step2 | Aucun | Non |
| desk_bridge | Aucun | Garde-fou optionnel |
| Desk Pro | Aucun | Non |
| vision_inbox | Meme dossier | Non |
| SFTP | Plus necessaire | Non (reste fallback) |

## Risques maitrisables

| Risque | Niveau | Mitigation |
| --- | --- | --- |
| Secrets/cookies | MOYEN | URLs publiques ou profil isole |
| Fichiers 0-byte | FAIBLE | Atomic write + verification |
| Charge CPU/RAM | FAIBLE | Oneshot timer, pas de daemon |
| Crash Chromium | FAIBLE | Timeout 30s + retry |
| Conflit ShareX | FAIBLE | Nommage unique, coexistence |

## Verdict

**FAISABLE** — Tous les pre-requis sont satisfaits ou faciles a installer.
La chaine existante est compatible sans modification.
Seul un garde-fou optionnel dans desk_bridge est recommande.

## Estimation effort

| Phase | Effort | Risque |
| --- | --- | --- |
| Installation Playwright/Chromium | 5 min | Faible |
| Script capture.js | 30 min | Moyen |
| Systemd timer | 10 min | Faible |
| Wrappers | 10 min | Faible |
| Validation | 15 min | Moyen |
| **Total** | **~1h** | **Faible** |
