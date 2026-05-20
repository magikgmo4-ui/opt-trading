# GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01 — 20_CLASSIFICATION_REVIEW

## 1_CANONICAL_CLASSIFICATION

| Sous-famille | Surfaces | Classement |
|---|---|---|
| Workflows strict-workers validation | `strict-workers-validate.yml` | Bucket 1, car validation read-only du plan de travail strict-workers |
| Workflows strict-workers smoke | `strict-workers-smoke.yml` | Bucket 1, car preuve dry-run sans write runtime |
| Workflows strict-workers schedule | `strict-workers-schedule.yml` | Hors scope ici, bucket 2 planification et periodicite |
| Unites `systemd` fleet/runtime | `deploy/systemd/opt-trading-fleet-orchestrator.*`, `opt-trading-runtime-health.*` | Bucket 1, car orchestration/deploiement runtime |
| Overrides machine | `deploy/systemd/overrides/*` | Bucket 1, car adaptation deploiement par machine |
| Carte machine/runtime | `config/machine_runtime_map.yml` | Bucket 1, car source canonique de separation des roles runtime |
| Modules avec surface `systemd` | `modules/*/systemd/*` | Bucket 1 comme surfaces adjacentes a raccorder, sans revoir leur code applicatif |

## 2_REVIEW_NOTES

### Workflows

- `strict-workers-validate.yml` est borne a la validation de packets et ne porte pas l'orchestration runtime.
- `strict-workers-smoke.yml` reste dans le bucket 1 car il exerce une preuve de non-modification et un dry-run controlle.
- `strict-workers-schedule.yml` reste explicitement separe pour eviter de melanger orchestration/deploiement et periodicite.

### Deploy systemd

- `opt-trading-fleet-orchestrator.*` et `opt-trading-runtime-health.*` sont les surfaces de deploiement les plus directes du bucket 1.
- Les overrides `fantome` et `student` montrent une adaptation machine-specifique limitee a l'identite d'execution, ce qui confirme leur classement dans le meme bucket.

### Machine runtime map

- `config/machine_runtime_map.yml` agit comme table de verite pour l'allocation des services, timers, ports et interdictions par machine.
- La presence de `admin-trading`, `db-layer`, `cursor-ai`, `fantome` et `student` confirme que cette surface est de coordination runtime, pas une surface strategy/apps.

### Modules systemd adjacents

- Les services/timers modules sont des consommateurs ou voisins du canon de deploiement.
- Ils doivent etre cites dans la revue bucket 1 pour prouver l'etendue des dependances, mais sans glisser vers une reclassification fonctionnelle de chaque module.

## 3_EXPLICIT_OUT_OF_SCOPE

- `modules/strategy/*` et `tools/strategy/validate_strategy_registry.py`
- `modules/airtable_bridge/*`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_*`
- `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_*`
- `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_*`
- toute modification de workflow, unit file, timer, override ou runtime map

## 4_NEXT_GO_EDGE

Si une suite est ouverte apres validation de cette revue, elle peut se separer en deux lignes:

1. `GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_*` pour modifications repo des artefacts `systemd`/workflows.
2. `GO_OPT_TRADING_MACHINE_RUNTIME_MAP_ALIGNMENT_*` pour evolution du canon machine/runtime sans toucher aux buckets strategy/apps.
