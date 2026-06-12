# 90_REPRISE_POINT — GO_SPACEX_SUPER_DESK_PARENT_01

## 7_CANONICAL_STATE

SpaceX/SPCX est prioritaire. Bundle V2 apporte une base exécutable et intégrée au repo zip fourni.

## 13_ESTABLISHED

- Repo contient Data Center, Desk Pro, Bot Vision, Telegram Screener, Google Sheets Global Schema, Perf/Webhook, Coinglass OCR/vision surfaces.
- Les modules ajoutés restent monitor-only.
- L'implémentation écrit dans `data/ipo/spacex` et `data/data_center/views/spacex_super_desk`.

## 14_HYPOTHESIS

- Les données SPCX live peuvent être indisponibles au premier run si ticker non actif côté provider.
- Coinglass est surtout un contexte de régime/risque, pas une source directe equity.
- TradingView/Bot Vision donneront la meilleure couverture technique initiale.

## 15_REMAINING_GAP

- Webhook TradingView réel à configurer côté TradingView.
- Bot Vision profile à intégrer au scheduler existant.
- Sheets/Telegram réels selon rôles credentials.
- Route Desk Pro native à coder après validation dry-run.

## 16_TODO

```bash
bash scripts/ipo/spacex_collect_once.sh
bash scripts/ipo/spacex_report_daily.sh
python3 -m modules.ipo_tracking.cli smoke
```

Puis ouvrir child : `GO_SPACEX_DESK_PRO_NATIVE_ROUTE_CHILD_01`.
