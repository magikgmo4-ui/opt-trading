---
doc_id: GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
point_de_reprise: "MATRIX_DRAFT"
created_at: 2026-05-21
links:
  - config/machine_runtime_map.yml
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/10_GAPS_REGISTER.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/50_PREPARED_MATRIX.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01.md
  - scripts/ai/workers/tasks.index.json
  - configs/openclaw/security/skill_policy.yaml
---

# GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01

## Objectif

Produire la matrice consolidée `actor × surface × permission × gate × log × rollback` manquante (GAP_01 du parent `GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01`).

Chaque intersection doit avoir une permission, une gate, un statut et une preuve vérifiable. La matrice doit être testée sur 3 scénarios minimum.

## Périmètre

- Acteurs : humain, OpenClaw, strict_worker, team_ai_manager, specialist_worker, app_bridge
- Surfaces : repo, tmux, Telegram, TradingView, Airtable, ClickUp, Botpress, Sheets, LocalCMS, DeskPro
- Permissions : read, draft, patch_draft, write_gated, forbidden
- Gates : none, dry_run, human_approve, dual_confirm

## Preuve concrète pour l'ouverture

Le mismatch `opt-trading-fleet-orchestrator.timer` absent de `config/machine_runtime_map.yml` (PR #661) établit une preuve concrète sur la surface `machine_runtime_map.yml`, conforme à la règle d'ouverture.

## Livrables

- `10_CAPABILITY_MATRIX.md` — matrice complète actor × surface × permission × gate
- Preuves par intersection (evidence_ref)
- 3 scénarios de validation :
  1. read-only signal (strict_worker → Telegram)
  2. draft patch repo (specialist_worker → repo)
  3. app external write gated (app_bridge → Airtable)

## Règles

- READ_ONLY par défaut pour tout agent non promu
- WRITE_GATED seulement après gate validée
- FORBIDDEN pour les actions explicitement interdites
- Toute intersection sans preuve reste OPEN
- Matrice versionnée et traçable par evidence_ref

## Références préparatoires

La consolidation préparatoire est dans le parent :
`docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/50_PREPARED_MATRIX.md`

Sources existantes :
- L0-L8 permission matrix (OpenClaw Security)
- Autonomy levels A0-A4 (Strict Workers)
- Tasks index (8 task types)
- Skill policy YAML (machine-readable)
- UI surfaces registry
