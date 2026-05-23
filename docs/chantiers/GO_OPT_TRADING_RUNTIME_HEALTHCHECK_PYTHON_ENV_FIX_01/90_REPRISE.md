---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01_REPRISE
doc_type: reprise
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE

## Etat

Chantier ouvert pour corriger le warning STEP 5 du GO parent operationnel :

```text
GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
```

Le patch local modifie `scripts/runtime_healthcheck.sh` pour choisir un Python
capable d'importer `yaml` avant de lancer `modules/runtime_health/healthcheck.py`.

Le patch est maintenant merge et valide sur `db-layer` contre le blocage
Python/PyYAML.

## Statut attendu

```text
STEP_5_SOURCE = WARN
PATCH_TARGET = STEP_5_PYTHON_PYYAML_BLOCKER_CLOSED
GO_STATUS = DEPLOYED_VALIDATED
STEP_5_FINAL = WARN_RESIDUAL_ENV_PORTS_PATHS_STALE_MACHINES
NEXT_GO = GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01
GLOBAL_INDEX_UPDATE = NOT_REQUIRED
WATCHDOG_11_12 = NOT_RUN
PARENT_UMBRELLA = NOT_CLOSED
```

## Surfaces modifiees

- `scripts/runtime_healthcheck.sh`
- `docs/chantiers/GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01/`

## Validation locale

Executee localement le 2026-05-23 :

```text
git diff --check = PASS
"C:\Program Files\Git\bin\bash.exe" -n scripts/runtime_healthcheck.sh = PASS
python -m pytest tests\runtime_health\test_warn_classification.py tests\runtime_health\test_cursor_ai_windows.py -q -p no:cacheprovider = 45 passed
```

## Validation distante restante

Executee apres merge/deploy sur `db-layer` :

```text
bash -n scripts/runtime_healthcheck.sh = PASS
bash scripts/runtime_healthcheck.sh --dry-run --no-telegram = OK
opt-trading-runtime-health.service relance par timer = status=0/SUCCESS
python3 modules/runtime_health/fleet_orchestrator.py --map config/machine_runtime_map.yml --dry-run = WARN_RESIDUAL
```

Ne pas lancer watchdog 11-12.

Details :

```text
db-layer latest.json timestamp = 2026-05-23T20:37:37+00:00
db-layer overall_status = WARN
failing = []
unreachable = []
stale_machines = cursor-ai, fantome
WARN blocks = ENV, PORTS, PATHS
```

Conclusion : STEP 5 n'est plus bloque par Python/PyYAML. Le STEP 5 global
reste `WARN_RESIDUAL` et doit etre traite dans
`GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01`.

## Gaps conserves

- hygiene repo distante ;
- allowlist Telegram vide ;
- smoke mobile reel non prouve.
- runtime healthcheck residuel : `ENV`, `PORTS`, `PATHS`, `stale_machines`.

## Support Git distant

`db-layer` n'a pas ete realigne sur le nom de branche `sot/mainline`, car la
verification a montre un commit local unique :

```text
branch = go/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
HEAD = 1a8d49a5
origin/sot/mainline = a02e5b24
origin/sot/mainline..HEAD = 1a8d49a5 feat(data_center): ouvrir parent PF_DATA_CENTER avec contrats producers/consumers et module layout
```

Decision : ne pas deplacer cette branche tant que ce commit n'est pas arbitre.
