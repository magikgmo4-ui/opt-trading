# 30_LIMITS_AND_NEXT_USAGE

## Limites permanentes de la v1

| Limite | Description |
|--------|-------------|
| `dry_run` uniquement | Aucune action live dans ce pilot |
| Gate humain obligatoire | Toute décision `next_go` reste humaine |
| `actions_executed` figé | Ne reflète pas les actions réelles exécutées |
| Pas de jobs registry live | `next_go` non proposé automatiquement |
| Pas de chaînage GO | Les GOs ne s'enchaînent pas sans intervention humaine |

## Ce que la v1 ne fait PAS

- Elle n'exécute pas d'ordres trading.
- Elle ne merge pas de PRs automatiquement.
- Elle ne modifie pas de workflows.
- Elle ne lit pas le jobs registry pour proposer un prochain GO.

## Prochaine étape — usage contrôlé

Le prochain chantier n'est plus "refactor". Il doit être un **usage réel de la boucle semi-auto sur un GO produit** :

```
Choisir un GO fonctionnel (data_center, strategy, perf, etc.)
→ Écrire un GO_PROMPT structuré
→ Lancer scripts/automation_ops/run_semiauto_pilot.sh
→ Valider la preuve humainement
→ Décider du next_go
```

## Candidats naturels pour le premier usage produit

| Candidat | Domaine | Complexité |
|----------|---------|-----------|
| `GO_OPT_TRADING_DATA_CENTER_*` | collecteurs data | faible |
| `GO_STRATEGY_*` | stratégie | moyen |
| `GO_OPT_TRADING_PERF_*` | perf analytics | moyen |

La décision appartient à l'opérateur. Ce close gate ne l'impose pas.
