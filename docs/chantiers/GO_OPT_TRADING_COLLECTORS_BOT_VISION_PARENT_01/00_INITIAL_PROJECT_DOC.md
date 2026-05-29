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

Alimenter DeskPro avec un pipeline headless robuste capable de choisir les bonnes
adresses / écrans / assets, capturer les bons visuels, analyser les screenshots,
produire des outputs utiles (images, analyse, setups, Telegram), pousser un
maximum de données structurées vers Data Center, puis rendre ces données
exploitables côté DeskPro.

## 2_INITIAL_PROJECT_DOC

Ce document ouvre le parent canonique `GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01`
pour `PF_BOT_VISION_HEADLESS`. Les premiers child GOs d'implémentation historiques
existent déjà sous le workstream admin-trading, mais le parent ne peut pas être
fermé : la surface réelle couvre désormais un pipeline complet `input -> capture
-> analyse -> outputs -> Data Center -> DeskPro`, encore non validé de bout en
bout.

## 4_MASTER_PROJECT_PLAN

1. Input surface expansion — URL / pages / assets / charts / indices / screeners
2. Capture validation — viewport, sections, reproductibilité, multi-capture
3. Analysis enrichment — OCR, lecture visuelle, extraction setup/signal
4. Output generation — images, analyses, setup cards, payload Telegram
5. Data Center handoff — max data out structuré
6. DeskPro consumption — contrat de consommation final

## 5_GO_PLAN — Child GOs

| GO | Rôle |
|---|---|
| `GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01` | Headless capture Playwright implementation |
| `GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01` | Systemd timer automation |
| `GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01` | Desk Pro bridge integration smoke |
| `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_STATUS_AWARE_INGESTION_GATE_01` | Status-aware ingestion gate |
| `GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01` | Expansion canonique du pipeline complet input -> DeskPro |

## CLOSE_GATE_MASTER_TARGET

```text
NON ATTEINT — l'historique capture/runtime existe, mais le pipeline complet
input -> capture -> analyse -> outputs -> Data Center -> DeskPro reste à prouver.
```
