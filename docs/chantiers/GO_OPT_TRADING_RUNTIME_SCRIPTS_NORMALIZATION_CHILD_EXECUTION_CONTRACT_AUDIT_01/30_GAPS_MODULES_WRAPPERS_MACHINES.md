---
doc_id: RUNTIME_SCRIPTS_NORMALIZATION_EXECUTION_CONTRACT_AUDIT_30
doc_type: GAPS_MODULES_WRAPPERS_MACHINES
repo: opt-trading
project: opt-trading
module: runtime_scripts_normalization
go_id: GO_OPT_TRADING_RUNTIME_SCRIPTS_NORMALIZATION_CHILD_EXECUTION_CONTRACT_AUDIT_01
status: open
lifecycle_stage: audit_doc_only
topic_keys:
  - opt-trading
  - modules
  - wrappers
  - machines
  - coverage
  - gaps
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-31
links:
  - registry/modules_registry.yaml
  - registry/wrappers_registry.yaml
  - registry/machines_registry.yaml
  - config/machine_runtime_map.yml
---

# 30_GAPS_MODULES_WRAPPERS_MACHINES

## Counting note

Les chiffres ci-dessous viennent d'un scan local du working tree le 2026-05-31. Le trunk ZIP inspecte precedemment indiquait environ 110 modules sous `modules/`; le scan local courant trouve 106 dossiers directs. L'ecart ne change pas la conclusion : la couverture registry est partielle et doit etre qualifiee, pas corrigee par renommage immediat.

## Modules coverage

| Controle | Count |
| --- | ---: |
| dossiers directs sous `modules/` | 106 |
| entrees `registry/modules_registry.yaml` | 49 |
| dossiers physiques non enregistres | 57 |
| modules en registry sans dossier physique | 0 |

La registry centrale couvre donc les modules retenus comme fonctionnels, mais pas l'ensemble physique du dossier `modules/`.

## Classification requise

Les modules non enregistres doivent etre classes avant toute mutation :

```text
ACTIVE
EXPERIMENTAL
ARCHIVED
DERIVED
LEGACY
DELETE_CANDIDATE
```

Exemples de dossiers non enregistres a qualifier :

```text
airtable_bridge
auth
bot_vision
bot_vision_step2
collector_binance_spot
collector_coingecko
data_center
deepseek_student
derivatives_collector
execution_engine
git_fleet_guard
governance
health
localcms
model_provider_openclaw
notification_dispatcher
openclaw_tmux_operator
ops_wrappers
perf
repo_hygiene
runtime_health
```

## Wrapper coverage

| Controle | Count |
| --- | ---: |
| wrappers attendus depuis `wrappers_expected` | 125 |
| wrappers declares dans `wrappers_registry.yaml` | 56 |
| wrappers declares qui matchent un attendu | 53 |
| wrappers attendus manquants | 72 |
| wrappers declares hors attentes actuelles | 3 |

Les trois wrappers declares hors attentes actuelles sont la famille `reseau_ssh_step2` :

```text
cmd-reseau_ssh_step2
menu-reseau_ssh_step2
sanity-reseau_ssh_step2
```

Ils ne doivent pas etre supprimes dans ce lot. Ils doivent etre qualifies : module attendu absent, legacy tolere, ou registry module a completer.

## Missing wrappers sample

Exemples de wrappers attendus mais non declares :

```text
cmd-configure_openclaw
cmd-desk_analyze
cmd-desk_capture_inputs
cmd-desk_common
cmd-desk_pro
cmd-desk_pro_orchestrator
cmd-desk_retention
cmd-desk_snapshot_ingest
cmd-desk_state
cmd-gateway_openclaw
cmd-memory_bricks
cmd-openclaw_operator_bridge
cmd-ops_menu_hub
cmd-registry_meta_reader
cmd-registry_router
cmd-vision_bot
menu-desk_pro_runner
menu-gateway_openclaw
sanity-gateway_openclaw
```

Le prochain audit wrapper doit separer :

```text
wrappers attendus
vs wrappers declares
vs scripts reels presents
vs wrappers installes runtime
```

Sans cette matrice, un module peut sembler actif en registry sans etre operable par l'operateur.

## Machine naming divergence

Deux modeles coexistent.

### Registry identity model

| `machine_id` | `hostname` | Role |
| --- | --- | --- |
| `admin_trading` | `admin-trading` | backend / orchestration |
| `msi_db_layer` | `db-layer` | operator UI / dashboards |
| `dell_cursor_ai` | `dell-cursor-ai` | dev station |
| `student` | `student` | auxiliary AI |
| `debian_network_future` | `debian-network` | future network placeholder |

### Runtime map keys

```text
admin-trading
db-layer
cursor-ai
fantome
student
```

## Machine gap table

| Registry machine | Runtime map state | Decision draft |
| --- | --- | --- |
| `admin_trading` / `admin-trading` | key exists as `admin-trading` | OK via hostname/runtime key |
| `msi_db_layer` / `db-layer` | key exists as `db-layer` | OK via hostname/runtime key |
| `dell_cursor_ai` / `dell-cursor-ai` | runtime key is `cursor-ai` | needs alias model |
| `student` / `student` | key exists as `student` | OK |
| `debian_network_future` / `debian-network` | no runtime key | keep as future placeholder or mark not deployed |
| no registry identity | runtime key `fantome` | add identity or classify external/secondary |

## Machine model proposal

Ne pas choisir arbitrairement entre snake_case et hyphen-case.

Modele recommande :

```yaml
machine_id: admin_trading
hostname: admin-trading
aliases:
  - admin-trading
runtime_map_key: admin-trading
```

Pour `cursor-ai`, la future entree devrait rendre explicite le pont :

```yaml
machine_id: dell_cursor_ai
hostname: dell-cursor-ai
aliases:
  - cursor-ai
  - DESKTOP-1KDQTBH
runtime_map_key: cursor-ai
```

Pour `fantome`, il faut choisir entre :

- ajouter une machine registry canonique;
- ou marquer `fantome` comme projection runtime externe/secondaire non registry.

## Non-actions in this GO

Ce GO ne doit pas :

- ajouter les modules manquants a `modules_registry.yaml`;
- ajouter les wrappers manquants a `wrappers_registry.yaml`;
- renommer les machines;
- modifier `machine_runtime_map.yml`;
- installer ou supprimer des wrappers;
- corriger les scripts physiques.

Le seul livrable attendu ici est la preuve structurante pour le GO d'implementation suivant.
