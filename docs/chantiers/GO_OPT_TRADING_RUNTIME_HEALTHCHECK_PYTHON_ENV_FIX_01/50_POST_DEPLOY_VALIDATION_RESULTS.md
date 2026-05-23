---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01_POST_DEPLOY_VALIDATION_RESULTS
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
status: deployed_validated
source_kind: runtime_evidence
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 50_POST_DEPLOY_VALIDATION_RESULTS

## Contexte

Validation post-deploiement executee sur `db-layer` apres merge PR #744 et pull
du contenu jusqu'au commit `a02e5b24`.

Objectif : verifier que le warning initial STEP 5 lie au mismatch
Python/PyYAML est corrige sans masquer les warnings residuels.

## Verdict

```text
GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01 = DEPLOYED_VALIDATED
STEP_5_PYTHON_PYYAML_BLOCKER = CLOSED
STEP_5_FINAL = WARN_RESIDUAL_ENV_PORTS_PATHS_STALE_MACHINES
NEXT_GO = GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01
```

## Preuves executees

| Surface | Resultat | Lecture |
|---|---|---|
| Pull `db-layer` | PASS | contenu runtime avance jusqu'a `a02e5b24` |
| `bash -n scripts/runtime_healthcheck.sh` | PASS | syntaxe wrapper OK sur `db-layer` |
| `bash scripts/runtime_healthcheck.sh --dry-run --no-telegram` | OK | sortie sans erreur Python/env ; `overall_status=WARN` |
| Timer systemd naturel | PASS | `opt-trading-runtime-health.service` relance par timer, `status=0/SUCCESS` |
| Python selectionne | PASS | service observe avec `/usr/bin/python3 ... healthcheck.py` |
| `fleet_orchestrator.py --map config/machine_runtime_map.yml --dry-run` | WARN_RESIDUAL | `failing=[]`, `unreachable=[]`, fleet status `WARN` |

## Resultat healthcheck `db-layer`

Run systemd naturel :

```text
timestamp = 2026-05-23T20:37:37+00:00
overall_status = WARN
service_status = 0/SUCCESS
```

Block statuses :

```text
MACHINE_IDENTITY = PASS
SYSTEMD_SERVICES = PASS
SYSTEMD_TIMERS = PASS
FORBIDDEN_SERVICES = PASS
VENV = PASS
ENV = WARN
PORTS = WARN
HTTP = PASS
PATHS = WARN
ARTIFACTS = PASS
LOGS = PASS
ORCHESTRATOR = PASS
```

## Resultat fleet STEP 5

```text
fleet_status = WARN
failing = []
unreachable = []
db-layer overall_status = WARN
db-layer stale = false
stale_machines = cursor-ai, fantome
```

Lecture :

- le mismatch Python/PyYAML n'est plus bloquant ;
- `db-layer` n'est plus `FAIL` dans fleet ;
- le `WARN` restant est residuel et porte sur `ENV`, `PORTS`, `PATHS` et
  `stale_machines`;
- STEP 5 ne doit pas etre ferme en `PASS_FULL`.

## Contraintes respectees

- watchdog 11-12 non lance ;
- secrets et untracked distants non touches ;
- aucun index global modifie ;
- parent umbrella non ferme ;
- aucun `stash pop`.

## Support Git `db-layer`

Verification du support Git distant :

```text
branch = go/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
HEAD = 1a8d49a5
origin/sot/mainline = a02e5b24
origin/sot/mainline..HEAD = 1a8d49a5 feat(data_center): ouvrir parent PF_DATA_CENTER avec contrats producers/consumers et module layout
```

Decision : ne pas realigner le nom de branche `db-layer` maintenant, car un
commit local unique existe au-dessus de `origin/sot/mainline`. Les untracked
distants restent hors scope.
