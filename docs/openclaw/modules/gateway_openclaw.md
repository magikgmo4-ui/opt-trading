---
doc_id: OPENCLAW_MODULE_GATEWAY_OPENCLAW
doc_type: module_fiche
module: gateway_openclaw
path: modules/gateway_openclaw/
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
statut: actif
---

# gateway_openclaw — Fiche opérateur

Pilotage du gateway OpenClaw via `tmux`, adapté au mode opératoire retenu quand `systemd --user` n'est pas disponible.

## Rôle

- Démarrer, stopper et attacher la session gateway
- Lire les logs foreground
- Vérifier `health` et `probe`
- Standardiser le pilotage sous l'utilisateur `openclaw`

## Runtime

```
utilisateur : openclaw
session tmux : openclaw-gateway
gateway URL  : 127.0.0.1:18789
log foreground : ~openclaw/.openclaw/logs/gateway_foreground.log
```

## Scripts

```bash
bash scripts/cmd.sh start    # démarre la session openclaw-gateway
bash scripts/cmd.sh stop     # stoppe la session
bash scripts/cmd.sh attach   # attache la session tmux
bash scripts/cmd.sh logs     # logs foreground
bash scripts/cmd.sh health   # health check gateway
bash scripts/cmd.sh probe    # probe gateway
bash scripts/menu.sh         # menu interactif
bash scripts/sanity_check.sh # validation installation
bash scripts/install_shortcuts.sh  # installe wrappers /usr/local/bin
```

## Contenu

```
app/gateway_env.sh           # variables communes (user, home, session, log)
scripts/cmd.sh
scripts/start.sh
scripts/stop.sh
scripts/attach.sh
scripts/logs.sh
scripts/sanity_check.sh
scripts/install_shortcuts.sh
docs/README.md
```

## Intégration

- Hôte prioritaire : db-layer
- `doctor_openclaw` diagnostique ; `gateway_openclaw` **pilote** le runtime
- `openclaw_config_modulaire` peut déclencher un redémarrage gateway après apply config

## Distinction

| Module | Rôle |
| --- | --- |
| `gateway_openclaw` | Pilotage runtime (start/stop/attach/logs) |
| `doctor_openclaw` | Diagnostic + health/probe |

## Statut

```
actif — composant runtime explicite de la suite OpenClaw
gateway prouvé sur 127.0.0.1:18789
```
