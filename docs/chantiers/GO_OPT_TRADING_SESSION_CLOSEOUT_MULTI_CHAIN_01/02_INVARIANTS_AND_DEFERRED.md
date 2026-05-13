---
doc_id: GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01_INVARIANTS_AND_DEFERRED
doc_type: invariants
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01
status: final
lifecycle_stage: global_closeout
topic_keys:
  - opt-trading
  - invariants
  - deferred
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01/02_INVARIANTS_AND_DEFERRED.md
point_de_reprise: "Invariants et points differes."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01/01_CHAINS_CLOSED.md
---

# 02_INVARIANTS_AND_DEFERRED

## 1_INVARIANTS — NE PAS ROUVRIR

```text
- PERF DB retire : deja execute, ne pas refaire
- PERF DB paths : ne pas modifier sans preuve
- COLLECTORS helper extraction : 10 lots livres, ne pas creer impl_11 sans bug
- modules/health/ : 4 phases livrees, circuit breaker reste dry-run
- DeepSeek READMEs : mis a jour, ne pas modifier sans audit callers
```

## 2_STALE CONTEXT — IGNORER

```text
- PERF_DB_LEGACY_RETIRE_IMPL_01 → deja execute via #309
- FORMULAS_SOURCE_LOCK → contexte different, hors session
```

## 3_POINTS DIFFERES

```text
PERF :
  - PERF DB legacy retire a ete execute
  - aucun point differe restant

COLLECTORS :
  - chaîne close, aucun point differe

Observability :
  - phase 5 (circuit breaker actif) non demarree
  - dashboard HTML statique, pas de serveur

DeepSeek :
  - retrait de scripts/student/ differe
  - verification post_change.sh requise avant retrait
  - effectuee par operateur humain
```
