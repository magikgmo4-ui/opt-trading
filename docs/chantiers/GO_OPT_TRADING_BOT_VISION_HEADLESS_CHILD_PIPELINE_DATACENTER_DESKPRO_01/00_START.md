---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_DATACENTER_DESKPRO_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_DATACENTER_DESKPRO_01
parent_go: GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01
status: active
lifecycle_stage: planning
surface: chantier
source_kind: canonical
created_at: 2026-05-30
updated_at: 2026-05-30
---

# 00_START — Data Center Handoff + DeskPro Consumption finalization

## GO

GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_DATACENTER_DESKPRO_01

## Dépendance

Requiert GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_EXTEND_01 : PASS
(pipeline multi-asset + multi-source validé avant intégration aval)

## Objectif

Finaliser l'aval du pipeline : ingestion Data Center complète et consommation DeskPro aboutie.

## Périmètre

### Data Center

| Bloc | Livrable |
|------|----------|
| Endpoints vision | POST /dc/ingest/vision/raw + /analysis + /summary + /distribution |
| Schema max data out | Implémenté et validé (raw_capture / extracted_signal / generated_summary / distribution_payload) |
| Fallback local | data/dc_fallback/ avec script de rejeu |
| Retry policy | 3 tentatives, intervalle 5s, timeout 10s |
| Retention | Rotation images 7j, analyses 30j, setups 90j |

### DeskPro

| Bloc | Livrable |
|------|----------|
| vision_analysis.json | Écrit dans desk/analysis/{symbol}.latest.json |
| setup_card.json | Écrit dans desk/setups/active.json |
| DeskPro notification | Polling ou inotify sur desk/analysis/ |
| Vue dashboard | Dernière analyse par actif dans DeskPro |
| Vue setup watch | Setups actifs tous actifs |
| Vue timeline | Historique 24h des analyses |

### Telegram

| Bloc | Livrable |
|------|----------|
| Filtrage par importance | Signal >= 0.6 ou setup détecté |
| Rate limiting | Max 8 messages/h |
| Format finalisé | Template par type de signal |

### Close Gate

| Critère | Description |
|---------|-------------|
| Pipeline E2E | Capture → analyse → outputs → DC → DeskPro prouvé sur BTCUSDT |
| Multi-asset | Au moins 5 actifs couverts (BTC, ETH, Gold, Oil, DXY) |
| Data Center | Endpoints implémentés + fallback + retry |
| DeskPro | vision_analysis.json + setup_card.json consommés |
| Telegram | Messages filtrés envoyés |
| Tests | Smoke test pipeline complet |

## Prochain GO après DC+DeskPro

CLOSE_GATE — PF_BOT_VISION_HEADLESS
(close gate du parent après validation E2E complète)
