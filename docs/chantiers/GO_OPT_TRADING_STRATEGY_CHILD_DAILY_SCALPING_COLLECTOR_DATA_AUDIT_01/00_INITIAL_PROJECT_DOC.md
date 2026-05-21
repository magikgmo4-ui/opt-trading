---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
depends_on: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - strategy
  - daily_scalping
  - collector_audit
  - xauusd_ohlcv
  - canonical_data
  - simex_bitget_bridge
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/10_COLLECTOR_INVENTORY.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/20_XAUUSD_OHLCV_CAPABILITY_CHECK.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/30_DERIVATIVES_CONTEXT_CAPABILITY_CHECK.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/40_CANONICAL_CONTRACT_GAP.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/50_SOURCE_DECISION.md
  - docs/index/inbox/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01.md
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Déterminer si les collectors API existants du repo peuvent fournir la source primaire `XAUUSD_M5_CANONICAL` / `XAUUSD_M15_CANONICAL` pour le backtest daily scalping, ou si un bootstrap externe (MT5/Dukascopy) est nécessaire en premier lieu.

## 2_CONTEXTE

### Dépendance

Le chantier `GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01` (PR #659) a établi :

```
Source primaire valide = broker export / prod api collector
Contrat obligatoire   = bid/ask/spread + UTC + sessions broker
Fallback smoke        = Yahoo/GC=F (interdit pour verdict)
```

Ce chantier audit prouve si un collector existant peut jouer le rôle de source primaire, avant de décider entre :

```
Option A : prod_collector/simex_bitget_bridge → adapté en source canonique
Option B : MT5/Dukascopy bootstrap rapide → puis collector en parallèle
Option C : Les deux en séquence (bootstrap court terme + collector moyen terme)
```

### Résultat de l'audit réel (2026-05-20)

L'audit du repo a révélé 4 collectors actifs. Conclusion préliminaire :

```
collector_binance_spot    → NOT_RELEVANT (crypto 24h seulement)
collector_coingecko       → NOT_RELEVANT (crypto seulement)
derivatives_collector     → CONTEXT_ONLY (OI/funding/liq/L/S — pas de prix)
simex_bitget_bridge       → PRIMARY_WITH_GAPS (XAUUSDT M5 via Bitget, mais gaps)
```

**Aucun collector n'est `PRIMARY_READY`** pour XAUUSD M5/M15 canonique avec bid/ask/spread.

`simex_bitget_bridge` est le seul candidat pour devenir la source primaire, avec adaptation.

## 3_OBJECTIF

Produire pour chaque collector :
- Classification : `PRIMARY_READY` / `PRIMARY_WITH_GAPS` / `CONTEXT_ONLY` / `SMOKE_ONLY` / `NOT_RELEVANT`
- Gaps précis vs contrat canonique
- Effort d'adaptation estimé

Et une décision finale :

```
50_SOURCE_DECISION : recommandation court terme + moyen terme + effort estimé
```

## 4_INVARIANTS

- Aucun ordre réel, aucun broker live execution
- Ne pas supposer que derivatives_collector fournit OHLCV
- Audit-first : ne pas coder avant d'avoir la décision documentée
- Aucun index global

## 5_PROCHAINE_ETAPE

Lire `10_COLLECTOR_INVENTORY.md` — inventaire complet avec classification.
