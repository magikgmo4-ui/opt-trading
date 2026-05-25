---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_OPERATIONAL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_github_actions
go_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_OPERATIONAL_01
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
status: open
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_GITHUB_ACTIONS_OPENCLAW
MASTER_PROJECT_PLAN_ID: MPP_GITHUB_ACTIONS_OPENCLAW
PARENT_GO_ID: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
1_MASTER_TARGET: github_actions_openclaw
NEXT_GO: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_ROUTING_01
topic_keys:
  - opt-trading
  - github_actions
  - openclaw
  - orchestration
  - operational
links:
  - modules/openclaw_github_actions_bridge/app/bridge.py
  - scripts/openclaw_gh_actions_orchestrate.py
---

# GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_OPERATIONAL_01

## Objet

Passer de l'orchestration dry-run à une orchestration OpenClaw opérationnelle contrôlée.

## Définition opérationnelle

OpenClaw doit pouvoir :
1. Lire `docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml`
2. Lister les jobs `orchestrable_by_openclaw=true`
3. Déclencher `workflow_dispatch` sur un job autorisé
4. Poller le run GitHub Actions
5. Récupérer status / conclusion / URL / logs disponibles
6. Produire un rapport d'orchestration
7. Classifier : PASS / FAIL / BLOCKED / NEEDS_HUMAN_REVIEW
8. Proposer l'action suivante sans l'exécuter automatiquement

## Contraintes fortes

- Pas d'auto-merge
- Pas d'apply patch automatique
- Pas de push automatique vers `sot/mainline`
- Pas de self-hosted runner
- Ne pas toucher admin-trading
- Ne pas lancer de trading runtime
- Ne pas modifier secrets
- Ne pas contourner GitHub Actions
- Ne pas contourner les required checks
- OpenClaw orchestre, GitHub Actions gate, humain valide

## Livrables

1. `00_INITIAL_PROJECT_DOC.md` — ce fichier
2. `FILE_SCOPE.txt` — scope
3. `OPERATIONAL_ORCHESTRATION_PLAN.md` — plan opérationnel
4. `RISK_CONTROLS.md` — contrôles de risque
5. `ACCEPTANCE_TESTS.md` — tests d'acceptation
6. `OPERATIONAL_REPORT_01.md` — rapport généré par le run réel
7. Inbox entry
