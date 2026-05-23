---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01_CURRENT_FAILURE_PROOF
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_CURRENT_FAILURE_PROOF

## Source

Preuve publiee via PR #740 dans :

```text
docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/56_STRICT_READ_ONLY_VALIDATION_RESULTS_1_10.md
```

## Lecture canonique

```text
STEP 5 = WARN
surface = fleet/runtime health
gateway = non incrimine
service = opt-trading-runtime-health.service
timer = present
wrapper = /opt/trading/scripts/runtime_healthcheck.sh
```

## Cause observee

```text
wrapper choisit /opt/trading/venv/bin/python3 en priorite
/opt/trading/venv/bin/python3 ne charge pas PyYAML
/usr/bin/python3 charge PyYAML 6.0.1
```

## Impact

`modules/runtime_health/machine_map.py` charge `config/machine_runtime_map.yml`
avec PyYAML. Sans `yaml`, la map devient vide et le healthcheck peut perdre le
scope machine attendu.

Le risque n'est pas OpenClaw ni le gateway. Le risque est un environnement
Python systemd/wrapper incoherent.

## Hors cause

- OpenClaw probe : PASS
- gateway : joignable
- tmux `db-layer` : PASS
- tmux `admin-trading` : PASS
- watchdog 11-12 : non execute volontairement
