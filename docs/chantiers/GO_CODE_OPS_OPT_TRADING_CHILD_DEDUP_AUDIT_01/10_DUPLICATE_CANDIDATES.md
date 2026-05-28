---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01_DUPLICATE_CANDIDATES
doc_type: dedup_audit
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01
status: open
lifecycle_stage: dedup_audit_complete
topic_keys: [dedup, duplicates, candidates, code_ops]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 10_DUPLICATE_CANDIDATES

Candidats de ce GO : anomalies A01–A06 et D05/D06.

---

## D05 — scripts doublés dans modules/execution_engine/scripts/

| Champ | Valeur |
|---|---|
| Groupe | D05 |
| Scripts canoniques | `cmd.sh`, `menu.sh`, `sanity_check.sh` |
| Scripts legacy | `execution_engine_cmd.sh`, `execution_engine_menu.sh`, `execution_engine_sanity_check.sh` |
| Catégorie | `LEGACY_REPLACED` |

**Description** : trois scripts canoniques (convention `modules/`) coexistent avec
trois scripts préfixés `execution_engine_*` dans le même répertoire. Les deux ensembles
sont structurellement différents et ne sont pas des alias.

---

## D06 — répertoires .bak commitées

| Champ | Valeur |
|---|---|
| Groupe | D06 |
| Path A | `modules/install_module_openclaw.bak_20260314/` |
| Path B | `modules/ops_wrappers.bak/` |
| Catégorie | `LEGACY_REPLACED` / `DELETE_CANDIDATE` |

**Description** : deux répertoires de backup committés. Les docs existants
(`GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01`) recommandent déjà
`rm -rf` pour ces deux répertoires.

---

## A01 — 22 modules sans sanity_check.sh

| Champ | Valeur |
|---|---|
| Catégorie | `MISSING_CONVENTION` |
| Impact | violation de la convention CLAUDE.md |
| Scope | 22 modules listés dans `GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/10_FILE_INVENTORY.md` |

**Description** : la convention `modules/` exige `cmd.sh`, `menu.sh`, `sanity_check.sh`
et `install_shortcuts.sh`. 22 modules ont `cmd.sh` mais pas `sanity_check.sh`.

---

## A03 — modules/router/ classé BLOCKED

| Champ | Valeur |
|---|---|
| Catégorie | `FALSE_POSITIVE` |
| Registre actuel | BLOCKED_UNKNOWN_CONSUMER |
| Verdict | CANDIDATE / KEEP |

**Description** : `modules/router/` a été classé BLOCKED dans le registre v1 par
manque de données. L'audit révèle que c'est une facade CLI (info/readme/ls/grep/menu)
sans logique Python. Son README est explicite sur son rôle minimal.

---

## A04/A05/A06 — validateurs et schémas sans test

| Anomalie | Path | Catégorie |
|---|---|---|
| A04 | `tools/governance/validate_master_target_continuity.py` | `MISSING_TEST` |
| A05 | `tools/strategy/validate_strategy_registry.py` | `MISSING_TEST` |
| A06 | `docs/ot/trading/schemas/trading_event_v1.schema.json` | `MISSING_TEST` |
| A06 | `docs/ot/trading/schemas/trading_trade_v1.schema.json` | `MISSING_TEST` |
