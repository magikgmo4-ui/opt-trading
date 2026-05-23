---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01_RESIDUAL_WARNINGS_PROOF
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_RESIDUAL_WARNINGS_PROOF

## Etat d’entrée (rapporté)

Etat transmis comme contexte canonique de ce GO :

```text
STEP_5_PYTHON_PYYAML_BLOCKER = CLOSED
STEP_5_FINAL = WARN_RESIDUAL_ENV_PORTS_PATHS_STALE_MACHINES
warnings = ENV, PORTS, PATHS
stale_machines = cursor-ai, fantome
failing = []
unreachable = []
gateway non incriminé
watchdog 11-12 non lancé
```

Note : ce dépôt (branche locale) ne contient pas, à ce stade, un artefact “post-deploy validation results” matérialisé pour reproduire la sortie runtime exacte. Le présent fichier fixe donc une preuve repo-first (définition des checks + sources possibles de WARN), et conserve explicitement le gap “preuve terrain” dans `90_REPRISE.md`.

## Définition des checks (repo-first)

### STEP 5 — checks implémentés

Le runtime healthcheck exécute explicitement :

- `ENV` via `check_env_key` (présence seulement, sans valeur)
- `PORTS` via `check_port` (TCP connect)
- `PATHS` via `check_path` (existence + os.access write si demandé)

Sources :

- `modules/runtime_health/healthcheck.py`
- `modules/runtime_health/machine_map.py`
- `config/machine_runtime_map.yml`
- `modules/runtime_health/config/runtime_health.yml`

### Cas typiques de WARN (mécanique)

- Une entrée marquée `optional_*` produit un statut `WARN` si elle est absente / injoignable.
- `stale_machines` est produit par l’orchestrateur fleet si l’âge du `latest.json` dépasse le seuil.

## Preuve “stale_machines” (seuil)

```text
modules/runtime_health/fleet_orchestrator.py
_STALE_THRESHOLD_MINUTES = 15
```

## Preuve “ENV/PORTS/PATHS” : scope db-layer dans la map

Extraits structurants (sans secrets) :

```yaml
# config/machine_runtime_map.yml
db-layer:
  optional_ports:
    - label: openclaw_gateway
      host: 127.0.0.1
      port: 18789
    - label: algo_hf_api
      host: 127.0.0.1
      port: 8000
  required_paths:
    - path: /opt/trading
      writable: false
    - path: /opt/trading/data
      writable: true
  optional_paths:
    - path: /var/log/trading
      writable: false
    - path: /shared
      writable: false
  optional_env:
    - TELEGRAM_BOT_TOKEN
    - ALLOWED_CHAT_ID
```

Lecture : à configuration inchangée, l’absence de ces éléments optionnels (variables, ports, chemins) suffit à expliquer `ENV=WARN`, `PORTS=WARN`, `PATHS=WARN` même si aucun FAIL n’existe.

