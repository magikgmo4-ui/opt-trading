---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
depends_on: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-20
topic_keys:
  - daily_scalping
  - collector_audit
  - xauusd_ohlcv
  - simex_bitget_bridge
  - canonical_data
  - source_decision
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/10_COLLECTOR_INVENTORY.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/20_XAUUSD_OHLCV_CAPABILITY_CHECK.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/30_DERIVATIVES_CONTEXT_CAPABILITY_CHECK.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/40_CANONICAL_CONTRACT_GAP.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01/50_SOURCE_DECISION.md
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01

**État:** Open — audit terminé, décision documentée
**Branche:** `go/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01`
**Parent:** `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`
**Dépend de:** PR #659 (DATA_METHOD_REWORK) mergée

Audit des 4 collectors existants pour déterminer la source primaire XAUUSD M5/M15 canonique.

## Résultat audit

| Collector | Classification |
|---|---|
| `collector_binance_spot` | NOT_RELEVANT |
| `collector_coingecko` | NOT_RELEVANT |
| `derivatives_collector` | CONTEXT_ONLY |
| `simex_bitget_bridge` | PRIMARY_WITH_GAPS |

**Aucune source PRIMARY_READY dans le repo.**

## Décision (50_SOURCE_DECISION)

```
Court terme  : MT5/Dukascopy export XAUUSD → bootstrap rapide (J+0 à J+2)
Moyen terme  : simex_bitget_bridge adapté → source durable (J+5 à J+10)
Contexte     : derivatives_collector XAUUSDT → enrichissement optionnel
```

## Prérequis immédiats

- Accès MetaTrader 5 avec historique XAUUSD M5 minimum 1 an, OU
- Accès Dukascopy (gratuit, historique 2003+)

## Docs

- `10_COLLECTOR_INVENTORY.md` — Inventaire + classification des 4 collectors
- `20_XAUUSD_OHLCV_CAPABILITY_CHECK.md` — Analyse détaillée simex_bitget_bridge (gaps + effort)
- `30_DERIVATIVES_CONTEXT_CAPABILITY_CHECK.md` — Confirmation CONTEXT_ONLY derivatives_collector
- `40_CANONICAL_CONTRACT_GAP.md` — Comparaison toutes sources vs contrat canonique
- `50_SOURCE_DECISION.md` — Recommandation stratégique + séquence bootstrap → collector durable
