# GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01 — 10_CURRENT_SURFACES

## 1_SCOPE_PROOF

Bucket source: `GO_STRICT_WORKERS_ORCHESTRATION_ET_DEPLOIEMENT` dans `docs/chantiers/GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01/00_classification_matrix.md`.

Etat de reprise valide au moment de l'ouverture:

- `sot/mainline` propre et a jour
- PR #617 mergee
- PR #619 mergee
- PR #645 mergee

## 2_WORKFLOWS_STRICT_WORKERS

### Inclus

- `.github/workflows/strict-workers-validate.yml`
  - validation de tous les job packets JSON sur PR et `workflow_dispatch`
  - permissions `contents: read`
  - aucun write runtime
- `.github/workflows/strict-workers-smoke.yml`
  - dry-run `READ_INVENTORY` sur PR et `workflow_dispatch`
  - garde explicite `Verify no tracked files modified`
  - aucun write runtime

### Exclu

- `.github/workflows/strict-workers-schedule.yml`
  - appartient au bucket 2 `GO_STRICT_WORKERS_PLANIFICATION_ET_GESTION_DES_TACHES`
  - utile comme voisin de frontiere, mais hors scope du present GO

## 3_DEPLOY_SYSTEMD

### Unites fleet/runtime au niveau repo

- `deploy/systemd/opt-trading-fleet-orchestrator.service`
- `deploy/systemd/opt-trading-fleet-orchestrator.timer`
- `deploy/systemd/opt-trading-runtime-health.service`
- `deploy/systemd/opt-trading-runtime-health.timer`

### Overrides machine-specifiques

- `deploy/systemd/overrides/fantome/opt-trading-runtime-health.service.d_override.conf`
- `deploy/systemd/overrides/student/opt-trading-runtime-health.service.d_override.conf`

## 4_MACHINE_RUNTIME_MAP

- `config/machine_runtime_map.yml`
  - machines lues dans l'etat courant: `admin-trading`, `db-layer`, `cursor-ai`, `fantome`, `student`
  - la carte declare services requis/interdits, timers, venvs, ports, paths, variables d'environnement et sessions tmux optionnelles selon machine

## 5_MODULES_SYSTEMD_ADJACENTS

Modules repertories avec surfaces `systemd` dans le repo:

- `modules/vision_bot/systemd/vision_bot.service`
- `modules/shared_sshfs_permanent/systemd/shared-sshfs.service.template`
- `modules/mimo_open_observer/systemd/mimo_open_observer_gate_replay.service`
- `modules/mimo_open_observer/systemd/mimo_open_observer_gate_replay.timer`
- `modules/desk_pro/systemd/desk_pro_dry_run.service`
- `modules/desk_pro/systemd/desk_pro_dry_run.timer`
- `modules/desk_retention/systemd/desk_retention.service`
- `modules/desk_retention/systemd/desk_retention.timer`
- `modules/bot_vision_step2/systemd/bot_vision_step2.service`
- `modules/bot_vision_step2/systemd/bot_vision_step2_send.service`
- `modules/bot_vision_step2/systemd/bot_vision_step2_send.timer`
- `modules/bot_vision_step2/systemd/bot_vision_step2_prune.service`
- `modules/bot_vision_step2/systemd/bot_vision_step2_prune.timer`

Ces surfaces sont inventoriees comme dependances ou voisins de classement, sans extension de scope vers leurs logiques applicatives internes.
