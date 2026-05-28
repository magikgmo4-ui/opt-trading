---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01_PROOF
doc_type: proof_index
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01
run_id: pilot_e2b9c0eb
created_at: 2026-05-28
---

# 30_PROOF_INDEX

## Artefacts générés

| Fichier | Chemin | Présent |
|---------|--------|:-------:|
| `proof.json` | `artifacts/automation_ops/semiauto_pilot/pilot_e2b9c0eb/proof.json` | oui |
| `proof_summary.md` | `artifacts/automation_ops/semiauto_pilot/pilot_e2b9c0eb/proof_summary.md` | oui |

## Résumé

```json
{
  "run_id": "pilot_e2b9c0eb",
  "mode": "dry_run",
  "human_gate_required": true,
  "verdict": "PASS_DRY_RUN",
  "actions_planned": 10,
  "stop_conditions": []
}
```

## Vérification

```bash
python3 -c "
import json
p = json.load(open('artifacts/automation_ops/semiauto_pilot/pilot_e2b9c0eb/proof.json'))
assert p['verdict'] == 'PASS_DRY_RUN'
assert p['human_gate_required'] is True
assert p['mode'] == 'dry_run'
print('OK')
"
```
