# 10_AUDIT_SCOPE

## Périmètre de l'audit

| Axe | Source | Mutation |
|-----|--------|---------|
| PRs ouvertes | `gh pr list --state open` | NON |
| 8 derniers commits mainline | `git log --oneline -8` | NON |
| Présence du module semiauto_pilot | filesystem | NON |
| Tests 17/17 PASS | `pytest` | NON |

## GO_PROMPT utilisé

```json
{
  "actions_planned": [
    "audit: vérifier état sot/mainline post-merges #922 #924 #875 #923 #925",
    "audit: lister les PRs ouvertes — résultat attendu 0",
    "audit: lister les 8 derniers commits mainline",
    "audit: vérifier présence modules/automation_ops/semiauto_pilot/",
    "audit: vérifier tests 17/17 PASS",
    "produire preuve JSON + Markdown",
    "retourner verdict au gate humain"
  ],
  "next_go": "",
  "stop_conditions": []
}
```

## Commande exécutée

```bash
python -m modules.automation_ops.semiauto_pilot.pilot_runner /tmp/mainline_audit_prompt.json
```

Exit : `0` (`PASS_DRY_RUN`)
