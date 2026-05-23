---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01_VALIDATION_PLAN
doc_type: validation_plan
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 40_VALIDATION_PLAN

## Validation locale read-only

```powershell
git diff --check
& "C:\Program Files\Git\bin\bash.exe" -n scripts/runtime_healthcheck.sh
python -m pytest tests\runtime_health\test_warn_classification.py tests\runtime_health\test_cursor_ai_windows.py -q
```

## Validation runtime distante a executer apres deploy

Ne pas lancer watchdog 11-12.

```bash
ssh db-layer 'cd /opt/trading && bash scripts/runtime_healthcheck.sh --dry-run --no-telegram'
ssh db-layer 'systemctl status opt-trading-runtime-health.service --no-pager'
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run --no-telegram'
```

## Critere de requalification

STEP 5 peut passer de `WARN` a `PASS` uniquement si :

- le wrapper choisit un Python capable d'importer `yaml` ;
- `runtime_healthcheck.sh --dry-run --no-telegram` sort sans erreur Python/env ;
- `opt-trading-runtime-health.service` n'affiche plus l'erreur PyYAML/wrapper ;
- le run fleet/runtime health ne met plus STEP 5 en WARN pour cette cause.

Les autres warnings ne doivent pas etre masques.

## Validation post-deploiement executee

Resultat du 2026-05-23 sur `db-layer` :

```text
STEP_5_PYTHON_PYYAML_BLOCKER = CLOSED
STEP_5_FINAL = WARN_RESIDUAL_ENV_PORTS_PATHS_STALE_MACHINES
```

Les criteres lies au fix Python/PyYAML sont satisfaits :

- wrapper syntaxe OK ;
- dry-run sans erreur Python/env ;
- service systemd relance par timer en `status=0/SUCCESS` ;
- `/usr/bin/python3` observe comme Python effectif du healthcheck ;
- fleet dry-run sans `FAIL` ni machine unreachable.

Les criteres de `PASS_FULL` ne sont pas satisfaits car les warnings residuels
restent a traiter dans un GO separe.
