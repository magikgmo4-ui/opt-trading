---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_IMPL_POC_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_IMPL_POC_01
parent_go: GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01
status: active
lifecycle_stage: implementation
surface: chantier
source_kind: canonical
created_at: 2026-05-30
updated_at: 2026-05-30
---

# 00_START — Pipeline Implementation POC

## GO

GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_IMPL_POC_01

## Parent canonique

PF_BOT_VISION_HEADLESS (ACTIVE_EXPANSION)
Parent GO: GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01

## Branche

go/GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_IMPL_POC_01
Base: origin/sot/mainline

## Contexte

Pipeline planning terminé (docs/chantiers/GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01/).
Module capture existant : modules/bot_vision/headless_capture/ (Playwright + Chromium, profiles.json, capture_headless.js).
Pas d'analyseur, pas de pipeline output, pas de liaison Data Center ni DeskPro.

## Objectif

POC fonctionnel du pipeline complet sur un actif unique (BTCUSDT 15m) :
capture → analyse → outputs → Data Center → DeskPro.

## Périmètre

| Bloc | Fait | À faire |
|------|------|---------|
| Capture Playwright | ✅ Existant | Valider profile BTCUSDT 15m |
| Analyse LLM/OCR | ❌ | Intégrer analyseur vision |
| vision_analysis.json | ❌ | Produire et écrire |
| Payload Data Center | ❌ | Structurer et POST |
| Telegram filtré | ❌ | Envoyer résumé si signal fort |
| desk/analysis/btcusdt.latest.json | ❌ | Écrire pour DeskPro |

## Livrables

1. Playwright profile BTCUSDT 15m validé → capture PNG + sidecar meta
2. Analyseur vision (LLM + OCR) branché → JSON analysis
3. vision_analysis.json écrit dans desk/analysis/
4. Payload structuré Data Center produit (POST ou fallback local)
5. Message Telegram envoyé (filtré, si signal >= 0.6)
6. desk/analysis/btcusdt.latest.json consommable par DeskPro

## Règles strictes

- Ne pas casser le système de capture existant (capture_headless.js, profiles, atomic write)
- Ne pas modifier les services systemd existants
- Écriture atomique préservée pour tous les fichiers
- Profiles existants conservés (profiles.example.json, *.smoke.local.json)
- PF_BOT_VISION_HEADLESS reste OPEN — ne pas fermer

## Gaps adressés

G-IN-01, G-CAP-01, G-AN-01, G-AN-02, G-DC-01, G-DP-01, G-INT-01
(voir 80_GAPS_AND_NEXT_GO.md du child planning)

## Prochain GO après POC

GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_EXTEND_01
(extension multi-actifs + Coinglass + screener)
