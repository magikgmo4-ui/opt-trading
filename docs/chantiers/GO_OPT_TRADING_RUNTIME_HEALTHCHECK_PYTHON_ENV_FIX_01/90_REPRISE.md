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

## Statut attendu

```text
STEP_5_SOURCE = WARN
PATCH_TARGET = STEP_5_PASS_AFTER_REMOTE_VALIDATION
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

Apres merge/deploy sur `db-layer` :

```text
bash scripts/runtime_healthcheck.sh --dry-run --no-telegram
systemctl status opt-trading-runtime-health.service --no-pager
python3 modules/runtime_health/fleet_orchestrator.py --dry-run --no-telegram
```

Ne pas lancer watchdog 11-12.

## Gaps conserves

- hygiene repo distante ;
- allowlist Telegram vide ;
- smoke mobile reel non prouve.
