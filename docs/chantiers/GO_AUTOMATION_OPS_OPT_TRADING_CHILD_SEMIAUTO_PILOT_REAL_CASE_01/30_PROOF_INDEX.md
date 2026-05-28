# 30_PROOF_INDEX

## Artefacts générés

| Fichier | Path |
|---------|------|
| Proof JSON | `artifacts/automation_ops/semiauto_pilot/pilot_b4812d88/proof.json` |
| Proof Markdown | `artifacts/automation_ops/semiauto_pilot/pilot_b4812d88/proof_summary.md` |

## Contenu proof.json (extrait)

```json
{
  "run_id": "pilot_b4812d88",
  "go_id": "GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_SCOPE_01",
  "parent_go_id": "GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01",
  "mode": "dry_run",
  "actions_planned": [
    "audit: lister les PRs ouvertes",
    "audit: vérifier état PR #875",
    "audit: lister les chantiers actifs récents",
    "audit: identifier les chantiers sans 90_CLOSEOUT.md",
    "produire preuve JSON + Markdown",
    "retourner verdict au gate humain"
  ],
  "actions_executed": [
    "read GO_PROMPT",
    "validate handoff contract"
  ],
  "stop_conditions": [],
  "human_gate_required": true,
  "verdict": "PASS_DRY_RUN",
  "next_go": "GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_RUNTIME_PROOF_01 — à décider humain"
}
```

## Vérification

```bash
cat artifacts/automation_ops/semiauto_pilot/pilot_b4812d88/proof.json
cat artifacts/automation_ops/semiauto_pilot/pilot_b4812d88/proof_summary.md
```
