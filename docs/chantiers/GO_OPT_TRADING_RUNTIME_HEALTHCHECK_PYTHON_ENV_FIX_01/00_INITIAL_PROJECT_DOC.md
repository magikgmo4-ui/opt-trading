---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PARENT_GO_ID: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
PF_ID: null
MASTER_TARGET_ID: null
MASTER_PROJECT_PLAN_ID: null
status: active
lifecycle_stage: fix
surface: runtime_health
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/56_STRICT_READ_ONLY_VALIDATION_RESULTS_1_10.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/90_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01/50_POST_DEPLOY_VALIDATION_RESULTS.md
  - scripts/runtime_healthcheck.sh
  - deploy/systemd/opt-trading-runtime-health.service
---

# GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01

## Objectif

Corriger durablement le warning STEP 5 issu de la validation runtime strict
read-only 1 a 10.

Etat source :

```text
STRICT_READ_ONLY_1_10 = PASS_WITH_WARNINGS
STEP_5 = WARN
NEXT_FIX_GO = GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
```

## Cause canonique

`opt-trading-runtime-health.service` lance
`/opt/trading/scripts/runtime_healthcheck.sh`. Le wrapper choisissait le premier
Python executable, donc `/opt/trading/venv/bin/python3` en priorite. La preuve
runtime indique que ce venv ne charge pas PyYAML, alors que `/usr/bin/python3`
charge PyYAML 6.0.1.

Effet : le runtime healthcheck peut perdre la machine map YAML et maintenir
STEP 5 en `WARN`.

## Cible

Transformer uniquement ce gap :

```text
STEP_5 = WARN
```

en :

```text
STEP_5 = PASS
```

Les autres warnings restent hors scope :

- hygiene repo distante
- allowlist Telegram vide
- smoke mobile reel non prouve

## Scope

Surfaces autorisees :

- `scripts/runtime_healthcheck.sh`
- `docs/chantiers/GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01/`

Surfaces non modifiees :

- index globaux
- parent umbrella
- secrets
- stash
- watchdog 11-12
- dependances systeme ou venv installees directement

## Decision

Le wrapper selectionne maintenant un Python par capacite : le candidat doit
pouvoir executer `import yaml`. L'ordre reste volontairement simple :

```text
/opt/trading/venv/bin/python3
/usr/bin/python3
python3
```

Si aucun candidat ne peut importer `yaml`, le wrapper echoue explicitement au
lieu de produire un healthcheck degrade.

## Resultat post-deploiement

```text
GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01 = DEPLOYED_VALIDATED
STEP_5_PYTHON_PYYAML_BLOCKER = CLOSED
STEP_5_FINAL = WARN_RESIDUAL_ENV_PORTS_PATHS_STALE_MACHINES
NEXT_GO = GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01
```

La validation distante sur `db-layer` prouve que le service systemd utilise un
Python capable d'importer `yaml` et sort en `status=0/SUCCESS`. Le `WARN`
restant ne vient plus du mismatch Python/PyYAML.
