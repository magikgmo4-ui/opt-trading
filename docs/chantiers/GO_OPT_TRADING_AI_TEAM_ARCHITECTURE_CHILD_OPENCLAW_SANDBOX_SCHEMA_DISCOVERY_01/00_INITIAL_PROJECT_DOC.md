---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_SANDBOX_SCHEMA_DISCOVERY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: ai_team_mvp
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_SANDBOX_SCHEMA_DISCOVERY_01
parent_go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
status: open
lifecycle_stage: child_cadrage
surface: chantier
source_kind: canonical_draft
updated_at: 2026-05-12
topic_keys:
  - ai_team
  - openclaw
  - sandbox
  - schema
  - discovery
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_SANDBOX_SCHEMA_DISCOVERY_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section NEXT_GO"
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/17_REMEDIATION_SANDBOX_MODE_SUPPORT_AUDIT.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/18_REMEDIATION_SANDBOX_BLOCKER_REPORT.md
  - modules/openclaw_config_modulaire/app/agents.json5
---

# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_SANDBOX_SCHEMA_DISCOVERY_01

## 3_INITIAL_NEED

La Phase 6 db-layer/OpenClaw remote exec remediation s'est cloturee en REVIEW_REQUIRED parce que `sandbox.mode = "all"` bloque le runtime et qu'aucune valeur supportee de `sandbox.mode` n'est prouvee localement.

## 6_FINAL_TARGET

Decouvrir, documenter et canoniser le schema supporte de `sandbox.mode` avant toute reprise runtime.

## 13_ESTABLISHED

- Child precedent : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01`
- Statut precedent : REVIEW_REQUIRED
- Merge PR : #333
- Merge commit : `215e81c61f4319f674b13b94d8e38382d4cc68ef`
- Runtime OpenClaw : BLOCKED
- Cause principale : SANDBOX_SCHEMA_UNKNOWN
- Fichier observe : `modules/openclaw_config_modulaire/app/agents.json5`
- Valeur observee : `sandbox.mode = "all"`

## 12_INVARIANTS

- Aucun runtime OpenClaw.
- Aucun patch `agents.json5` sans schema prouve.
- Aucune connexion SSH reelle.
- Aucun secret dans le repo.
- Aucun WAN.
- Aucun bridge.
- Aucun admin-trading.
- Aucun closeout DB_LAYER rouvert.
- Aucun index global modifie sans instruction explicite.

## 16_TODO

1. Rechercher documentation locale et externe sur `sandbox.mode`.
2. Identifier les valeurs supportees.
3. Identifier les regles `allow` / `deny` supportees.
4. Determiner si SSH/network peut etre autorise sans desactiver le sandbox.
5. Produire une matrice de decision.
6. Revenir ensuite au runtime uniquement si une option sure est prouvee.

## RISKS

- À qualifier.
