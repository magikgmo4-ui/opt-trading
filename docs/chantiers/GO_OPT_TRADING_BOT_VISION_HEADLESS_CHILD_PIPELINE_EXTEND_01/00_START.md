---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_EXTEND_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_EXTEND_01
parent_go: GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01
status: active
lifecycle_stage: planning
surface: chantier
source_kind: canonical
created_at: 2026-05-30
updated_at: 2026-05-30
---

# 00_START — Pipeline Extension multi-asset / multi-source

## GO

GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_EXTEND_01

## Dépendance

Requiert GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_IMPL_POC_01 : PASS
(pipeline BTCUSDT 15m validé avant extension)

## Objectif

Étendre le pipeline POC à la surface complète définie dans l'inventaire input :
multi-actifs, multi-sources, multi-types d'écran.

## Périmètre

| Bloc | Actifs / Sources | Priorité |
|------|-----------------|----------|
| Extension crypto | ETHUSDT, TOTAL, TOTAL2, TOTAL3, BTC.D | P0 |
| Métaux / macro | XAUUSDT, XAUUSD, DXY, US10Y, VIX | P0 |
| Énergie | BZUSDT, BRENT, WTI | P0 |
| Coinglass | Liquidation heatmap, funding, OI, L/S ratio | P0 |
| ETF crypto | IBIT, FBTC, GBTC, BITB, ARKB | P1 |
| Stock screener | Biggest caps, trending, AI, defense, space, crypto, energy | P1 |
| News / calendar | Economic calendar, earnings | P2 |

## Livrables par extension

### Vague 1 — Multi-asset chart (P0)

- Profiles Playwright pour chaque actif P0 (timeframes : 15m, 1h, 4h, 1D)
- Capture validée + analyse pour chaque actif
- vision_analysis.json produit pour chaque actif
- Vue macro multi-chart (BTC + Gold + DXY + Oil)

### Vague 2 — Coinglass derivatives (P0)

- Profiles Playwright pour Coinglass (heatmap, funding, OI, L/S)
- Analyseur spécialisé LIQUIDITY_DERIVATIVES_SCREEN
- Payload enrichi avec signaux de liquidité

### Vague 3 — Stock screener (P1)

- Profiles Playwright pour TradingView screener
- Analyseur spécialisé STOCK_SCREENER_SCREEN
- Détection rotation sectorielle + momentum clusters

### Vague 4 — ETF + News (P2)

- Profiles ETF crypto
- Analyseur ETF_CRYPTO_SCREEN
- Calendar / news integration (design only)

## Mise à jour des contrats

| Contrat | Mise à jour |
|---------|-------------|
| profiles.json | Nouveaux profiles par actif/source |
| Analyseurs | Nouveaux analyseurs Coinglass + screener |
| Data Center schema | Enrichi pour multi-source |
| DeskPro views | Nouvelles vues macro + screener |

## Gaps adressés

G-IN-02, G-IN-03, G-IN-04, G-CAP-02, G-CAP-03, G-CAP-04, G-CAP-05, G-AN-03
(voir 80_GAPS_AND_NEXT_GO.md du child planning)

## Prochain GO après EXTEND

GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_DATACENTER_DESKPRO_01
(intégration Data Center complète + consommation DeskPro finalisée)
