---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_DAEMONIZATION_01
doc_type: closeout
repo: opt-trading
status: CLOSED / MERGED
closed_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_DAEMONIZATION_01 — CLOSEOUT

## 7_CANONICAL_STATE

```text
RUNTIME_DAEMONIZATION = CLOSED / MERGED
CODE_CHANGES = scripts/deskpro_api_daemon.sh (new)
UNITTEST = 111_PASS
SECRETS = NOT_INCLUDED
PORT_8010 = managed via deskpro_api_daemon.sh
```

## Livrable

`scripts/deskpro_api_daemon.sh` — 5 subcommands :

| Commande | Comportement validé |
|---|---|
| `start` | PID absent → lance uvicorn, écrit PID, health check → OK |
| `start` (double) | PID présent + process running → "already running", no-op |
| `stop` | SIGTERM → attente → "stopped", supprime PID |
| `status` | RUNNING + health JSON / STOPPED selon PID |
| `restart` | stop → start → health OK |

## Décisions techniques

| Point | Décision |
|---|---|
| Gestion PID | Fichier `/opt/trading/tmp/deskpro_api.pid` |
| Python | Venv `.venv/bin/python3` si présent, sinon `python3` système |
| Env | `source scripts/load_env.sh` au start |
| Port conflict | `ss -ltnp` avant start — erreur explicite si occupé |
| SIGKILL | Fallback après 10s d'attente SIGTERM |
| `set -euo pipefail` | `(( i++ ))` → `i=$(( i + 1 ))` pour éviter exit code 1 |
| `return` vs `exit` | Fonctions utilisent `return` pour composer dans `restart` |

## Findings audit

| Élément | Constat |
|---|---|
| `desk_pro_ui_toolbox_final_cmd.sh` | Utilise venv — inutilisable en local sans venv |
| `scripts/desk_pro_cmd.sh serve` | Pointe vers `scripts/run_api.sh` — absent |
| tmux `desk-pro` | Gère stack complète (runner+orchestrator+perf+logs) — non modifié |
| systemctl | Inaccessible en sandbox |
| venv | Absent en local, system python3 (miniforge3 3.13.12) utilisé |
