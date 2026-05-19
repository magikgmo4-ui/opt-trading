# Runtime Health Supervisor — Phase 1

## Objectif

Diagnostic-only health supervisor pour opt-trading. Aucun restart automatique. Aucun secret dans les logs ou outputs. Compatible Debian 12, Python 3.11+, systemd.

## Structure

```
modules/runtime_health/
├── __init__.py
├── healthcheck.py          # Script principal
├── config/
│   └── runtime_health.yml  # Configuration des checks
├── schemas/
│   └── runtime_health.schema.json  # JSON Schema (draft-07) du rapport
└── README.md
```

## Checks couverts

| Bloc              | Description                                              |
|-------------------|----------------------------------------------------------|
| SYSTEMD_SERVICES  | `systemctl is-active` + `is-enabled` pour chaque service|
| SYSTEMD_TIMERS    | `systemctl show` (ActiveState, NextElapseUSecRealtime)   |
| VENV              | Existence venv + `python --version`                      |
| ENV               | Présence des variables d'env requises (valeur jamais loggée) |
| PORTS             | TCP connect timeout=2s                                   |
| HTTP              | HTTP GET timeout=3s, code retour                         |
| PATHS             | Existence + droits write si requis                       |
| ARTIFACTS         | mtime age check (répertoires ou fichiers)                |
| LOGS              | journalctl -p err + tail logfiles                        |
| ORCHESTRATOR      | `tmux has-session`                                       |

## Outputs

- `/opt/trading/data/runtime_health/latest.json` : rapport complet du dernier run
- `/opt/trading/data/runtime_health/healthcheck.jsonl` : historique (une ligne JSON par run)

### Format latest.json

```json
{
  "timestamp": "2026-05-19T10:00:00+00:00",
  "hostname": "db-layer",
  "run_id": "<uuid4>",
  "overall_status": "PASS|WARN|FAIL",
  "block_statuses": {"SYSTEMD_SERVICES": "PASS", ...},
  "checks": {"SYSTEMD_SERVICES": [...], ...},
  "elapsed_seconds": 1.23
}
```

### Exit codes

- `0` : PASS ou WARN
- `1` : FAIL bloquant

## Options CLI

```
healthcheck.py [--config <path>] [--dry-run] [--no-telegram]
```

- `--config` : chemin vers `runtime_health.yml` (défaut : `config/runtime_health.yml` relatif au script)
- `--dry-run` : exécute les checks, affiche le rapport, n'écrit aucun fichier
- `--no-telegram` : supprime les notifications Telegram

## Installer le systemd timer

```bash
# Copier les unités
cp deploy/systemd/opt-trading-runtime-health.service /etc/systemd/system/
cp deploy/systemd/opt-trading-runtime-health.timer   /etc/systemd/system/

# Recharger et activer
systemctl daemon-reload
systemctl enable --now opt-trading-runtime-health.timer

# Vérifier
systemctl status opt-trading-runtime-health.timer
```

## Tester manuellement

```bash
# Dry-run (aucun fichier écrit, aucune notification Telegram)
python3 modules/runtime_health/healthcheck.py --dry-run --no-telegram

# Run complet avec config custom
python3 modules/runtime_health/healthcheck.py \
  --config modules/runtime_health/config/runtime_health.yml

# Via le wrapper shell
bash scripts/runtime_healthcheck.sh --dry-run --no-telegram

# Déclencher le service systemd manuellement
systemctl start opt-trading-runtime-health.service
journalctl -u ot-runtime-health -f
```

## Contraintes Phase 1

- Diagnostic-only : aucun restart, aucune action corrective automatique
- Aucun secret dans les logs ou outputs (valeurs env jamais loggées)
- Stdlib uniquement (`pyyaml` optionnel via try/except)
- Notifications Telegram uniquement sur changement d'état (configurable)
- Exit 0 si PASS ou WARN, exit 1 si FAIL

## Phase 2 (future)

Voir `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_01` pour la roadmap self-heal.
