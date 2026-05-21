---
doc_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
topic_keys:
  - opt-trading
  - collectors
  - api_collectors
  - market_metrics
  - desk_pro
  - data_ingestion
  - normalized_storage
  - consumption_surfaces
links:
  - docs/COLLECTORS_FAMILY_DOCTRINE_01.md
  - docs/COLLECTORS_MIGRATION_MAP_01.md
  - docs/COLLECTORS_BASELINE_GAP_MATRIX_01.md
  - docs/COLLECTORS_LIFECYCLE_COMPAT_SPEC_01.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/20_TARGET_INPUT_CLASSES.md
  - docs/db_layer_desk_pro_runbook.md
  - docs/index/inbox/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01.md
---

# GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Collector API normalisation : combler les gaps des collectors API, tester et produire un rapport des donnees collectables, normaliser le stockage pour ingestion Desk Pro et reutilisation rapide par les differentes surfaces de consommation.

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche de reference initiale du chantier parent. Il fige la demande de depart et le plan initial. Il ne doit pas etre remplace par les sous-GO d'implementation.

## 3_INITIAL_NEED

La demande initiale est de documenter entierement l'etat des collectors de donnees via API dans le repo, leur etat, l'ingestion prevue par Desk Pro, les gaps, et la facon de stocker les donnees pour reutilisation rapide dans les surfaces consommatrices.

Extension explicite utilisateur : creer le chantier avec le master target suivant : collector API normalisation ; combler les gaps ; tester et rapporter les donnees collectables ; normaliser le stockage pour ingestion Desk Pro et reutilisation par les differentes surfaces.

## 4_MASTER_PROJECT_PLAN

1. Figer l'etat reel des collectors API presents dans le repo.
2. Identifier les providers et leurs donnees collectables : derivatives, Bitget, Binance derivatives, Binance spot, CoinGecko, Coinglass si prouve.
3. Distinguer les providers reels des placeholders ou gaps.
4. Definir le contrat `market_metrics.v1` comme sortie normalisee pour Desk Pro.
5. Definir le stockage rapide : raw, normalized, latest, manifest, status, events, errors, cache by-symbol.
6. Preparar l'ingestion Desk Pro en read-only avant toute ecriture DB, Sheets ou Telegram.
7. Ajouter des tests smoke et un rapport de couverture provider/metric.
8. Ouvrir ensuite les sous-GO d'implementation bornes.

## 5_GO_PLAN

Chantier parent doc-first. Sous-GO proposes :

- `GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01`
- `GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01`
- `GO_OPT_TRADING_COLLECTORS_CHILD_DESKPRO_READONLY_CONSUMER_01`
- `GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01`
- `GO_OPT_TRADING_COLLECTORS_CHILD_TEST_REPORTING_MATRIX_01`

## 6_FINAL_TARGET

Livrable cible : une chaine coherente et testee :

```text
API providers
  -> collectors raw captures
  -> normalized collector outputs
  -> market_metrics.v1
  -> latest + by_symbol cache
  -> Desk Pro read-only input
  -> consommation future par Sheets / Telegram / Perf / replay / paper
```

## 7_CANONICAL_STATE

- `derivatives_collector` est le collector derivatives canonique.
- `collector_coingecko` et `collector_binance_spot` sont des providers spot valides sur `collectors_core`.
- Bitget existe via `modules/derivatives_collector/app/bitget_adapter.py`, mais sa couverture metrics est partielle.
- Desk Pro dispose deja d'une taxonomie d'inputs cible incluant `market_metrics.v1`.
- L'ingestion DB de Desk Pro n'est pas encore implementee ; le repo documente seulement une surface source minimale `/shared/desk_pro/latest/` pour ingestion future.

## 8_VALIDATED_PLAN

Plan valide pour cette ouverture : documenter d'abord, ne pas modifier runtime, ne pas ecrire dans les index globaux, ne pas brancher Sheets/Telegram/DB, et creer une entree inbox locale de decouverte.

## 9_SELECTED_SOLUTION

Adopter `market_metrics.v1` comme contrat de jonction entre collectors et Desk Pro. Le contrat doit rester provider-aware et accepter explicitement les metriques absentes par `null` + coverage/gap, jamais par simulation.

## 10_SELECTED_SETUP

Stockage propose :

```text
data/collectors/<family_or_provider>/
  raw/
  normalized/
  latest.json
  manifest.json
  status.json
  events.jsonl
  errors.jsonl
  cache/by_symbol/<SYMBOL>.json

data/deskpro/inputs/market_metrics/
  latest.json
  by_symbol/<SYMBOL>.json
```

## 11_KEY_DECISIONS

- Le chantier est parent documentaire.
- Aucun runtime n'est modifie a l'ouverture.
- `market_metrics.v1` est le pont cible Desk Pro.
- Les gaps provider doivent etre visibles et testes.
- Les exports legacy JSON/CSV derivatives restent valides.

## 12_INVARIANTS

- Aucun ordre live.
- Aucune ecriture Google Sheets globale.
- Aucun Telegram live.
- Aucune ingestion DB active.
- Aucun refactor force de `derivatives_collector` vers `collectors_core`.
- Aucune fausse unification spot/derivatives.

## 13_ESTABLISHED

Le repo prouve deja une doctrine collector family, une migration map, une gap matrix, une compat lifecycle pour derivatives, des providers spot sur `collectors_core`, et une taxonomie Desk Pro qui prevoit `market_metrics.v1`.

## 14_HYPOTHESIS

A valider par tests : l'artefact `market_metrics.v1` peut etre produit depuis `derivatives_collector/lifecycle_compat.py` sans casser les exports existants, puis consomme par Desk Pro en read-only.

## 15_REMAINING_GAP

- Couverture Bitget incomplete : pas de liquidations ni long/short ratio dans l'adapter lu.
- Coinglass non prouve comme adapter runtime.
- Cache by-symbol non standardise.
- Desk Pro consumer `market_metrics.v1` non materialise.
- Rapport collectable/non-collectable provider par provider a produire.

## 16_TODO

1. Produire la matrice provider/metric.
2. Specifier `market_metrics.v1`.
3. Definir le stockage rapide normalise.
4. Ajouter un plan de tests smoke.
5. Ouvrir le premier child GO d'implementation.

## 17_RESUME_POINT

Reprendre depuis `90_REPRISE_POINT.md`, puis executer le child `GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01`.
