# GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_SMOKE_01

## Résultat

| Test | Durée | Input tokens | Output tokens | Statut |
|------|:-----:|:------------:|:-------------:|:------:|
| Diagnostic session | — | — | — | PASS (aucune session saturée) |
| Cold smoke | 54 080ms | 3 457 | 3 | PASS |
| Warm smoke | 5 368ms | 3 500 | 3 | PASS |
| Health finale | — | — | — | LIVE |
| Trade/worker | — | — | — | AUCUN |

## Session utilisée

- `66e1f924-2bdf-42b7-be39-6f83d70cff33` (créée automatiquement, vierge au départ)

## Archives présentes

- `session_63716f9b.archived` (bloatée)
- `dae2495a-...` + index files (sessions de test intermédiaires)
- Aucune > 30 jours → purge non déclenchée

## Verdict

```
SESSION_RETENTION_SMOKE_PASS
```

L'enchaînement post-purge est validé : session vierge → cold smoke → warm smoke → tout PASS.

## RISKS

- À qualifier.
