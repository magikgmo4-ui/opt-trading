---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01_REPRISE
doc_type: reprise
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-26
---

# 90_REPRISE

## Etat

Chantier ouvert pour corriger le warning STEP 5 du GO parent operationnel :

```text
GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
```

Le patch local aligne les wrappers systemd runtime health sur un principe
simple : choisir un Python capable d'importer `yaml` avant de lancer les
binaires runtime health.

Wrappers couverts :

- `scripts/runtime_healthcheck.sh` (healthcheck.py)
- `scripts/fleet_orchestrator.sh` (fleet_orchestrator.py)

## Statut attendu

```text
STEP_5_SOURCE = WARN
PATCH_TARGET = STEP_5_PYTHON_PYYAML_BLOCKER_REDUCED
CHILD_GO_STATUS = PATCH_READY
RUNTIME_DEPLOY = NOT_PROVEN
STEP_5_FINAL = PENDING_RUNTIME_REPLAY
NEXT_GO = PR_CHILD_GO
GLOBAL_INDEX_UPDATE = NOT_REQUIRED
WATCHDOG_11_12 = NOT_RUN
PARENT_UMBRELLA = NOT_CLOSED
```

## Surfaces modifiees

- `scripts/runtime_healthcheck.sh`
- `scripts/fleet_orchestrator.sh`
- `docs/chantiers/GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01/`

## Validation locale

Executee localement le 2026-05-26 :

```text
git diff --check = PASS
"C:\Program Files\Git\bin\bash.exe" -n scripts/runtime_healthcheck.sh = PASS
python -m pytest tests/runtime_health/test_warn_classification.py tests/runtime_health/test_cursor_ai_windows.py -q -p no:cacheprovider = 46 passed
```

## Validation distante restante

Non executee dans ce GO :

```text
STATUS = NOT_PROVEN
```

Ne pas lancer watchdog 11-12.

## Gaps conserves

- hygiene repo distante ;
- allowlist Telegram vide ;
- smoke mobile reel non prouve.
