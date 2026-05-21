---
doc_id: GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01_MATRIX
doc_type: capability_matrix
go_id: GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: draft
lifecycle_stage: impl
---

# 10_CAPABILITY_MATRIX — actor × surface × permission × gate

## Structure

Chaque ligne définit une intersection `actor_id × surface_id` avec :
- permission : read, draft, patch_draft, write_gated, forbidden
- gate : none, dry_run, human_approve, dual_confirm
- log_required : true / false
- rollback_required : true / false
- evidence_ref : chemin ou artefact
- status : OPEN / PARTIAL / PASS_WITH_EVIDENCE

## Matrice

| # | actor_id | surface_id | permission | gate | log | rollback | evidence_ref | status |
|---|---|---|---|---|---|---|---|---|---|
| M01 | humain | repo | write_gated | human_approve | true | true | `PERMISSION_MATRIX_01.md` L4+ REPO_CODE; `A4_WRITE_GATE_POLICY.md` | PARTIAL |
| M02 | humain | Telegram | write_gated | human_approve | true | false | `PERMISSION_MATRIX_01.md` L2 TELEGRAM default; humain override to L4+ | PARTIAL |
| M03 | humain | TradingView | read | none | true | false | `webhook_server.py`; `tradingview/` adapters exist | PARTIAL |
| M04 | humain | DeskPro | write_gated | human_approve | true | true | `ui_surfaces_registry.yaml` desk_pro surfaces; `modules/desk_pro/systemd/` | PARTIAL |
| M05 | humain | LocalCMS | write_gated | human_approve | true | true | `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` LocalCMS consumer | PARTIAL |
| M06 | OpenClaw | repo | patch_draft | dry_run | true | true | `agent_model_matrix.yaml` orchestrateur; `STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` | PARTIAL |
| M07 | OpenClaw | Telegram | read | none | true | false | Telegram bot infrastructure (env vars, adapters) | PARTIAL |
| M08 | OpenClaw | tmux | read | none | true | false | `machine_runtime_map.yml` admin-trading optional_tmux_sessions: openclaw | PARTIAL |
| M09 | OpenClaw | Airtable | read | none | true | false | `modules/airtable_bridge/` exists | PARTIAL |
| M10 | OpenClaw | LocalCMS | read | none | true | false | LocalCMS infrastructure (urls, routes) | PARTIAL |
| M11 | strict_worker | repo | read | none | true | false | `STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` A1 READ_INVENTORY; `tasks.index.json` READ_INVENTORY | PARTIAL |
| M12 | strict_worker | Telegram | read | none | true | false | `tasks.index.json` READ_INVENTORY task type; Telegram adapter | PARTIAL |
| M13 | strict_worker | tmux | read | none | true | false | `machine_runtime_map.yml` sessions tmux; `STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` A1 | PARTIAL |
| M14 | strict_worker | TradingView | read | none | true | false | TradingView webhook infra; strict_worker A1 READ_ONLY | PARTIAL |
| M15 | team_ai_manager | repo | patch_draft | human_approve | true | true | `10_ROLES_JOBS_TASKS_INVENTORY.md` Manager A4 (HITL); patch capability | PARTIAL |
| M16 | team_ai_manager | Telegram | write_gated | human_approve | true | true | `10_ROLES_JOBS_TASKS_INVENTORY.md` Manager role with HITL gate | PARTIAL |
| M17 | team_ai_manager | LocalCMS | patch_draft | human_approve | true | true | `10_ROLES_JOBS_TASKS_INVENTORY.md` Manager A4 with human validation | PARTIAL |
| M18 | specialist_worker | repo | patch_draft | dry_run | true | true | `10_ROLES_JOBS_TASKS_INVENTORY.md` Specialists A2; `tasks.index.json` PATCH_DRAFT | PARTIAL |
| M19 | specialist_worker | Telegram | read | none | true | false | `10_ROLES_JOBS_TASKS_INVENTORY.md` Specialists A2 read capability | PARTIAL |
| M20 | specialist_worker | tmux | read | none | true | false | `10_ROLES_JOBS_TASKS_INVENTORY.md` Specialists A2; tmux sessions per map | PARTIAL |
| M21 | app_bridge | Airtable | write_gated | human_approve | true | true | `modules/airtable_bridge/`; `10_GAPS_REGISTER.md` APP_BRIDGE_CONTRACT template | PARTIAL |
| M22 | app_bridge | ClickUp | write_gated | human_approve | true | true | `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` ClickUp validated | PARTIAL |
| M23 | app_bridge | Botpress | write_gated | human_approve | true | true | `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` Botpress validated | PARTIAL |
| M24 | app_bridge | Sheets | read | none | true | false | `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` Sheets operational | PARTIAL |
| M25 | app_bridge | Telegram | read | none | true | false | Telegram bot adapters; app_bridge read-only by default | PARTIAL |
| M26 | app_bridge | Gmail | write_gated | human_approve | true | true | `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` planned surface | PARTIAL |
| M27 | app_bridge | Calendar | read | none | true | false | `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` planned surface | PARTIAL |
| M28 | app_bridge | Drive | write_gated | human_approve | true | true | `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` planned surface | PARTIAL |
| M29 | app_bridge | Figma | read | none | true | false | `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` planned surface | PARTIAL |
| M30 | app_bridge | LocalCMS | patch_draft | dry_run | true | true | `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` LocalCMS consumer; patch by dry-run | PARTIAL |

## Scénarios de validation

| # | Scénario | Acteur | Surface | Permission | Gate | Critère de succès | Evidence |
|---|---|---|---|---|---|---|---|---|
| S1 | read-only signal | strict_worker | Telegram | read | none | Extraction de signal sans write, log produit | _pending_ |
| S2 | draft patch repo | specialist_worker | repo | patch_draft | dry_run | Patch proposé sans write, diff vérifiable, rollback défini | _pending_ |
| S3 | app external write gated | app_bridge | Airtable | write_gated | human_approve | Write bloqué sans approbation, passant avec | _pending_ |

## Règles d'inférence

- Toute ligne non renseignée en evidence_ref est `OPEN`
- Le passage de `OPEN` à `PASS_WITH_EVIDENCE` nécessite :
  - evidence_ref non vide
  - test ou preuve exécuté
  - gate respectée
  - log produit
- `forbidden` prime sur toute autre permission
