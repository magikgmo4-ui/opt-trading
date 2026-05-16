# LocalCMS — Central UI

Cockpit de navigation système pour opt-trading. Lecture seule.

## Endpoints

| Endpoint | Description |
|---|---|
| `/` | UI HTML — menu global + sessions TMUX |
| `/health` | Health check |
| `/menu` | Menu JSON (14 domaines, 85+ modules) |
| `/menu/state` | Module state cache |
| `/runtime/tmux` | TMUX sessions report (9 sessions, critical/non-critical) |
| `/runtime/tmux/live` | Live TMUX session list |

## Commandes

```
cmd.sh sanity     — validation
cmd.sh status     — module status
cmd.sh run        — start FastAPI (port 8700)
cmd.sh stop       — stop FastAPI
cmd.sh health     — health check
```

## TMUX

Session `localcms-ui` (db-layer). Windows: consumer, health, logs.

## Contraintes V1

- Lecture seule
- Pas de live trade
- Aucun restart depuis LocalCMS
- LocalCMS = cockpit de navigation système
- Desk Pro = dashboard trading opérationnel
