---
go_id: GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_TARGET_VALIDATOR_01
master_target_id: MT_PRODUCT_GOVERNANCE
doc_type: project_doc
repo: opt-trading
surface: code + doc
---

# GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_TARGET_VALIDATOR_01

## Objectif
Ajouter un validateur warning-only pour contrôler la continuité `master_target_id` dans `docs/chantiers/**`.

## Inputs
- `docs/governance/PRODUCT_FINAL_TARGET_REGISTRY_01.md`
- `docs/chantiers/**/*.md`

## Checks attendus
- `master_target_id` existant dans le registry
- absence de doublons de `master_target_id` entre chantiers
- `current_go` cohérent (si un fichier porte le `current_go` d'un target, il doit référencer ce target)
- rapport warning-only initial

## Fichiers livrés
- `tools/governance/validate_master_target_continuity.py` — validateur warning-only
- `tests/governance/test_master_target_validator.py` — 4 tests (smoke, registry, duplicates, output)

## Commande
```bash
python tools/governance/validate_master_target_continuity.py
```
