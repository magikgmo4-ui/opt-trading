---
doc_id: GO_OPT_TRADING_RUNTIME_HELPERS_CLOSEOUT_SYNC_01_CLOSEOUT
doc_type: global_closeout
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_RUNTIME_HELPERS_CLOSEOUT_SYNC_01
status: final
lifecycle_stage: global_closeout
topic_keys:
  - opt-trading
  - perf
  - collectors
  - closeout
  - resume-point
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_RUNTIME_HELPERS_CLOSEOUT_SYNC_01/01_GLOBAL_CLOSEOUT.md
point_de_reprise: "Chantiers PERF et COLLECTORS clos. Point de reprise canonique."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01_EXEC/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/90_CLOSEOUT.md
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10_V2/90_CLOSEOUT.md
---

# GO_OPT_TRADING_RUNTIME_HELPERS_CLOSEOUT_SYNC_01

## 1_VERDICT

```text
PERF DB canonical migration   → CLOSED
COLLECTORS helper extraction   → CLOSED
```

## 2_ETAT FINAL — PERF

```text
PR de clôture : #309
SHA           : c16075b13

DB canonique  : modules/perf/data/perf.db (actif)
Legacy        : retiré → perf/perf.db.retired_20260512_000848
Launchers     : modules.perf.app:app avec resolve_perf_db_path()
Rollback      : perf_db_relocate.sh unretire
Backup        : backup/pre-perf-sync-20260511_232839

Chaîne complète :
  restructure plan → shims → path switch → DB relocation → relocate tool
  → path switch impl → retire gate → proof → runtime proof
  → deploy sync plan → deploy sync impl → DB copy & proof → legacy retire
```

## 3_ETAT FINAL — COLLECTORS

```text
PR de clôture : #324
SHA           : 762a6ce

collectors_core enrichi de :
  - ErrorInfo, classify_collector_error
  - build_running_status, build_success_status, build_failure_status
  - build_manifest_record, build_latest_record
  - append_event_record, append_error_record
  - freshness_state, retry_after_absolute, status_value
  - read_status_payload, status_payload_as_text, safe_previous_status
  - ensure_writable_directories, ensure_file

Consommateurs alignés :
  - collector_coingecko.run
  - collector_binance_spot.run
  - derivatives_collector (lifecycle_compat)
```

## 4_INVARIANTS — NE PAS ROUVRIR

```text
- PERF DB retire : déjà exécuté, ne pas refaire
- COLLECTORS helper extraction : 10 lots livrés, ne pas créer impl_11 sans bug
- TODO stale PERF_DB_LEGACY_RETIRE_IMPL_01 : ne pas suivre
- FORMULAS_SOURCE_LOCK : ne pas suivre (contexte stale différent)
```

## 5_POINT DE REPRISE CANONIQUE

```text
docs/product/PRODUCT_USAGE_MATRIX.md
```

## 6_NEXT GO CANDIDATS

```text
Priorité 1 :
  GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01

Priorité 2 :
  GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_EXECUTION_01
  ou suite de la chaîne BTC COIN-M (#235→#239→#243→#244)

Priorité 3 :
  GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01
```
