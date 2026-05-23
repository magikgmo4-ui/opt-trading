---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
topic_keys:
  - opt-trading
  - collectors
  - provider_coverage
  - market_metrics
  - fixtures
links:
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/10_REPO_STATE_AND_GAPS.md
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/20_MARKET_METRICS_V1_CONTRACT.md
  - docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01.md
---

# GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Produire le rapport de couverture provider/metric pour les collectors API avant toute implementation runtime ou consommateur Desk Pro.

## 2_PARENT_CONTEXT

Child de `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01`. Le parent a etabli :

- L'etat reel des collectors (10_REPO_STATE_AND_GAPS)
- Le contrat `market_metrics.v1` (20_MARKET_METRICS_V1_CONTRACT)
- Les gaps majeurs : Bitget partial, Coinglass non prouve, cache by_symbol absent

Ce child cible **la preuve documentaire de couverture**, pas l'implementation.

## 3_INITIAL_NEED

Avant de toucher au runtime ou a Desk Pro, il faut figer :

1. Ce que chaque provider peut reellement fournir (vs ce que la dataclass declare).
2. Les metriques prouvees vs manquantes, par provider et par symbole.
3. Les fixtures qui representent des reponses API reelles ou realistes.
4. La validation du schema `market_metrics.v1` contre ces fixtures.
5. La decision sur le prochain patch (schema/fixtures vs consumer Desk Pro).

## 4_SCOPE

### Autorise

- Docs uniquement : rapports, matrices, schema tests en markdown
- Fixtures decrites (pas de code Python execute)
- Rapport `provider_metric_coverage_latest.json` structure
- Criteres PASS/BLOCKED/PARTIAL par provider

### Interdit

- Runtime modifie
- Appel API externe
- DB write, Sheets, Telegram
- Index globaux modifies
- Simulation de donnees manquantes (liquidations, long_short_ratio inventes)

## 5_DELIVERABLES

| Fichier | Role |
|---|---|
| `10_PROVIDER_COVERAGE_REPORT.md` | Rapport provider par provider : metriques prouvees/manquantes |
| `20_FIXTURE_MATRIX.md` | Matrice fixtures : reponses API attendues par provider/endpoint |
| `30_MARKET_METRICS_SCHEMA_TESTS.md` | Tests schema `market_metrics.v1` contre les fixtures |
| `40_NEXT_PATCHES.md` | Decision prochaine etape : schema/fixtures vs Desk Pro consumer |
| `BRANCH_STATE.md` | Etat de la branche, stacking info, prochaines actions |

## 6_INVARIANTS

- Bitget = partial coverage : open_interest, funding_rate, volume_futures prouves ; long_short_ratio et liquidations NON prouves.
- Binance derivatives = partial coverage : open_interest, funding_rate, volume_futures, long_short_ratio prouves ; liquidations non prouvees.
- Coinglass = not_proven_runtime_adapter sauf preuve d'adapter reel dans le repo.
- Binance spot, CoinGecko = couverture spot uniquement, hors scope derivatives.
- Metrique non prouvee reste `null` dans le payload + declaree dans `missing_metrics`.
- Aucune metrique n'est inventee ou synthetisee.

## 7_BRANCH_STATE

- Base : `go/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01` (PR #663, OPEN)
- Head : `go/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01`
- PR cible : base = parent branch ; ne pas baser sur `sot/mainline` avant merge de #663
- Apres merge #663 : retarget ou rebase du child vers `sot/mainline`
