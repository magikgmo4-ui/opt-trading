---
go_id: GO_OPT_TRADING_UI_DUAL_SURFACE_LIVE_DATA_BRIDGE_01
doc_type: live_data_audit
repo: opt-trading
status: DRAFT
created_at: 2026-05-18
---

# GO_OPT_TRADING_UI_DUAL_SURFACE_LIVE_DATA_BRIDGE_01

## 1_MASTER_TARGET

Passer Desk Pro UI du mode `step2_mock` vers une source de données réelle ou fixture contrôlée, sans casser l'état PASS existant.

## 3_INITIAL_NEED

Le socle UI Desk Pro est validé (GO_OPT_TRADING_UI_DUAL_SURFACE_USAGE_TEST_01) mais toutes les données sont mock. Les endpoints perf sont déjà live avec SQLite mais vides. Le gap est : seed des données + bridge desk snapshot.

## 5_AUDIT — DATA SOURCE CLASSIFICATION

### Desk Pro endpoints

| Endpoint | Source actuelle | Type | Stockage | Accepte data live |
|---|---|---|---|---|
| `GET /desk/health` | dict hardcodé `routes.py:29` | MOCK | Aucun | Non |
| `GET /desk/snapshot` | `build_snapshot_mock()` `aggregator.py:8-14` | MOCK (2 metrics placeholder) | Aucun | Non |
| `POST /desk/form` | `build_snapshot_mock()` + `compute_probability()` stub | MOCK | Aucun | Non (user-provided form) |
| `GET /desk/ui` | HTML statique `page.py` | STATIC | Aucun | Non |
| `GET /desk/toolbox` | HTML statique `routes.py:71-204` | STATIC | Aucun | Non |

### Perf endpoints (already LIVE)

| Endpoint | Source | Type | Stockage | Accepte data live |
|---|---|---|---|---|
| `GET /perf/summary` | SQLite `trades` table | LIVE | `perf.db` | Oui (via `POST /perf/event`) |
| `GET /perf/equity` | SQLite `trades` table | LIVE | `perf.db` | Oui |
| `GET /perf/open` | SQLite `trades` table | LIVE | `perf.db` | Oui |
| `GET /perf/trades` | SQLite `trades` table | LIVE | `perf.db` | Oui |
| `POST /perf/event` | Écrit dans SQLite events + trades | LIVE (ingestion) | `perf.db` | Oui — point d'entrée |

### Chaînes d'ingestion live existantes

| Source | Cible | État |
|---|---|---|
| `webhook_server.py` → `POST /perf/event` | Perf SQLite | LIVE mais nécessite TradingView alerts actifs |
| `simex_bitget_bridge.py` → `POST /perf/event` | Perf SQLite | LIVE mais nécessite API Bitget + clés |
| `adapters/webhook_to_perf.py` | Conversion webhook → PerfEvent | PRÊT |

### Fixtures existantes

| Fichier | Utilité |
|---|---|
| `modules/perf_engine/config/sample_positions.json` | 3 positions sample (BTCUSDT, ETHUSDT, SOLUSDT) |
| `modules/perf_engine/config/sample_execution.json` | Execution states sample |
| `data/journal/daily/20260518_001.json` | Pipeline dry-run trace complète (317 lines) |
| `data/journal/daily/20260518_001.csv` | Pipeline dry-run summary |

## 7_CANONICAL_STATE

- Desk Pro UI endpoints : MOCK (step2_mock)
- Perf endpoints : LIVE (SQLite, vide)
- Chaîne d'ingestion webhook → perf : PRÊTE (nécessite source externe)
- Fixtures disponibles : perf_engine sample + pipeline journal
- unittest : 92/92 PASS
- secrets/ non inclus

## 13_ESTABLISHED

| Fait | Preuve |
|---|---|
| Perf SQLite engine est opérationnel | `perf_app.py:54-99` — init DB, tables events + trades |
| `POST /perf/event` accepte et persiste des events | `perf_app.py:385-403` |
| Aucune donnée dans perf.db actuellement | 0 events, 0 trades |
| Desk Pro snapshot est hardcodé mock | `aggregator.py:8-14` — 2 metrics BTC/DXY placeholders |
| Aucune fixture pour Desk Pro snapshot | Aucun fichier JSON chargé dans aggregator |
| Pipeline journal contient des données exploitables | `data/journal/daily/20260518_001.json` |

## 14_HYPOTHESIS

| Hypothèse | Preuve nécessaire |
|---|---|
| Seeding perf.db avec fixtures est suffisant pour rendre Perf UI utilitaire | Lancer seed + ouvrir `/perf/ui` |
| Desk Pro snapshot peut être enrichi via les trades perf.db | Analyser si trades → snapshot market metrics |
| Pipeline journal peut être converti en fixture perf | Écrire un script de replay |

## 15_REMAINING_GAP

| Gap | Criticité | Action |
|---|---|---|
| `perf.db` vide — Perf UI montre zéro trades | haute | Seed fixture trades dans perf.db |
| Desk Pro snapshot purement mock | haute | Créer fixture snapshot JSON ou bridge trades → snapshot |
| Aucun mécanisme pour basculer mock ↔ fixture | moyenne | Ajouter query param `?source=mock\|fixture\|live` |
| Pipeline journal non exploité comme fixture | basse | Script de replay si pertinent |

## 16_TODO — PLAN DE BRIDGE MINIMAL

### Étape 1 : Seed perf.db avec fixtures contrôlées

Créer un script `scripts/seed_perf_fixture.py` qui POSTe des trades simulés vers `/perf/event` :

- 5-10 trades OPEN/CLOSE sur BTCUSDT, ETHUSDT
- Entrées/sorties réalistes
- Permet de voir des données dans `/perf/ui`, `/perf/summary`, `/perf/equity`

### Étape 2 : Créer fixture snapshot Desk Pro

Créer `data/desk_snapshot_fixture.json` avec metrics complètes (prix, tendances, volume) pour remplacer les placeholders BTC/DXY.

### Étape 3 : Modifier `aggregator.py`

- `build_snapshot_mock()` conservé comme fallback
- Ajouter `build_snapshot_from_fixture()` lisant `data/desk_snapshot_fixture.json`
- Ajouter `build_snapshot_from_perf()` lisant les trades perf.db
- Query param `?source=mock|fixture|live` optionnel

### Étape 4 : Tester

- `python3 -m unittest discover -s tests -p "test_*.py"` → 92/92
- Smoke perf avec fixtures seedées
- Smoke desk snapshot non mock

## 17_RESUME_POINT

```text
Audit data sources terminé.
Perf endpoints sont LIVE sur SQLite mais vides.
Desk Pro endpoints sont MOCK (step2_mock).
Fixtures disponibles (perf_engine samples, pipeline journal).
Bridge minimal = seed perf.db + fixture snapshot desk.
Prochaine action : seed perf.db avec trades simulés.
```
