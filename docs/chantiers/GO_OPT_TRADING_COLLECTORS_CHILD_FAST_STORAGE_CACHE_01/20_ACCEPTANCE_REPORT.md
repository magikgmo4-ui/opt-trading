---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01_ACCEPTANCE_REPORT
doc_type: acceptance_report
repo: opt-trading
project: opt-trading
module: derivatives_collector
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: closed
lifecycle_stage: accepted
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

## Verdict

**ACCEPTED** — Toutes les fonctions de publication `market_metrics.v1` livrées et testées.

---

## Fichiers créés

| Fichier | Rôle |
|---|---|
| `modules/derivatives_collector/app/market_metrics_writer.py` | Trois fonctions de publication |
| `modules/derivatives_collector/tests/test_market_metrics_writer.py` | Suite unittest (25 tests) |
| `docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01/00_INITIAL_PROJECT_DOC.md` | Cahier des charges |
| `docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01/20_ACCEPTANCE_REPORT.md` | Ce rapport |
| `docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01/90_REPRISE_POINT.md` | Point de reprise |
| `docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01.md` | Entrée index inbox |

---

## Fonctions livrées

| Fonction | Chemin cible | Comportement not_proven |
|---|---|---|
| `write_market_metrics_latest` | `data/collectors/derivatives/latest.json` | `None` (skip) |
| `write_market_metrics_by_symbol` | `data/collectors/derivatives/cache/by_symbol/<SYMBOL>.json` | `None` (skip) |
| `publish_market_metrics_for_deskpro` | `data/deskpro/inputs/market_metrics/{latest,by_symbol/<SYMBOL>}.json` | `None` (skip) |

---

## Contrat

- Accepte `MarketMetricsV1` (dataclass) ou `dict` brut.
- Lève `ValueError` si `input_class != "market_metrics.v1"`.
- Retourne `None` sans écrire si `provider_coverage.status == "not_proven_runtime_adapter"`.
- Crée les répertoires manquants automatiquement (atomic write via `tempfile`).
- Conserve les `null` pour les métriques absentes — aucune synthèse.
- N'efface pas les exports legacy derivatives JSON/CSV.

---

## Tests livrés

| Suite | Fichier | Tests | Status |
|---|---|---|---|
| `TestWriteMarketMetricsLatest` | `test_market_metrics_writer.py` | 9 | OK |
| `TestWriteMarketMetricsBySymbol` | `test_market_metrics_writer.py` | 7 | OK |
| `TestPublishMarketMetricsForDeskpro` | `test_market_metrics_writer.py` | 9 | OK |
| **Total writer** | | **25** | **OK** |
| Desk Pro reader (existant) | `test_desk_pro_market_metrics_reader.py` | 22 | OK |

---

## Couverture des critères GO

| Critère | Status |
|---|---|
| écrit latest.json | PASS |
| écrit by_symbol/BTCUSDT.json | PASS |
| crée les dossiers manquants | PASS |
| refuse input_class incorrect | PASS |
| conserve null pour métriques absentes | PASS |
| n'écrit pas Coinglass (not_proven_runtime_adapter) | PASS |
| Desk Pro reader peut relire le latest publié | PASS |

---

## Contraintes respectées

- Aucun appel API externe (Binance, Bitget, Coinglass).
- Aucune écriture DB, Sheets, Telegram.
- Exports legacy derivatives JSON/CSV non modifiés.
- Coinglass Vision non modifié.

---

## Gaps résiduels — hors scope accepté

| Gap | Raison | Action future |
|---|---|---|
| Intégration dans `lifecycle_compat.py` | Non prioritaire — writer produit indépendant | Child futur GO |
| Ingestion DB `market_metrics` | Non prioritaire | Child futur GO |
| Stratégie multi-provider (merge BTCUSDT binance + bitget) | Complexité hors scope | Child futur GO |
