# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_SCOPE_01

## Objectif

Implémenter le premier pilote runtime semi-automatisé minimal, borné et non destructif, basé sur le plan Automation Ops validé.

## Parent GO

`GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01`

## Contexte

Le parent `GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01` est clos (PR #919, merge `1d7382740a`). Le plan validé documente : architecture map → jobs registry → jobs dedup → semi-auto loop protocol → handoff format → batch refactor.

Ce child GO met en pratique la boucle semi-auto avec un pilote réel.

## Contraintes

- Ne pas rouvrir le parent Automation Ops fermé.
- Ne pas modifier de workflow GitHub Actions.
- Ne pas automatiser de merge.
- Ne pas appeler d'API live trading.
- Ne pas supprimer de job.
- Ne pas modifier `secrets/`.
- Garder un gate humain obligatoire (`human_gate_required: true`).
- Mode `dry_run` uniquement pour ce pilote initial.

## Livrables

```
modules/automation_ops/semiauto_pilot/
  __init__.py
  handoff_contract.py
  proof_writer.py
  stop_conditions.py
  pilot_runner.py

scripts/automation_ops/run_semiauto_pilot.sh

tests/automation_ops/test_semiauto_pilot_contract.py

artifacts/automation_ops/semiauto_pilot/<run_id>/
  proof.json
  proof_summary.md
```

## Contrat de preuve JSON

```json
{
  "run_id": "pilot_<hex8>",
  "go_id": "GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_SCOPE_01",
  "parent_go_id": "GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01",
  "mode": "dry_run",
  "input_prompt_path": "...",
  "actions_planned": [],
  "actions_executed": [],
  "stop_conditions": [],
  "human_gate_required": true,
  "verdict": "PASS_DRY_RUN",
  "next_go": ""
}
```

## Exit codes

| Code | Signification |
|------|--------------|
| 0 | PASS_DRY_RUN |
| 2 | STOP_CONDITION_TRIGGERED |
| 3 | INVALID_HANDOFF_CONTRACT |
