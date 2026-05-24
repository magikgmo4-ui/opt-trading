---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PARENT_ACCEPTANCE_REVIEW_01_ACCEPTANCE_REVIEW
doc_type: acceptance_review
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PARENT_ACCEPTANCE_REVIEW_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_PARENT_ACCEPTANCE_REVIEW

## Verdict global

```text
GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01 : ACCEPTED / CLOSABLE
CLOSE_GATE_MASTER_TARGET                  : ATTEINT
PF_DATA_CENTER                            : OPEN
```

---

## Vérification critères CLOSE_GATE_MASTER_TARGET

Source : `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md` § `CLOSE_GATE_MASTER_TARGET`.

### Critère 1 — ≥2 surfaces consommatrices lisant depuis data/data_center/

| Surface | Consumer | Reader | Preuve |
|---|---|---|---|
| `PF_DESK_PRO` | `desk_pro__market_metrics` | `modules/desk_pro/service/market_metrics_reader.py` | 28 tests PASS — PR #753 |
| `PF_LOCALCMS_COCKPIT` | `localcms__data_center_health` | `modules/data_center/localcms_health_reader.py` | 10 tests PASS — PR #768 |

**Verdict : ATTEINT** — 2/2 surfaces consommatrices avec lecture prouvée.

---

### Critère 2 — ≥2 producers avec contrats formalisés, schémas versionnés, testés

| Producer | Contrat | Schema | Tests | Statut |
|---|---|---|---|---|
| `derivatives_collector__bitget` | `market_metrics.v1` | `schema_version: v1` | `test_bitget_is_full_6_of_6` | **PASS** |
| `derivatives_collector__binance` | `market_metrics.v1` | `schema_version: v1` | `test_binance_is_full_6_of_6` | **PASS** |
| `collector_binance_spot` | `pair_market_snapshot.v1` | `schema_version: v1` | `test_pair_snapshot_consumers_read_from_view` | **PASS** |

Note : `last_write: null` sur bitget et binance — runs prod non encore confirmés. Ce gap est documenté (GAP-P03, GAP-P04) et non bloquant pour le critère formel (contrats formalisés et testés).

**Verdict : ATTEINT** — 2/2 producers requis (bitget + binance, market_metrics.v1 complet à 6/6 métriques).

---

### Critère 3 — ≥2 consumers avec lecture prouvée depuis data/data_center/

| Consumer | access_pattern | Preuve | PR |
|---|---|---|---|
| `desk_pro__market_metrics` | `latest_only` | `test_consumer_read_path_reachable_via_view_writer` + 28 tests reader | #753 |
| `localcms__data_center_health` | `status_only` | `test_localcms_is_in_implemented_consumers` + `test_at_least_two_consumers_implemented` | #768 |

**Verdict : ATTEINT** — 2/2 consumers avec lecture prouvée.

---

### Critère 4 — Tests contractuels smoke passant

| Suite | Tests | Résultat |
|---|---|---|
| `modules/data_center/tests/test_contract_tests.py` | 44 | **44/44 PASS** |
| `modules/data_center/tests/test_localcms_health_reader.py` | 10 | **10/10 PASS** |
| `modules/data_center/tests/test_pair_snapshot_view_writer.py` | 10 | **10/10 PASS** |
| `modules/data_center/tests/test_layout.py` | 14 | **14/14 PASS** |
| `modules/derivatives_collector/tests/test_market_metrics_writer.py` | 59 | **59/59 PASS** |
| `tests/test_desk_pro_market_metrics_reader.py` | 28 | **28/28 PASS** |
| `bash modules/data_center/scripts/sanity_check.sh` | — | **PASS** (consumers implemented: 2) |
| **Total** | **162** | **162/162 PASS** |

**Verdict : ATTEINT** — 162/162 tests PASS.

---

### Critère 5 — Documentation reprise par consumer actif

