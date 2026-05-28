---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01_BLOCKED_OR_RISKY_CASES
doc_type: dedup_audit
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01
status: open
lifecycle_stage: dedup_audit_complete
topic_keys: [dedup, blocked, risky, code_ops]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 50_BLOCKED_OR_RISKY_CASES

Cas bloqués ou risqués identifiés dans ce GO.

---

## Cas bloqués hérités du registre v1 (non traités dans ce GO)

Ces cas restent BLOCKED — ils nécessitent un audit consommateur séparé :

| code_id | path | raison du blocage | lot requis |
|---|---|---|---|
| `portfolio_engine` | `modules/portfolio_engine/app/portfolio_engine.py` | consommateurs non identifiés | grep audit + qualifier |
| `probability_engine` | `modules/probability_engine/app/probability_engine.py` | consommateurs non identifiés | grep audit + qualifier |
| `reseau_ssh_step1b` | `modules/reseau_ssh_step1b/` | relation avec reseau_ssh non documentée | qualifier |
| `trae_module_validator` | `modules/trae_module_validator/` | rôle non documenté, absent de CLAUDE.md | qualifier |

---

## Cas risqués à surveiller dans les lots de suppression

### D05 — précaution suppression scripts

Avant de supprimer les scripts `execution_engine_*` :
1. vérifier que `sanity_check.sh` canonique passe bien (`bash scripts/sanity_check.sh`)
2. vérifier que `cmd.sh` est fonctionnel
3. commit séparé et réversible
4. noter dans le commit le grep de preuve d'absence de consommateur

Condition bloquante : si un runbook opérateur utilise `execution_engine_cmd.sh`
sur une machine distante non indexée dans le repo, la suppression serait cassante.
À vérifier sur les machines admin-trading et student avant suppression.

### D06 — précaution suppression .bak

Avant de supprimer les répertoires .bak :
1. vérifier qu'aucune machine distante ne les référence (admin-trading, student)
2. `git rm -r` + commit séparé réversible
3. ne pas faire dans une PR groupée avec d'autres changements

---

## Invariants appliqués dans ce GO

Aucune des décisions de suppression n'a été exécutée dans ce GO.
Toutes les suppressions sont déférées à des lots séparés, réversibles, avec commit dédié.

Ce GO est `doc-only` et `audit-first` conformément à la contrainte parent.
