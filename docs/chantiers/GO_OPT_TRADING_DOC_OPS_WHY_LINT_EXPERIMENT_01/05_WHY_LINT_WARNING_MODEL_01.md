---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01_WARNING_MODEL
doc_type: chantier_warning_model
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: opening
topic_keys:
  - why_lint
  - warning_model
  - severity
  - gates
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/04_DEPENDENCY_GRAPH_4_AXES_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/06_CROSS_AXIS_GATE_BINDING_01.md
---

# 05_WHY_LINT_WARNING_MODEL_01

## Objet

Definir les familles de warnings du WHY lint, leur severite, leur axe source, leur axe affecte et les exigences de gate/trace/eval associees.

## Severite R0-R5

| Severite | Nom | Description |
| --- | --- | --- |
| R0 | CRITICAL_CONTRADICTION | Contradiction structurelle entre deux axes souverains. Necessite resolution humaine immediate. |
| R1 | STRUCTURAL_GAP | Absence d'un element structurel requis par la gouvernance. |
| R2 | ALIGNMENT_DRIFT | Ecart entre un document et le canon souverain. |
| R3 | COVERAGE_GAP | Manque de couverture documentaire sur un sujet requis. |
| R4 | CONSISTENCY_WARNING | Incoherence mineure entre surfaces non souveraines. |
| R5 | INFORMATIONAL | Note informative, pas un probleme reel. |

## Warning families

| Warning ID | Family | Severity | Source Axis | Affected Axis | Gate Required | Trace Required | Eval Required |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WHY_GAP | Absence de section WHY dans un document canonique | R2 | Gouvernance | WHY | REVIEW_REQUIRED | true | false |
| GOVERNANCE_DRIFT | Ecart entre un document et la matrice maitre | R2 | Gouvernance | Document affecte | GOVERNANCE_ALIGNMENT_REQUIRED | true | false |
| RUNTIME_SECURITY_GAP | Absence de garde-fou pour une action runtime | R1 | Runtime Security | OpenClaw Central | RUNTIME_PROOF_REQUIRED | true | true |
| MACHINE_SCOPE_GAP | Contradiction de routage machine | R3 | Gouvernance | MACHINE_WORK_SPLIT | REVIEW_REQUIRED | true | false |
| WORKER_OWNER_GAP | Worker sans proprietaire documente | R3 | Runtime Security | OpenClaw Central | REVIEW_REQUIRED | true | false |
| MEMORY_SCOPE_GAP | Scope memoire non borne | R2 | Runtime Security | OpenClaw Central | RUNTIME_PROOF_REQUIRED | true | false |
| CONTROL_PLANE_GAP | Surface de controle non documentee | R1 | Gouvernance | OpenClaw Central | MULTI_MACHINE_REVIEW_REQUIRED | true | true |
| SKILL_REGISTRY_GAP | Skill sans entree registry | R3 | Runtime Security | OpenClaw Central | REVIEW_REQUIRED | true | false |
| TRACE_EVAL_GAP | Action sans trace ni eval | R2 | Runtime Security | OpenClaw Central | RUNTIME_PROOF_REQUIRED | true | true |
| OBSERVABILITY_GAP | Signal d'observabilite manquant | R3 | WHY | OpenClaw Central | REVIEW_REQUIRED | false | false |
| BRANCH_CHANTIER_GAP | Branche sans dossier chantier correspondant | R2 | Gouvernance | Branche/Git | REVIEW_REQUIRED | true | false |

## Proprietes communes a tous les warnings

| Propriete | Valeur |
| --- | --- |
| autofix_allowed | false |
| runtime_binding | false |
| can_fail_ci | false |
| mode | WARNING_ONLY |
| action_autorisee | SIGNALER seulement |
| correction | Dans l'axe source, jamais dans WHY lint |

## Regles de declaration de warning

1. Tout warning doit avoir un id unique dans sa famille.
2. Tout warning doit pointer vers la source canonique qui fait autorite.
3. Tout warning doit proposer un chemin de resolution (quel axe, quel document, quel gate).
4. Aucun warning ne doit suggerer une correction automatique.
5. Aucun warning ne doit bloquer la CI.
6. Aucun warning ne doit declencher une action runtime.

## RISKS

- À qualifier.
