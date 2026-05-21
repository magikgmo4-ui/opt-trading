---
doc_id: GO_HITL_APPROVAL_GATES_01_INITIAL
doc_type: initial_project_doc
go_id: GO_HITL_APPROVAL_GATES_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-21
links:
  - configs/openclaw/security/skill_policy.yaml
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01/A4_WRITE_GATE_POLICY.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_EXTERNAL_APPS_ORCHESTRATION_RUNNER_01/50_SECURITY_AND_STOP_CONDITIONS.md
---

# GO_HITL_APPROVAL_GATES_01

## Objectif

Pipeline HITL complet : propose → review → approve → execute → verify → log (GAP_07 du parent).

## Périmètre

- Proposal packet (format, champs, validation)
- Approval packet (approbateur, signature, conditions)
- Execution packet (commande, dry-run, rollback)
- Verification packet (résultat, statut, preuve)
- Approver roles (humain, manager AI)
- Dual confirm pour actions sensibles
- Write-gated test

## Preuve concrète pour l'ouverture

- `skill_policy.yaml` définit des niveaux de permission (L0-L8) mais le pipeline HITL complet n'existe pas
- `A4_WRITE_GATE_POLICY.md` définit les règles de refus mais pas le circuit complet propose→execute
- `PERMISSION_MATRIX_01.md` définit les surfaces et niveaux mais pas le packet HITL

## Livrables

- Proposal packet schema
- Approval packet schema
- Execution packet schema
- Verification packet schema
- Roles approvers définis
- Dual confirm policy
- Write-gated test

## Exclusions

- Implémentation runtime des approvals (UI/backend)
- Déploiement systemd
