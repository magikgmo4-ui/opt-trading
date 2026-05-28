---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_TEST_LOCK_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_TEST_LOCK_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: closed
lifecycle_stage: done
topic_keys:
  - opt-trading
  - code_ops
  - test_lock
  - validation
  - registry
  - blocked_qualify
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/60_TEST_LOCK_AND_VALIDATION.md
  - docs/registry/CODE_REGISTRY.md
---

# GO_CODE_OPS_OPT_TRADING_CHILD_TEST_LOCK_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Appliquer le verrouillage test/validation défini par `60_TEST_LOCK_AND_VALIDATION.md` :
- créer les tests manquants (A05, A06) ;
- qualifier les 4 entrées BLOCKED du registre (consumer audit) ;
- mettre à jour CODE_REGISTRY.md en conséquence.

## 6_FINAL_TARGET

Tests A05 + A06 présents et PASS. 4 entrées BLOCKED résolues dans le registre.

## 3_SCOPE

| # | Action | Cible |
|---|---|---|
| T01 | créer tests | `tests/governance/test_strategy_registry_validator.py` (A05) |
| T02 | créer tests | `tests/governance/test_trading_schemas.py` (A06) |
| T03 | qualifier BLOCKED | `portfolio_engine` — consumer audit |
| T04 | qualifier BLOCKED | `probability_engine` — consumer audit |
| T05 | qualifier BLOCKED | `trae_module_validator` — consumer audit |
| T06 | qualifier BLOCKED | `reseau_ssh_step1b` — consumer audit |
| T07 | update registry | A04 note tests existants ; T03-T06 résultats |

## 4_AUDIT_BLOCKED

### portfolio_engine
- `modules/desk_pro_orchestrator/app/desk_pro_orchestrator.py:44` — dynamic import map
- `modules/desk_pro_dashboard/app/desk_pro_dashboard.py` — référencé
- Verdict : **ACTIVE** — consommateurs confirmés, next_action KEEP

### probability_engine
- `modules/desk_pro_orchestrator/app/desk_pro_orchestrator.py:36` — dynamic import map
- `modules/proposition_engine/app/engines.py:17-19` — import direct
- Verdict : **ACTIVE** — consommateurs confirmés, next_action KEEP

### trae_module_validator
- `modules/ops_menu_hub/scripts/menu.sh:152,162` — entrée menu `menu-trae_module_validator`
- Verdict : **CANDIDATE** — utilisé en ops menu, rôle opérateur, next_action KEEP

### reseau_ssh_step1b
- `modules/reseau_ssh/scripts/_reseau_ssh_common.sh:35` — RESEAU_SSH_STEP1B_DIR défini et utilisé
- Verdict : **CANDIDATE** — sous-module de reseau_ssh, relation documentée, next_action KEEP

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| A04 validate_master_target_continuity | tests déjà présents — 4 PASS (tests/governance/test_master_target_validator.py) |
| A05 validate_strategy_registry | CRÉER tests/governance/test_strategy_registry_validator.py |
| A06 schemas trading | CRÉER tests/governance/test_trading_schemas.py |
| T03-T06 BLOCKED audit | consumer proof via git grep |

## 7_CANONICAL_STATE (post-exécution)

| Champ | Valeur |
|---|---|
| T01 test_strategy_registry_validator.py | DONE — 5/5 PASS |
| T02 test_trading_schemas.py | DONE — 10/10 PASS |
| T03 portfolio_engine | ACTIVE/KEEP — consumers confirmés |
| T04 probability_engine | ACTIVE/KEEP — consumers confirmés |
| T05 trae_module_validator | CANDIDATE/KEEP — ops_menu_hub consumer |
| T06 reseau_ssh_step1b | CANDIDATE/KEEP — reseau_ssh sub-module |
| T07 CODE_REGISTRY update | DONE — BLOCKED_UNKNOWN_CONSUMER 4→0 ; A04-A06 DONE |

## 17_RESUME_POINT

```text
DONE — 15 tests PASS, 4 BLOCKED qualifiés, registre mis à jour.
GO fermé. Parent proche de 6_FINAL_TARGET.
```
