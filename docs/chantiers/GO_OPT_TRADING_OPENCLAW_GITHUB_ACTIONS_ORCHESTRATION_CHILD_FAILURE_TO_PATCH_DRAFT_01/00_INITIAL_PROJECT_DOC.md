---
go_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_FAILURE_TO_PATCH_DRAFT_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
1_MASTER_TARGET: github_actions_openclaw
NEXT_GO: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_FAILURE_LOGS_ANALYSIS_FIX_01
topic_keys:
  - opt-trading
  - github_actions
  - openclaw
  - patch_draft
links:
  - scripts/openclaw_gh_actions_analyze_failure_logs.py
  - scripts/openclaw_gh_actions_draft_failure_patch.py
---

# GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_FAILURE_TO_PATCH_DRAFT_01

## Objet
À partir d'une analyse d'échec GitHub Actions (classification + logs), produire un draft de patch contrôlé sans application automatique.

## Définition
OpenClaw doit pouvoir charger un rapport d'analyse d'échec, identifier la classification, et pour les types réparables, produire un patch sous forme de diff unifié. Le patch est proposé à l'humain — jamais appliqué automatiquement.

## Classifications patchables
- **TEST_FAILURE** → draft fix de test
- **YAML_WORKFLOW_FAILURE** → draft correction YAML
- **MISSING_FILE** → draft création du fichier manquant
- **FILE_SCOPE_FAILURE** → draft mise à jour FILE_SCOPE.txt
- **NO_LOCK_OVERLAP_FAILURE** → note de résolution de conflit
- **PERMISSION_FAILURE** → pas de patch (info uniquement)
- **TIMEOUT** → draft augmentation timeout
- **NETWORK_OR_API_FAILURE** → pas de patch (info uniquement)
- **UNKNOWN_FAILURE** → pas de patch (review humaine requise)

## Contraintes
- Pas d'auto-merge, apply patch, push vers sot/mainline
- Pas de trading runtime, secrets, contournement GitHub Actions
- Humain dans la boucle — `dangerous_action_executed` toujours false
- `human_review_required` toujours true pour tout patch drafté

## 12_INVARIANTS
- No modification of global indexes.
- No modification of CI workflows.
- No modification of trading/runtime modules.
- No automatic mutations — patches are drafts only.

## 16_TODO
- [x] Initiation
- [ ] Implementation
- [ ] Validation
- [ ] Close Gate
