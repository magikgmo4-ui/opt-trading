---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02_PROOF_INDEX
doc_type: proof_index
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02
run_id: pilot_634561cf
created_at: 2026-05-28
---

# 30_PROOF_INDEX

## Artefacts générés

| Fichier | Chemin | Présent |
|---------|--------|:-------:|
| `proof.json` | `artifacts/automation_ops/semiauto_pilot/pilot_634561cf/proof.json` | oui |
| `proof_summary.md` | `artifacts/automation_ops/semiauto_pilot/pilot_634561cf/proof_summary.md` | oui |

## Résumé proof.json

```json
{
  "run_id": "pilot_634561cf",
  "mode": "dry_run",
  "human_gate_required": true,
  "verdict": "PASS_DRY_RUN",
  "next_go": "GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01",
  "actions_planned": 8,
  "actions_executed": 2,
  "stop_conditions": []
}
```

## Note gap G03

Le champ `go_id` dans `proof.json` reflète le runner (`GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_SCOPE_01`), pas ce GO (`_JOBS_REGISTRY_PILOT_02`). Comportement connu — documenté dans `40_GAPS_AND_NEXT_GO.md`.

## Vérification intégrité

```bash
python3 -c "
import json
p = json.load(open('artifacts/automation_ops/semiauto_pilot/pilot_634561cf/proof.json'))
assert p['verdict'] == 'PASS_DRY_RUN'
assert p['human_gate_required'] is True
assert p['mode'] == 'dry_run'
assert p['stop_conditions'] == []
print('OK')
"
```
