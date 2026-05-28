---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_BAK_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_BAK_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: blocked
lifecycle_stage: blocked_permissions
topic_keys: [cleanup, bak, code_ops, dedup]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01/30_DECISION_TABLE.md
---

# GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_BAK_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Supprimer les deux répertoires `.bak` présents sur disque local.

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| Cible A | `modules/install_module_openclaw.bak_20260314/` |
| Cible B | `modules/ops_wrappers.bak/` |
| Status git | non trackées (gitignorées par `*.bak_*`) |
| Propriétaire disque | `root:root` |
| Status | **BLOCKED** — permission denied |

## Blocage

Les deux répertoires sont la propriété de `root`. La suppression locale nécessite
`sudo rm -rf` par un opérateur ayant les droits.

Commande à exécuter manuellement :

```bash
sudo rm -rf /opt/trading/modules/install_module_openclaw.bak_20260314
sudo rm -rf /opt/trading/modules/ops_wrappers.bak
```

Aucun commit git requis (les répertoires sont gitignorés, non committés).

## Preuve de sécurité

- aucun import Python détecté (`git grep`)
- aucune référence dans workflow CI
- `*.bak_*` et `*.bak` dans `.gitignore` depuis l'origine
- suppression recommandée dans `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01`

## Verdict

```text
BLOCKED_PERMISSIONS — action manuelle root requise.
```
