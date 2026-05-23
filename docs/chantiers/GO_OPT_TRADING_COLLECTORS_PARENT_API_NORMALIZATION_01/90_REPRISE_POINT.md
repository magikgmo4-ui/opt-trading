---
doc_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 90_REPRISE_POINT

## 7_CANONICAL_STATE

Chantier parent ouvert pour normaliser les collectors API vers une consommation Desk Pro et multi-surfaces.

Etat courant :

- le master target est fige dans `00_INITIAL_PROJECT_DOC.md` ;
- l'etat repo et les gaps sont documentes dans `10_REPO_STATE_AND_GAPS.md` ;
- le contrat cible `market_metrics.v1` est documente dans `20_MARKET_METRICS_V1_CONTRACT.md` ;
- le stockage normalise et le chemin d'ingestion future sont documentes dans `30_STORAGE_AND_INGESTION_PLAN.md` ;
- le plan de tests et reporting est documente dans `40_TEST_AND_REPORTING_PLAN.md`.

## 13_ESTABLISHED

- Bitget est dans le scope.
- Bitget est reel comme adapter derivatives, mais partiel.
- Les metrics manquantes doivent etre explicites, jamais simulees.
- Desk Pro doit recevoir `market_metrics.v1` en read-only.
- Les surfaces Sheets/Telegram/Perf restent consommateurs futurs, pas writes dans ce chantier parent.

## 14_HYPOTHESIS

La premiere implementation utile est un child GO qui produit le rapport de couverture provider/metric et valide un schema `market_metrics.v1` sur fixtures.

## 15_REMAINING_GAP

- adapter Coinglass non prouve ;
- cache by-symbol non cree ;
- Desk Pro consumer read-only absent ;
- tests smoke absents ;
- rapport coverage absent.

## 16_TODO

1. Ouvrir `GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01`.
2. Ajouter fixtures Bitget/Binance/mock.
3. Produire `provider_metric_coverage_latest.json`.
4. Ajouter spec/test `market_metrics.v1`.
5. Ouvrir ensuite le child Desk Pro read-only consumer.

## 17_RESUME_POINT

Reprise operationnelle : commencer par `GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01` sur une branche child dediee.

## 18_TO_DOCUMENT

- `10_PROVIDER_COVERAGE_REPORT.md`
- `20_FIXTURE_MATRIX.md`
- `30_MARKET_METRICS_SCHEMA_TESTS.md`
- `40_NEXT_PATCHES.md`

## 19_TO_REMEMBER

### MEM_CANDIDATE

- `[Collectors API normalization parent]` : chantier parent cree pour normaliser collectors API vers `market_metrics.v1`, stockage rapide, Desk Pro read-only et consommation future Sheets/Telegram/Perf.
- `[Bitget collector gap]` : Bitget existe dans `derivatives_collector`, mais seulement OI/funding/volume futures sont prouves ; L/S ratio et liquidations restent gaps.

### SAVE_MEMORY

- Aucun enregistrement automatique ; a valider manuellement si ce chantier devient doctrine durable.
