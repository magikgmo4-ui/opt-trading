---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01_ACCEPTANCE_REPORT
doc_type: acceptance_report
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

## Bloc fermé

```text
MARKET_METRICS_CONSUMER_DECOUPLING_BLOCK_01
```

## Tests au merge de #761

| Suite | Résultat |
|---|---|
| `modules/data_center/tests/test_contract_tests.py` | **36/36 PASS** |
| `modules/derivatives_collector/tests/test_market_metrics_writer.py` | **59/59 PASS** |
| `tests/test_desk_pro_market_metrics_reader.py` | **28/28 PASS** |
| `modules/data_center/tests/test_layout.py` | **12/12 PASS** |
| `bash modules/data_center/scripts/sanity_check.sh` | **PASS** |
| `git diff --check` | **CLEAN** |
| **Total** | **135/135 PASS** |

---

## Critère 1 — Access patterns couverts

| access_pattern | Vue neutre | Test invariant | Statut |
|---|---|---|---|
| `latest_only` | `views/market_metrics/latest.json` | `test_latest_only_consumers_read_from_view` | **PASS** |
| `by_symbol` | `views/market_metrics/by_symbol/<SYMBOL>.json` | `test_by_symbol_consumers_read_from_view` | **PASS** |
| `full_history` | `views/market_metrics/history/` | `test_full_history_consumers_read_from_view` | **PASS** |

**Verdict** : 3/3 access patterns couverts.

---

## Critère 2 — Consumers non implémentés restent `not_started`

| Consumer | access_pattern | Reader réel | Statut |
|---|---|---|---|
| `telegram_screener__signal_context` | `latest_only` | Aucun | `not_started` ✓ |
| `google_sheets__market_reporting` | `latest_only` | Aucun | `not_started` ✓ |
| `strategy_framework__market_context` | `by_symbol` | Aucun | `not_started` ✓ |
| `perf_engine__replay_context` | `full_history` | Aucun | `not_started` ✓ |
| `localcms__data_center_health` | `status_only` | Aucun | `not_started` ✓ |

Test invariant : `test_not_implemented_consumers_remain_not_started` couvre les 4 consumers `market_metrics.v1`.

**Verdict** : Aucun reader fantôme créé. Invariant verrouillé.

---

## Critère 3 — Desk Pro est le seul consumer runtime réel migré

| Consumer | Surface | Status | Lecture réelle prouvée |
|---|---|---|---|
| `desk_pro__market_metrics` | `PF_DESK_PRO` | `implemented` | OUI — `market_metrics_reader.py` lit `views/market_metrics/latest.json` avec fallback `data/deskpro/inputs/market_metrics/latest.json` |

28 tests `tests/test_desk_pro_market_metrics_reader.py` couvrent le chemin primaire, le fallback legacy, et la dégradation gracieuse.

**Verdict** : 1 consumer runtime réel — Desk Pro. Migré et verrouillé.

---

## Critère 4 — Producer paths restent source/audit

| Producer | output_path_root | Rôle |
|---|---|---|
| `derivatives_collector__bitget` | `data/data_center/derivatives/derivatives_collector__bitget/` | écriture producteur / audit |
| `derivatives_collector__binance` | `data/data_center/derivatives/derivatives_collector__binance/` | écriture producteur / audit |

Aucun consumer `market_metrics.v1` ne lit directement ces paths.

Test invariant :
- `test_latest_only_consumers_have_no_producer_id_in_path`
- `test_by_symbol_consumers_have_no_producer_id_in_path`
- `test_full_history_consumers_have_no_producer_id_in_path`
- `test_desk_pro_reads_from_contract_class_view`

**Verdict** : producer paths = write-only pour les producers, read-only pour l'audit. Invariant verrouillé.

---

## Critère 5 — Views sont les surfaces consumer

| Vue | Chemin | Alimentée par | Consommée par |
|---|---|---|---|
| `latest` | `views/market_metrics/latest.json` | bitget, binance | desk_pro, telegram*, sheets* |
| `by_symbol` | `views/market_metrics/by_symbol/<SYMBOL>.json` | bitget, binance | strategy_framework* |
| `history` | `views/market_metrics/history/<SYMBOL>/<run_id>.json` | bitget, binance | perf_engine* |

`*` = not_started, path déclaré correct dans registry.

Writer functions dans `market_metrics_writer.py` :
- `write_market_metrics_view()` → latest + by_symbol
- `write_market_metrics_history_view()` → history/<SYMBOL>/<run_id>
- `publish_market_metrics()` → pipeline complet

**Verdict** : toutes les views existent, sont écrites, et les consumers lisent uniquement depuis views/.

---

## Règle finale

```text
Aucun consumer market_metrics.v1 ne lit un producer_id path.
```

Vérifiée sur les 3 access patterns, les 6 consumers `market_metrics.v1`, et les 2 producers actifs.

---

## Verdict du bloc

**ACCEPTED — CLOSED**

```text
MARKET_METRICS_CONSUMER_DECOUPLING_BLOCK_01 : ACCEPTED / CLOSED
PF_DATA_CENTER : OPEN
GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01 : OPEN
```
