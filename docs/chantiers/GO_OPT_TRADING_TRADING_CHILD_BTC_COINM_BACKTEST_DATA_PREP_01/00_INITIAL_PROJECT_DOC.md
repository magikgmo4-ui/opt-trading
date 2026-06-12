---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01
status: draft_for_user_validation
lifecycle_stage: child_opening_plan
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01
topic_keys:
  - opt-trading
  - trading
  - bitcoin
  - btc
  - bitget
  - coin-futures
  - backtest
  - data-prep
  - historical-data
  - candles
  - funding-history
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Préparer le pipeline de données historiques pour le backtest BTC COIN-M, sans exécuter le backtest ni connecter l'exchange."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/01_formulas_source_lock.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/02_professional_variable_impact_review.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/04_math_formulas.md
---

# GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01

## 1_MASTER_TARGET

Préparer le pipeline de données historiques pour le backtest de la stratégie d'accumulation BTC COIN-M, sans exécuter le backtest, sans connecter Bitget en live, sans implémenter de worker runtime.

Objectif strict :

```text
Définir les schémas, les sources, les transformations et les invariants
des données de backtest pour que le backtest réel (POSTERIEUR) puisse
s'exécuter sur des bases solides et vérifiables.
```

## 2_INITIAL_PROJECT_DOC

Ce document est le transporteur initial pour ouvrir le child `BACKTEST_DATA_PREP_01`, débloqué par la PR #243 (FORMULAS_SOURCE_LOCK = merged PASS, 9/9 UNKNOWN levés).

Règle : aucun backtest réel, aucun worker runtime, aucune connexion exchange et aucune UI nouvelle ne sont autorisés dans ce child.

## 3_INITIAL_NEED

Contexte :

```text
PR #235 (PARENT_BTC_COINM) = merged
PR #239 (FORMULAS_COMPAT_REVIEW) = merged PASS
PR #243 (FORMULAS_SOURCE_LOCK) = merged PASS, 9/9 UNKNOWN → PAPER_LOCKED
BACKTEST_DATA_PREP_01 = débloqué
```

Besoin immédiat :

```text
Préparer les données de backtest BTC COIN-M :
- schéma des données d'entrée (candles, funding, contract spec)
- sources de données historiques (Bitget API publiques, sans clé live)
- transformations nécessaires (resampling, gap detection, validation)
- contrats de données compatibles avec les formules PAPER_LOCKED
- invariants de qualité (pas de trous, pas de prix aberrants)
```

## 4_MASTER_PROJECT_PLAN

1. Relire les formules PAPER_LOCKED de `FORMULAS_SOURCE_LOCK_01`.
2. Définir le schéma de données d'entrée pour le backtest.
3. Inventorier les sources Bitget publiques (kline publique, funding rate history, contract info).
4. Définir les transformations et la validation.
5. Produire un contrat de données minimal avec un exemple de jeu test.
6. Vérifier la compatibilité avec `trading_lab_v1`.
7. Produire verdict : `PASS / PATCH_REQUIRED`.

## 6_FINAL_TARGET

Ce child doit produire :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/01_backtest_data_prep.md
```

Contenu attendu :

```text
1. Schéma des données d'entrée (candles OHLCV, funding_rate, contract_spec_snapshot).
2. Sources Bitget (endpoints publics, pas de clé API live).
3. Pipeline de transformation (resampling, alignement temporel, gap filling).
4. Validation et invariants de qualité.
5. Contrat de données JSON minimal.
6. Exemple de jeu de test statique (quelques bougies + funding).
7. Mapping vers trading_lab_v1 pour le futur backtest engine.
8. Verdict et autorisation du backtest réel.
```

## 8_VALIDATED_PLAN — Séquence

```text
1. Valider le présent 00_INITIAL_PROJECT_DOC.md.
2. Créer 01_backtest_data_prep.md.
3. Y définir le pipeline de données complet.
4. Produire verdict PASS / PATCH_REQUIRED.
5. Si PASS → backtest réel autorisé (dans un child ultérieur WORKER/BACKTEST).
6. RUNTIME et LIVE restent bloqués (PAPER_LOCKED < API_VERIFIED).
```

## 12_INVARIANTS

```text
- aucune connexion exchange live (pas de clé API, pas d'ordre)
- aucun backtest réel exécuté dans ce child
- aucun worker runtime
- aucune nouvelle UI
- pas de second backtest engine (réutiliser trading_lab_v1)
- les données doivent être vérifiables sans connexion Bitget (endpoints publics ou snapshots)
- les formules utilisées sont celles PAPER_LOCKED de FORMULAS_SOURCE_LOCK_01
- aucun historique funding manquant ne doit être toléré sans avertissement
- les gaps de bougies doivent être détectés et documentés
- les prix doivent être cohérents : MarkPrice ≈ IndexPrice, LastPrice proche
- pas de données synthétiques non documentées comme telles
- le contrat de données doit être lisible par trading_lab_v1
```

## 10_SELECTED_SETUP — Sources de données

| Donnée | Source | Accès |
|---|---|---|
| Candles OHLCV BTCUSD COIN-M | Bitget API publique `/api/v2/mix/market/candles` | Public, pas de clé |
| Mark price history | Bitget API publique `/api/v2/mix/market/mark-price` | Public, pas de clé |
| Funding rate history | Bitget API publique `/api/v2/mix/market/history-fundRate` | Public, pas de clé |
| Contract spec `contractSize`, tiers, etc. | Bitget API publique `/api/v2/mix/market/contracts` | Public, pas de clé |
| Index price constituents | Bitget doc / spot exchange composites | Documentation |

## 15_REMAINING_GAP

```text
- accès réel à l'API Bitget pour télécharger l'historique (pas dans ce child, documentation uniquement)
- volume de données (> 1 an de candles 1h) et stockage local
- snapshot contract spec réel (contractSize, tiers, fundingInterval) à confirmer
- gestion des changements de contract spec dans le temps (delisting, nouveaux tiers)
```

## 16_TODO

```text
1. Commit + push du présent document.
2. Créer 01_backtest_data_prep.md.
3. Définir les schémas, sources, transformations, contrats.
4. Après PASS du child complet, ouvrir le child backtest réel (WORKER_BACKTEST).
5. RUNTIME et LIVE restent dans la séquence future.
```

## GAP_INDEXATION

Ce lot ouvre un child documentaire sur branche dédiée. Les index globaux ne sont pas modifiés.

Trace canonique de reprise :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/00_INITIAL_PROJECT_DOC.md
```

## 17_RESUME_POINT

```text
PR #243 mergée : FORMULAS_SOURCE_LOCK = PASS, 9/9 UNKNOWN levés.
BACKTEST_DATA_PREP_01 = débloqué, ouvert comme child documentaire.
Portée : schémas, sources, transformations, contrats de données.
Aucun backtest réel exécuté ici.
Prochaine action : validation utilisateur, puis création 01_backtest_data_prep.md.
```

## RISKS

- À qualifier.
