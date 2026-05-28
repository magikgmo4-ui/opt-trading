---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01_DECISION_TABLE
doc_type: dedup_audit
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01
status: open
lifecycle_stage: dedup_audit_complete
topic_keys: [dedup, decision_table, code_ops]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 30_DECISION_TABLE

Table de décision finale pour chaque anomalie de ce GO.

| duplicate_group | files | category | canonical_candidate | evidence | risk | decision | next_go |
|---|---|---|---|---|---|---|---|
| D05_legacy_cmd | `execution_engine_cmd.sh` | LEGACY_REPLACED | `cmd.sh` | aucun appelant externe prouvé | low | DELETE_AFTER_PROOF | `GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_SCRIPTS_01` |
| D05_legacy_menu | `execution_engine_menu.sh` | LEGACY_REPLACED | `menu.sh` | aucun appelant externe prouvé | low | DELETE_AFTER_PROOF | `GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_SCRIPTS_01` |
| D05_legacy_sanity | `execution_engine_sanity_check.sh` | LEGACY_REPLACED | `sanity_check.sh` | aucun appelant externe prouvé | low | DELETE_AFTER_PROOF | `GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_SCRIPTS_01` |
| D06_bak_openclaw | `modules/install_module_openclaw.bak_20260314/` | LEGACY_REPLACED | `modules/install_module_openclaw/` | aucun import Python ; rm-rf recommandé historiquement | low | DELETE_AFTER_PROOF | `GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_BAK_01` |
| D06_bak_ops | `modules/ops_wrappers.bak/` | LEGACY_REPLACED | `modules/ops_wrappers/` | aucun import Python ; dette .bak documentée | low | DELETE_AFTER_PROOF | `GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_BAK_01` |
| A01_missing_sanity | 22 modules (voir liste) | MISSING_CONVENTION | template `sanity_check.sh` | convention CLAUDE.md | medium | ADD_MISSING_FILE | `GO_CODE_OPS_OPT_TRADING_CHILD_SANITY_CHECK_BATCH_01` |
| A03_router | `modules/router/` | FALSE_POSITIVE | — | facade CLI, README explicite, pas de Python | low | KEEP — registre corrigé | aucun (corrigé dans ce GO) |
| A04_missing_test | `tools/governance/validate_master_target_continuity.py` | MISSING_TEST | — | aucun fichier test trouvé | medium | ADD_TEST | batch tests |
| A05_missing_test | `tools/strategy/validate_strategy_registry.py` | MISSING_TEST | — | aucun fichier test trouvé | medium | ADD_TEST | batch tests |
| A06_schema_s02 | `docs/ot/trading/schemas/trading_event_v1.schema.json` | MISSING_TEST | — | aucun test JSON Schema | high | ADD_TEST | batch tests |
| A06_schema_s03 | `docs/ot/trading/schemas/trading_trade_v1.schema.json` | MISSING_TEST | — | aucun test JSON Schema | high | ADD_TEST | batch tests |

---

## Règles appliquées

- `DELETE_AFTER_PROOF` : preuve de l'absence de consommateur requise avant suppression. Ici prouvée.
  La suppression reste dans un lot séparé avec commit réversible.
- `ADD_MISSING_FILE` : fichier à créer (sanity_check.sh) — pas une suppression.
- `FALSE_POSITIVE` : registre corrigé directement.
- `ADD_TEST` : tests à ajouter dans un lot dédié.

---

## Lots de travail dérivés

| Lot | Scope | Priorité |
|---|---|---|
| `GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_SCRIPTS_01` | supprimer D05 legacy scripts (3 fichiers) | low — sécurisé |
| `GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_BAK_01` | supprimer D06 .bak dirs (2 dirs) | low — sécurisé |
| `GO_CODE_OPS_OPT_TRADING_CHILD_SANITY_CHECK_BATCH_01` | créer 22 sanity_check.sh | medium |
| batch ADD_TEST validateurs | A04, A05, A06 | medium |
