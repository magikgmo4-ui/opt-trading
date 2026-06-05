---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_DAEMONIZATION_01
doc_type: initial_project_doc
status: IN_PROGRESS
created_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_DAEMONIZATION_01

## Objectif

Créer un script de gestion stable pour le processus Desk Pro API (port 8010) :
`start | stop | status | restart | logs`

## Contexte

- Précédent GO (RUNTIME_SUPERVISION_01) a documenté l'architecture runtime.
- Gap identifié : aucun script ne gère proprement le processus uvicorn seul.
- `desk_pro_ui_toolbox_final_cmd.sh` utilise venv (absent en local).
- systemctl inaccessible en sandbox.
- Approche retenue : shell script avec PID file.

## Livrable

`scripts/deskpro_api_daemon.sh`

| Commande | Comportement |
|---|---|
| `start` | Lance uvicorn, écrit PID file, health check post-start |
| `stop` | SIGTERM + attente, SIGKILL si nécessaire, supprime PID file |
| `status` | Vérifie PID + health, détecte port occupé par autre process |
| `restart` | stop → sleep 1 → start |
| `logs` | `tail -f` du log uvicorn |

## Contraintes

- PID file : `/opt/trading/tmp/deskpro_api.pid`
- Log : `/opt/trading/tmp/uvicorn_8010.log`
- Port conflict detection avant start
- Fallback python : venv si présent, sinon `python3` système
- Env : `source scripts/load_env.sh`

## RISKS

- À qualifier.