| Consumer | Documentation | Localisation |
|---|---|---|
| `desk_pro__market_metrics` | Complet — migration, fallback, tests | PR #753, `90_REPRISE_POINT.md` de chaque child GO |
| `localcms__data_center_health` | Complet — reader, endpoint, tests | PR #768, `GO_OPT_TRADING_DATA_CENTER_CHILD_LOCALCMS_HEALTH_READER_01/90_REPRISE_POINT.md` |
| `desk_pro__spot_snapshot` | `not_started` — path corrigé | PR #766 |
| `strategy_framework__market_context` | `not_started` — documenté | `30_REMAINING_GAPS_AND_NEXT_GO.md` (#763) |
| `perf_engine__replay_context` | `not_started` — documenté | `30_REMAINING_GAPS_AND_NEXT_GO.md` (#763) |
| `telegram_screener__signal_context` | `not_started` — documenté | `30_REMAINING_GAPS_AND_NEXT_GO.md` (#763) |
| `google_sheets__market_reporting` | `not_started` — documenté | `30_REMAINING_GAPS_AND_NEXT_GO.md` (#763) |

**Verdict : ATTEINT** — tous les consumers actifs documentés ; les `not_started` explicitement listés comme NEXT_GO.

---

### Critère 6 — Aucun gap bloquant non documenté

Tous les gaps connus sont inventoriés dans :
- `GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01/30_REMAINING_GAPS_AND_NEXT_GO.md`
- `GO_OPT_TRADING_DATA_CENTER_CHILD_PARENT_ACCEPTANCE_REVIEW_01/30_REMAINING_GAPS_AND_NEXT_GO.md` (ce GO)

**Verdict : ATTEINT** — aucun gap bloquant non documenté.

---

## Règle canonique — état verrouillé

```text
data/data_center/<family>/<producer_id>/     = écriture producteur / audit
data/data_center/views/<contract_class>/     = lecture consommateur
data/data_center/_registry/                  = status / registry / health
```

Vérification : 100% des tests `test_no_consumer_reads_from_raw`, `test_*_consumers_have_no_producer_id_in_path`,
`test_*_consumers_read_from_view` — tous PASS.

---

## Récapitulatif state registry post-#768

### Producers

| Producer | Contrat | Coverage | last_write |
|---|---|---|---|
| `derivatives_collector__bitget` | `market_metrics.v1` | full (6/6) | null |
| `derivatives_collector__binance` | `market_metrics.v1` | full (6/6) | null |
| `collector_binance_spot` | `pair_market_snapshot.v1` | full | null |

### Consumers

| Consumer | Contrat | access_pattern | Status |
|---|---|---|---|
| `desk_pro__market_metrics` | `market_metrics.v1` | `latest_only` | **implemented** |
| `localcms__data_center_health` | null | `status_only` | **implemented** |
| `desk_pro__spot_snapshot` | `pair_market_snapshot.v1` | `latest_only` | not_started |
| `strategy_framework__market_context` | `market_metrics.v1` | `by_symbol` | not_started |
| `perf_engine__replay_context` | `market_metrics.v1` | `full_history` | not_started |
| `telegram_screener__signal_context` | `market_metrics.v1` | `latest_only` | not_started |
| `google_sheets__market_reporting` | `market_metrics.v1` | `latest_only` | not_started |

---

## Verdict final

| Critère | Statut |
|---|---|
| ≥2 surfaces consommatrices lisant data/data_center/ | **ATTEINT** |
| ≥2 producers formalisés/testés | **ATTEINT** |
| ≥2 consumers avec lecture prouvée | **ATTEINT** |
| Tests contractuels smoke PASS | **ATTEINT** |
| Documentation reprise par consumer actif | **ATTEINT** |
| Aucun gap bloquant non documenté | **ATTEINT** |

```text
CLOSE_GATE_MASTER_TARGET : ATTEINT (6/6 critères)
GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01 : ACCEPTED / CLOSABLE
PF_DATA_CENTER : OPEN
```

Le parent peut être fermé. `PF_DATA_CENTER` reste OPEN pour accueillir de nouveaux producers,
consumers et contrats.
