---
doc_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01_INITIAL
doc_type: initial_project_doc
go_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-21
links:
  - configs/openclaw/security/skill_policy.yaml
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01/A4_WRITE_GATE_POLICY.md
  - config/machine_runtime_map.yml
---

# GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01

## Objectif

Consolider la politique de sécurité : inventaire des secrets, stockage, scopes OAuth, rotation, kill switch, deny-by-default, tests anti-secret (GAP_08 du parent).

## Périmètre

- Inventaire des secrets (tokens, clés, credentials)
- Politique de stockage des secrets (env vars, fichiers, vault)
- Scopes OAuth par app
- Rotation policy
- Kill switch (coupe-circuit général)
- Deny-by-default (principe)
- Tests anti-secret (détection de fuite)

## Preuve concrète pour l'ouverture

- `skill_policy.yaml` : politique sécurité existante en mode WARNING_ONLY sans kill switch ni rotation
- `machine_runtime_map.yml` : required_env/optional_env listés sans politique de rotation
- `A4_WRITE_GATE_POLICY.md` : règles de refus existantes sans inventaire secrets global

## Livrables

- Inventaire des secrets
- Politique de stockage documentée
- Scopes OAuth par app définis
- Rotation policy
- Kill switch design
- Deny-by-default policy
- Tests anti-secret
