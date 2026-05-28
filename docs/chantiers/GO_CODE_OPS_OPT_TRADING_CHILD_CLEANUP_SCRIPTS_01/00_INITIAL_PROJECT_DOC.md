---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_SCRIPTS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_SCRIPTS_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: closed
lifecycle_stage: done
topic_keys: [cleanup, scripts, code_ops, dedup]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01/30_DECISION_TABLE.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01/20_CONSUMER_MAP.md
---

# GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_SCRIPTS_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Supprimer les 3 scripts legacy `execution_engine_*` du module `execution_engine`.

## 6_FINAL_TARGET

Suppression effectuée. Module ne conserve que les scripts canoniques.

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| Fichiers supprimés | 3 |
| Commit | `ce0648db` |
| Preuve | grep — aucun appelant externe (D05, GO_CHILD_DEDUP_AUDIT_01) |
| Réversibilité | `git revert ce0648db` |

## Suppression effectuée

```text
SUPPRIMÉ : modules/execution_engine/scripts/execution_engine_cmd.sh
SUPPRIMÉ : modules/execution_engine/scripts/execution_engine_menu.sh
SUPPRIMÉ : modules/execution_engine/scripts/execution_engine_sanity_check.sh

CONSERVÉ : modules/execution_engine/scripts/cmd.sh
CONSERVÉ : modules/execution_engine/scripts/menu.sh
CONSERVÉ : modules/execution_engine/scripts/sanity_check.sh
```

## Verdict

```text
DONE — D05 nettoyé.
```
