---
go_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_FAILURE_LOGS_ANALYSIS_FIX_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
1_MASTER_TARGET: github_actions_openclaw
topic_keys:
  - opt-trading
  - github_actions
  - openclaw
  - analysis_fix
links:
  - scripts/openclaw_gh_actions_analyze_failure_logs.py
  - scripts/openclaw_gh_actions_draft_failure_patch.py
---

# GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_FAILURE_LOGS_ANALYSIS_FIX_01

## Objet
Améliorer l'analyse d'échec GitHub Actions : analyse au niveau des steps, extraction de snippet de log, scoring de confiance multi-patrons.

## Définition
- Analyser les steps individuels dans les jobs failed
- Extraire les lignes d'erreur pertinentes des logs
- Score de confiance basé sur le nombre de patrons matchés
- Ajouter des patrons d'échec supplémentaires (edge cases)
- Pipeline amélioré analyse → patch draft

## Améliorations
1. Step-level analysis : `steps` dans la réponse jobs GitHub
2. Log snippet : première ligne d'erreur du step failed
3. Confidence scoring : multi-pattern -> score 0.0-1.0
4. Edge case patterns : ajouter plus de variantes de logs
5. Pipeline test : analyse → patch draft en une commande

## 12_INVARIANTS
- No modification of global indexes.
- No modification of CI workflows.
- No modification of trading/runtime modules.
- No automatic mutations — patches are drafts only.
- `dangerous_action_executed` always false.

## 16_TODO
- [x] Initiation
- [ ] Implementation
- [ ] Validation
- [ ] Close Gate
