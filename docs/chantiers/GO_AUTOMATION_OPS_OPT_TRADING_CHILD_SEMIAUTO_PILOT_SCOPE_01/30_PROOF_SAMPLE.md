# 30_PROOF_SAMPLE

## Exemple de proof.json (PASS_DRY_RUN)

```json
{
  "run_id": "pilot_3f7a1c2d",
  "go_id": "GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_SCOPE_01",
  "parent_go_id": "GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01",
  "mode": "dry_run",
  "input_prompt_path": "/tmp/my_go_prompt.txt",
  "actions_planned": [
    "read GO_PROMPT",
    "validate handoff contract",
    "check stop conditions",
    "write proof artefacts",
    "return verdict"
  ],
  "actions_executed": [
    "read GO_PROMPT",
    "validate handoff contract"
  ],
  "stop_conditions": [],
  "human_gate_required": true,
  "verdict": "PASS_DRY_RUN",
  "next_go": ""
}
```

## Exemple de proof_summary.md

```markdown
# Proof — pilot_3f7a1c2d

| Field | Value |
|---|---|
| GO | `GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_SCOPE_01` |
| Parent GO | `GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01` |
| Mode | `dry_run` |
| Human gate | `True` |
| Verdict | **PASS_DRY_RUN** |
| Next GO | `—` |
| Generated | 2026-05-28T10:00:00Z |

## Actions planned

- read GO_PROMPT
- validate handoff contract
- check stop conditions
- write proof artefacts
- return verdict

## Actions executed

- read GO_PROMPT
- validate handoff contract
```
