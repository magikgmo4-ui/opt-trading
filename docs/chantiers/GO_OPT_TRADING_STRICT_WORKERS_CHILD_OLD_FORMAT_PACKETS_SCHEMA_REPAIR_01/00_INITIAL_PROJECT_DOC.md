# GO_OPT_TRADING_STRICT_WORKERS_CHILD_OLD_FORMAT_PACKETS_SCHEMA_REPAIR_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_STRICT_WORKERS_CHILD_OLD_FORMAT_PACKETS_SCHEMA_REPAIR_01` |
| Objet | Réparer les 12 job packets old-format pour atteindre 22/22 PASS au validateur |
| Déclencheur | PR #610 (registry reconciliation) lue — il reste 12 packets invalides sur sot/mainline |
| Critère PASS | 22/22 packets PASS, 0 errors, aucun modèle retired dans worker_candidates |
| Source | `scripts/ai/workers/_validate_job.py`, `tasks.index.json`, `models.registry.json` |

## État initial (sot/mainline, pre-#610)

```
PASS=10 FAIL=12
```

### Packets OK (10)
Les 10 packets MATRIX et READONLY_SMOKE passent déjà le validateur.

### Packets FAIL (12)
Tous avec la même erreur : `MISSING_FIELD: worker_candidates` + `MISSING_FIELD: default_worker`.

Répartition :
- 3 POOL_SMOKE (dont 2 avec worker_assigned = modèle RETIRED)
- 2 E2E
- 7 A4 (5 négatifs, 1 positif, 1 write reel test)
