---
doc_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_MACHINE_RUNTIME_MAP_01_INBOX
doc_type: inbox
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_MACHINE_RUNTIME_MAP_01
parent_go: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_01
status: active
lifecycle_stage: impl
surface: index
source_kind: canonical
created_at: 2026-05-19
updated_at: 2026-05-19
links:
  - config/machine_runtime_map.yml
  - modules/runtime_health/machine_map.py
  - modules/runtime_health/fleet_orchestrator.py
  - modules/runtime_health/healthcheck.py
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_MACHINE_RUNTIME_MAP_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_MACHINE_RUNTIME_MAP_01

## Objet

Map multi-machine pour le Runtime Health Supervisor. Chaque machine ne verifie
que son scope declare. Forbidden services detectes. Fleet orchestrator agregateur.

## Livrables crees

- `config/machine_runtime_map.yml` — 5 machines : admin-trading, db-layer, cursor-ai, fantome, student
- `modules/runtime_health/machine_map.py` — MachineMap loader, scope resolver, forbidden checks
- `modules/runtime_health/fleet_orchestrator.py` — collecte SSH/SSHFS/local, fleet_status.json
- `modules/runtime_health/healthcheck.py` — +--machine +--map +MACHINE_IDENTITY +FORBIDDEN_SERVICES
- `scripts/runtime_healthcheck.sh` — +MACHINE_ROLE env +--map +PYTHONPATH

## Prochaine etape

Tester depuis chaque machine : `bash scripts/runtime_healthcheck.sh --dry-run`.
Puis deployer le timer sur admin-trading et activer la collection fleet.
