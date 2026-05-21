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
|---|---|---|---|---|---|---|---|---|
| M01 | humain | repo | write_gated | human_approve | true | true | | OPEN |
| M02 | humain | Telegram | write_gated | human_approve | true | false | | OPEN |
| M03 | humain | TradingView | read | none | true | false | | OPEN |
| M04 | humain | DeskPro | write_gated | human_approve | true | true | | OPEN |
| M05 | humain | LocalCMS | write_gated | human_approve | true | true | | OPEN |
| M06 | OpenClaw | repo | patch_draft | dry_run | true | true | | OPEN |
| M07 | OpenClaw | Telegram | read | none | true | false | | OPEN |
| M08 | OpenClaw | tmux | read | none | true | false | | OPEN |
| M09 | OpenClaw | Airtable | read | none | true | false | | OPEN |
| M10 | OpenClaw | LocalCMS | read | none | true | false | | OPEN |
| M11 | strict_worker | repo | read | none | true | false | | OPEN |
| M12 | strict_worker | Telegram | read | none | true | false | | OPEN |
| M13 | strict_worker | tmux | read | none | true | false | | OPEN |
| M14 | strict_worker | TradingView | read | none | true | false | | OPEN |
| M15 | team_ai_manager | repo | patch_draft | human_approve | true | true | | OPEN |
| M16 | team_ai_manager | Telegram | write_gated | human_approve | true | true | | OPEN |
| M17 | team_ai_manager | LocalCMS | patch_draft | human_approve | true | true | | OPEN |
| M18 | specialist_worker | repo | patch_draft | dry_run | true | true | | OPEN |
| M19 | specialist_worker | Telegram | read | none | true | false | | OPEN |
| M20 | specialist_worker | tmux | read | none | true | false | | OPEN |
| M21 | app_bridge | Airtable | write_gated | human_approve | true | true | | OPEN |
| M22 | app_bridge | ClickUp | write_gated | human_approve | true | true | | OPEN |
| M23 | app_bridge | Botpress | write_gated | human_approve | true | true | | OPEN |
| M24 | app_bridge | Sheets | read | none | true | false | | OPEN |
| M25 | app_bridge | Telegram | read | none | true | false | | OPEN |
| M26 | app_bridge | Gmail | write_gated | human_approve | true | true | | OPEN |
| M27 | app_bridge | Calendar | read | none | true | false | | OPEN |
| M28 | app_bridge | Drive | write_gated | human_approve | true | true | | OPEN |
| M29 | app_bridge | Figma | read | none | true | false | | OPEN |
| M30 | app_bridge | LocalCMS | patch_draft | dry_run | true | true | | OPEN |

## Scénarios de validation

| # | Scénario | Acteur | Surface | Permission | Gate | Critère de succès |
|---|---|---|---|---|---|---|
| S1 | read-only signal | strict_worker | Telegram | read | none | Extraction de signal sans write, log produit |
| S2 | draft patch repo | specialist_worker | repo | patch_draft | dry_run | Patch proposé sans write, diff vérifiable, rollback défini |
| S3 | app external write gated | app_bridge | Airtable | write_gated | human_approve | Write bloqué sans approbation, passant avec |

## Règles d'inférence

- Toute ligne non renseignée en evidence_ref est `OPEN`
- Le passage de `OPEN` à `PASS_WITH_EVIDENCE` nécessite :
  - evidence_ref non vide
  - test ou preuve exécuté
  - gate respectée
  - log produit
- `forbidden` prime sur toute autre permission
