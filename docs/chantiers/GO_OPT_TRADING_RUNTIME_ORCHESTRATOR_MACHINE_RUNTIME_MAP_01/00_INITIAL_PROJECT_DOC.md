---
doc_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_MACHINE_RUNTIME_MAP_01_INITIAL
doc_type: chantier
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_MACHINE_RUNTIME_MAP_01
parent_go: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_01
status: active
lifecycle_stage: impl
created_at: 2026-05-19
updated_at: 2026-05-19
---

# GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_MACHINE_RUNTIME_MAP_01

## Objectif

Ajouter une map multi-machine au Runtime Health Supervisor.
Chaque machine doit vérifier uniquement son scope déclaré, pas l'état brut local.

## Architecture cible

```
machine_runtime_map.yml
  -> machine_map.py (résolution scope + forbidden_services)
    -> healthcheck.py (branché sur le scope machine)
      -> MACHINE_IDENTITY block
      -> FORBIDDEN_SERVICES block
      -> checks scopés par machine

fleet_orchestrator.py
  -> collecte les latest.json de chaque machine (sshfs → ssh → local)
  -> produit fleet_status.json + fleet_status.jsonl
```

## Machines déclarées

| Machine       | Rôle              | Services requis                                        |
|---------------|-------------------|-------------------------------------------------------|
| admin-trading | runtime_primary   | tv-webhook, tv-perf, bot_vision_step2                 |
| db-layer      | data_layer        | shared-sshfs, daily-session                           |
| cursor-ai     | ide_patch_operator| aucun service requis                                  |
| fantome       | secondary_operator| aucun service requis                                  |
| student       | sandbox_learning  | aucun service requis                                  |

## Règles d'invariant

- Une machine vérifie uniquement son scope déclaré.
- FAIL si required down.
- WARN si optional down.
- FAIL si forbidden actif.
- WARN si machine inconnue de la map.
- Aucun restart automatique (Phase 1).
- Aucun secret dans les outputs.
- Aucun auto-trade.

## Livrables

- `config/machine_runtime_map.yml` — map canonique fleet
- `modules/runtime_health/machine_map.py` — loader + scope resolver + forbidden check
- `modules/runtime_health/fleet_orchestrator.py` — agrégateur fleet
- `modules/runtime_health/healthcheck.py` — modifié pour --machine, --map, MACHINE_IDENTITY, FORBIDDEN_SERVICES
- `scripts/runtime_healthcheck.sh` — modifié pour MACHINE_ROLE + --map

## Outputs runtime

- `/opt/trading/data/runtime_health/latest.json` — rapport local par machine
- `/opt/trading/data/runtime_health/healthcheck.jsonl` — journal local
- `/opt/trading/data/runtime_health/fleet_status.json` — statut fleet agrégé
- `/opt/trading/data/runtime_health/fleet_status.jsonl` — journal fleet

## Collection fleet

Stratégie par ordre de préférence :
1. SSHFS partagé : `/shared/<machine>/runtime_health/latest.json`
2. SSH pull : `ssh <machine> cat /opt/trading/data/runtime_health/latest.json`
3. Local : lecture directe (machine = orchestrateur)

## Phase 2 (future)

Ajouter self-heal allowlist par machine (try-restart uniquement sur services required FAIL).

## RISKS

- À qualifier.
