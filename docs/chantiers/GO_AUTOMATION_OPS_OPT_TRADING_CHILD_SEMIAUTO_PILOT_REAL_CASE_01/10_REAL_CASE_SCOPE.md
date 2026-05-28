# 10_REAL_CASE_SCOPE

## Cas choisi : audit état repo

### Pourquoi ce cas

- Non destructif à 100% (lecture seule).
- Données réelles disponibles immédiatement (GitHub API + filesystem).
- Résultat vérifiable par l'opérateur humain.
- Illustre la boucle complète : GO_PROMPT → pilote → preuve → gate humain.

### Périmètre de l'audit

| Axe | Source | Mutation |
|-----|--------|---------|
| PRs ouvertes | `gh pr list --state open` | NON |
| Chantiers sans `90_CLOSEOUT.md` | `docs/chantiers/*/` | NON |

### GO_PROMPT utilisé

Fichier JSON passé au pilote :

```json
{
  "actions_planned": [
    "audit: lister les PRs ouvertes",
    "audit: vérifier état PR #875 (ANDROID_OPERATOR / TERMUX_TASKER)",
    "audit: lister les chantiers actifs récents dans docs/chantiers/",
    "audit: identifier les chantiers sans 90_CLOSEOUT.md",
    "produire preuve JSON + Markdown",
    "retourner verdict au gate humain"
  ],
  "next_go": "GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_RUNTIME_PROOF_01 — à décider humain",
  "stop_conditions": []
}
```

### Commande exécutée

```bash
python -m modules.automation_ops.semiauto_pilot.pilot_runner /tmp/real_case_go_prompt.json
```

Exit : `0` (`PASS_DRY_RUN`)
