# GO_OPT_TRADING_DESKPRO_WATCHDOG_STATUS_HEALTH_ALIGNMENT_01 — CLOSEOUT

## État final

| Élément | Statut |
|---------|--------|
| Tests | 172/172 PASS |
| `scripts/deskpro_watchdog.sh` | patché — classification infra/business |
| `tests/test_desk_pro_health_classification.py` | ajouté — 17 tests |
| Secrets | absents |
| Subcommands watchdog | `start/stop/status/run-once/logs` inchangées |

## Décision de classification

| Niveau | Condition | Action watchdog |
|--------|-----------|----------------|
| Infrastructure | Port 8000 ou 8010 DOWN | `ALERT` (issues++) |
| Application | `/desk/health` fail | `ALERT` (issues++) |
| Infrastructure applicative | `webhook:fail`, `perf:fail`, `probe_errors:fail` dans `/desk/status` (ports UP) | `ALERT` (issues++) via `infra_count` |
| Business / activité | `webhook_activity:fail` ou `warn` seul | `WARN` dans log — pas d'ALERT |
| Business / activité | `health=degraded` seul | `WARN` dans log — pas d'ALERT |

**Règle anti-double-comptage :** `infra_count` n'incrémente `issues` que si `issues == 0` à ce point. Si port 8000 DOWN provoque `webhook:fail` dans `/desk/status`, l'ALERT est déjà émise par le check de port — pas de sur-comptage.

## Comportement observé (run-once avec ports UP)

```
HEARTBEAT port=8000 status=UP
HEARTBEAT port=8010 status=UP health=ok
STATUS health=down webhook:pass perf:pass webhook_activity:fail probe_errors:pass
(no ALERT — infra_count=0)
```

`webhook_activity:fail` seul → pas d'ALERT. Attendu : aucun signal TradingView entrant en dev local.

## Fichiers modifiés

| Fichier | Nature |
|---------|--------|
| `scripts/deskpro_watchdog.sh` | Patch section `/desk/status` : infra_count + ALERT conditionnel |
| `tests/test_desk_pro_health_classification.py` | 17 tests : `_compute_health` + `_infra_fail_count` classification |

## Note : `/desk/health` hardcodé

`/desk/health` retourne toujours `{"ok": true}`. Le check `_health_ok()` dans le watchdog détecte uniquement si le port 8010 répond à HTTP — pas la santé applicative réelle. La classification infra/business via `/desk/status` est donc la seule couverture applicative effective.
