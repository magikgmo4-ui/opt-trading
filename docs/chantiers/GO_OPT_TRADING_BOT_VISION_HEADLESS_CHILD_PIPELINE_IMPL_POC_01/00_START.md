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
Module analyse existant (production) : modules/bot_vision_step2/ (OpenAI vision, resize/crop, Telegram, DeskPro artifacts).

⚠ Architecture : ne PAS reconstruire localement ce que bot_vision_step2 fait déjà.
   Ce POC est un adaptateur qui :
   - utilise capture_headless.js (Playwright) — unique, pas dans bot_vision_step2
   - délègue l'analyse à bot_vision_step2 analyze_latest
   - écrit vision_analysis.v1 au chemin canonique du reader DeskPro

## Objectif

POC fonctionnel du pipeline sur BTCUSDT 15m, en réutilisant l'infra existante :
capture_headless.js (Playwright) → bot_vision_step2 (analyse) → DeskPro.

## Périmètre

| Bloc | Fait | Méthode |
|------|------|---------|
| Capture Playwright | ✅ Existant | capture_headless.js (profile BTCUSDT 15m) |
| Analyse LLM/OCR | ✅ Existant (prod) | bot_vision_step2 analyze_latest (OpenAI gpt-4.1-mini) |
| vision_analysis.v1 | ✅ Stub | run_vision_pipeline.py → data/deskpro/inputs/vision_analysis/latest.json |
| Telegram | ✅ Existant (prod) | bot_vision_step2 (image + analyse caption) |
| DeskPro output | ✅ Existant (prod) | bot_vision_step2 → summary.json + DESKPRO_VISION_DIR |

## Livrables

1. ✅ Profile Playwright BTCUSDT 15m (profiles.btcusdt_poc.json)
2. ✅ capture_headless.js enrichi (indicators dans sidecar)
3. ✅ run_vision_pipeline.py — adaptateur capture → bot_vision_step2 → DeskPro
4. ✅ vision_analysis.v1 au chemin canonique du reader DeskPro (data/deskpro/inputs/vision_analysis/latest.json)
5. ❌ ~~analyze_capture.py~~ supprimé (dupliquait bot_vision_step2)

## Architecture retenue

```
capture_headless.js (Playwright)
  → vision_inbox/
    → bot_vision_step2 analyze_latest (OpenAI, Telegram, artifacts)
    → run_vision_pipeline.py (stub vision_analysis.v1 pour DeskPro reader)

Voie alternative (via bridge existant) :
  vision_inbox/ → bridge_vision_to_desk_inbox.sh → inbox/
    → desk_snapshot_ingest → /opt/trading/desk/snapshots/latest.json
    → desk_analyze analyze_latest.py (lecture latest.json + Binance data)
```

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
