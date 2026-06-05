---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01_EXISTING_VIEWS_AND_PATHS
doc_type: audit
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 40_EXISTING_VIEWS_AND_PATHS

## Objet

Inventaire exhaustif des vues Data Center existantes et des paths legacy DeskPro, avec verification des chemins effectifs vs registry.

## 1. Views Data Center existantes

### 1.1 market_metrics/

```text
data/data_center/views/market_metrics/
├── latest.json          (present)
└── by_symbol/           (present, directory)
```

| Consumer | Path | Existe |
|---|---|---|
| desk_pro__market_metrics | latest.json | OUI |
| strategy_framework__market_context | by_symbol/ | OUI |
| perf_engine__replay_context | history/ | NON (directory non liste, a verifier) |
| telegram_screener__signal_context | latest.json | OUI |
| google_sheets__market_reporting | latest.json | OUI |

**Status :** OK pour latest_only. by_symbol present. history/ a confirmer.

### 1.2 vision_analysis/

```text
data/data_center/views/vision_analysis/
└── by_symbol/
    ├── BTCUSDT.P.json
    ├── ETHUSDT.P.json
    ├── SOLUSDT.P.json
    ├── XRPUSDT.P.json
    ├── TVC:DXY.json
    ├── TVC:US10Y.json
    ├── TVC:VIX.json
    ├── OANDA:XAUUSD.json
    ├── SPY.json
    ├── NASDAQ:IBIT.json
    ├── NASDAQ:FBTC.json
    ├── NASDAQ:BITB.json
    ├── NASDAQ:ARKB.json
    ├── NYMEX:CL1!.json
    ├── NYMEX:NG1!.json
    ├── NYMEX:RB1!.json
    ├── FX:EURUSD.json
    ├── CRYPTOCAP:TOTAL.json
    ├── CRYPTOCAP:TOTAL2.json
    └── BITGET:BZUSDT.json
```

| Consumer | Path | Existe |
|---|---|---|
| desk_pro__vision_analysis | deskpro/inputs/vision_analysis/latest.json | LEGACY (hors DC view) |
| dashboards__vision_analysis_history | data_center/views/vision_analysis/history/ | NON (history/ absent) |

> **Note :** Le consumer dashboards reference `history/` mais le directory contient `by_symbol/`. Deconnecte.

### 1.3 market_metrics (pair_market_snapshot view)

```text
data/data_center/views/pair_market_snapshot/   ← ABSENT
```

| Consumer | Path | Existe |
|---|---|---|
| desk_pro__spot_snapshot | latest.json | NON |

### 1.4 vision_context/

Aucun sous-dossier `vision_context/` dans `views/`. Les 3 contracts (coinglass, screener, news_sentiment) n'ont pas de view directory dedie.

Cependant, les producers ecrivent dans :

```text
data/data_center/views/vision_context/coinglass/
data/data_center/views/vision_context/screener/
data/data_center/views/vision_context/news_sentiment/
```

Ces paths sont des output producer paths (pas des views neutres), ce qui confirme la violation de convention notee en 30_.

### 1.5 Autres views (non liees aux contracts audites)

```text
data/data_center/views/
├── analysis/                  (non reference dans consumers.json)
├── coinglass/                 (squeeze_alerts/)
├── data_center_coverage/      (non reference)
├── telegram_context/          (non reference)
├── telegram_discovery/        (non reference)
├── telegram_performance/      (non reference)
└── telegram_signals/          (non reference)
```

> **Note :** 7 directories de views existent sans consumer enregistre dans `consumers.json`. Ces views ne sont pas documentees dans le registry et leur origine/usage est inconnu dans le cadre de cet audit.

## 2. Paths legacy DeskPro

### 2.1 Fichiers presents

```text
data/deskpro/inputs/
├── analysis_report/latest.json
├── analysis_verdict/latest.json
└── vision_context/coinglass/latest.json
```

### 2.2 Paths references par les readers

| Reader | Path reference | Fichier existant |
|---|---|---|
| market_metrics_reader.py | deskpro/inputs/market_metrics/latest.json | NON (fallback) |
| vision_analysis_reader.py | deskpro/inputs/vision_analysis/latest.json | NON |
| vision_context_reader.py | deskpro/inputs/vision_context/coinglass/latest.json | OUI |
| vision_context_reader.py | deskpro/inputs/vision_context/news_sentiment/latest.json | NON |
| vision_context_reader.py | deskpro/inputs/vision_context/screener/latest.json | NON |
| telegram_claim_reader.py | deskpro/inputs/telegram_claim/latest.json | NON |
| vision_panel.py | deskpro/inputs/vision_context/coinglass/latest.json | OUI |
| vision_panel.py | deskpro/inputs/vision_context/news_sentiment/latest.json | NON |
| vision_panel.py | deskpro/inputs/vision_context/screener/latest.json | NON |
| vision_panel.py | deskpro/inputs/telegram_claim/latest.json | NON |

## 3. Bilan paths

```text
VIEWS DC EXISTANTES      : market_metrics (latest + by_symbol), vision_analysis (by_symbol)
VIEWS DC MANQUANTES      : pair_market_snapshot, vision_context (x3)
VIEWS NON DOCUMENTEES    : analysis, coinglass/squeeze_alerts, data_center_coverage, telegram_*
LEGACY FICHIERS PRESENTS : 2 (coinglass/latest.json, analysis_report/latest.json, analysis_verdict/latest.json)
LEGACY FICHIERS ABSENTS  : 6 (vision_analysis, news_sentiment, screener, telegram_claim, market_metrics)
READERS LEGACY REFERENCES: 10 paths — 2 fichiers existent, 8 absents
```

## 4. Anomalies

| ID | Gravite | Description |
|---|---|---|
| D01 | HIGH | `pair_market_snapshot/` view directory absente — consumer desk_pro lit un path inexistant |
| D02 | HIGH | 6 readers referencent des paths legacy dont les fichiers n'existent pas |
| D03 | HIGH | 7 views directories non references dans consumers.json (usage inconnu) |
| D04 | MEDIUM | `vision_analysis/history/` reference par dashboards mais directory absent (seul by_symbol/ existe) |
| D05 | MEDIUM | `data/deskpro/inputs/` contient 3 fichiers legacy mais 2 ne sont pas references par des consumers (analysis_report, analysis_verdict) |
| D06 | LOW | Le seul fichier legacy existant reference par un consumer est coinglass/latest.json |
