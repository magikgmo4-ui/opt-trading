---
doc_id: GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: bot_vision_headless
go_id: GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01
parent_go_id: null
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-29
updated_at: 2026-05-29
GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID: PF_BOT_VISION_HEADLESS
MASTER_PROJECT_PLAN_ID: MPP_BOT_VISION_HEADLESS_OPERATIONAL
BUNDLE_TARGET: null
NEXT_ATTACH_TARGET: null
topic_keys:
  - opt-trading
  - bot_vision
  - headless_capture
  - product_surface
links:
  - docs/index/GO_INDEX.md
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
---

# GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Bot Vision / Headless Screener opérationnel : capture visuelle headless (Playwright)
→ extraction OCR/OpenAI → artefacts exploitables pour Desk Pro et Telegram.

## 2_INITIAL_PROJECT_DOC

Ce document ouvre le parent canonique `GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01`
pour `PF_BOT_VISION_HEADLESS`. Tous les child GOs d'implémentation sont déjà clos
sous le workstream admin-trading. Cette ouverture formalise le parent produit,
inventorie les 4 child GOs principaux, et ferme le parent immédiatement
(ouverture et fermeture simultanées, car l'implémentation pré-existe).

## 4_MASTER_PROJECT_PLAN

1. Headless capture runtime (Playwright + Chromium) — ✅ DONE
2. Systemd timer automation — ✅ DONE
3. Desk Pro bridge integration — ✅ DONE
4. Status-aware ingestion gate — ✅ DONE

## 5_GO_PLAN — Child GOs

| GO | Rôle |
|---|---|
| `GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01` | Headless capture Playwright implementation |
| `GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01` | Systemd timer automation |
| `GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01` | Desk Pro bridge integration smoke |
| `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_STATUS_AWARE_INGESTION_GATE_01` | Status-aware ingestion gate |

## CLOSE_GATE_MASTER_TARGET

```text
ATTEINT — 4 child GOs principaux complétés, 11 GO totaux dans le workstream.
```
