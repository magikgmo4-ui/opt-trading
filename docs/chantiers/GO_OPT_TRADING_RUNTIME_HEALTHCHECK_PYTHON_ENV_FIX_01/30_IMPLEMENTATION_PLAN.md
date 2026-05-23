---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01_IMPLEMENTATION_PLAN
doc_type: implementation_plan
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 30_IMPLEMENTATION_PLAN

## Patch code

Modifier `scripts/runtime_healthcheck.sh` :

1. garder `/opt/trading/venv/bin/python3` comme premier candidat ;
2. supprimer le fallback vers le venv specialise
   `/opt/trading/.venvs/bot_vision_step2/bin/python3` ;
3. tester chaque candidat avec `import yaml` ;
4. choisir le premier candidat compatible ;
5. afficher une erreur explicite si aucun candidat ne peut importer `yaml`.

## Patch docs

Creer le chantier local :

```text
docs/chantiers/GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01/
```

Fichiers :

- `00_INITIAL_PROJECT_DOC.md`
- `10_CURRENT_FAILURE_PROOF.md`
- `20_FIX_OPTIONS.md`
- `30_IMPLEMENTATION_PLAN.md`
- `40_VALIDATION_PLAN.md`
- `90_REPRISE.md`

## Exclusions

- pas de modification des index globaux ;
- pas de fermeture du parent umbrella ;
- pas de modification de secrets ;
- pas de `stash pop` ;
- pas de watchdog 11-12 ;
- pas d'installation directe de PyYAML.
