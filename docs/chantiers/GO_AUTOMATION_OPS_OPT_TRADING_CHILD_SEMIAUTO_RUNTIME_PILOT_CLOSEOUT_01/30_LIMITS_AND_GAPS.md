# 30_LIMITS_AND_GAPS

## Limites permanentes de la v1

| Limite | Description |
|--------|-------------|
| `dry_run` uniquement | Aucun mode live dans ce pilote |
| Gate humain obligatoire | `human_gate_required: true` non contournable |
| `actions_executed` figé | Ne reflète pas les actions réellement exécutées — toujours `["read GO_PROMPT", "validate handoff contract"]` |
| `next_go` manuel | Pas de proposition automatique basée sur un jobs registry |
| Pas de chaînage | Les GOs ne s'enchaînent pas automatiquement |

## Gaps ouverts (non bloquants)

| ID | Description | Priorité |
|----|-------------|---------|
| G01 | `actions_executed` auto-tracking | ADD_FEATURE |
| G02 | Connexion au jobs registry pour proposer `next_go` | ADD_FEATURE |
| G03 | Diff `actions_planned` vs `actions_executed` dans la preuve | ADD_FEATURE |
| G04 | `go_id` dans la preuve reflète le runner, pas le GO enfant courant | MINOR |

## Ce que ce parent NE couvre PAS

- Merge automatique de PRs.
- Exécution d'actions destructives.
- Connexion à l'API trading.
- Modification de `secrets/` ou de workflows GitHub.

Ces sujets relèvent de futurs GOs explicitement ouverts par l'opérateur.
