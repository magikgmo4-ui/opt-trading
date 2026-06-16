# PROBE_EVIDENCE — ruleset enforcement

## Probe invalide

| Champ | Valeur |
|---|---|
| PR invalide | https://github.com/magikgmo4-ui/opt-trading/pull/1199 |
| Branche invalide | probe/GO_OPT_TRADING_GITHUB_ACTIONS_CHILD_RULESET_ENFORCEMENT_PROBE_01_INVALID_NO_CHANTIER |
| Résultat attendu | blocked |
| Résultat observé | blocked |
| Workflow | Gated PR — Scope and No-Overlap |
| Run ID | 27604838991 |
| Jobs conclusion | failure |
| gate/preflight | success |
| gate/file-scope | failure — "Validate current GO file scope" |
| gate/no-lock-overlap | failure — "Detect competing FILE_SCOPE claims for changed files" |
| gate/tests | skipped |
| Merge possible ? | non |
| PR fermée sans merge ? | oui |

## Verdict

Le ruleset est considéré validé :
- la PR invalide a échoué aux gates (file-scope + no-lock-overlap) ;
- GitHub a bloqué le merge (conclusion=failure) ;
- la PR invalide a été fermée sans merge.
