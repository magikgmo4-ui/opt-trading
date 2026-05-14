---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01_CROSS_AXIS_GATE_BINDING
doc_type: chantier_gate_binding
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: opening
topic_keys:
  - why_lint
  - gates
  - cross_axis
  - binding
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/05_WHY_LINT_WARNING_MODEL_01.md
---

# 06_CROSS_AXIS_GATE_BINDING_01

## Objet

Relier chaque famille de warning WHY lint aux gates de revue appropriees.

## Gates definies

| Gate ID | Description | Axe source | Condition de franchissement |
| --- | --- | --- | --- |
| REVIEW_REQUIRED | Revue humaine obligatoire | Gouvernance | Au moins un humain doit valider |
| RUNTIME_PROOF_REQUIRED | Preuve de runtime securise requis | Runtime Security | La matrice de permissions doit couvrir l'action |
| GOVERNANCE_ALIGNMENT_REQUIRED | Alignement gouvernance requis | Gouvernance | Le document doit etre aligne sur la matrice maitre |
| MULTI_MACHINE_REVIEW_REQUIRED | Revue multi-machine requise | Gouvernance | Au moins deux surfaces machine doivent etre verifiees |
| GATE_SECRET | Gate secret | Gouvernance | Aucun secret ne doit etre expose |
| GATE_TRADE | Gate trade | Runtime Security | Aucune action de trading reelle sans confirmation |
| GATE_GIT_PUSH | Gate git push | Gouvernance | Aucun push sans revue documentaire |
| GATE_GLOBAL_INDEX | Gate index global | Gouvernance | Aucune modification d'index global sans batch d'agregation |
| GATE_RUNTIME | Gate runtime | Runtime Security | Aucune execution runtime sans permission L4+ |
| GATE_OLLAMA_INSTALL | Gate installation Ollama | Runtime Security | Aucune installation Ollama sans validation multi-machine |
| GATE_DOC_WRITE | Gate ecriture documentaire | Gouvernance | Aucune ecriture documentaire sans revue de non-duplication |

## Binding Warning → Gate

| Warning Family | Gate(s) requise(s) |
| --- | --- |
| WHY_GAP | REVIEW_REQUIRED |
| GOVERNANCE_DRIFT | GOVERNANCE_ALIGNMENT_REQUIRED + REVIEW_REQUIRED |
| RUNTIME_SECURITY_GAP | RUNTIME_PROOF_REQUIRED + GATE_RUNTIME |
| MACHINE_SCOPE_GAP | REVIEW_REQUIRED |
| WORKER_OWNER_GAP | REVIEW_REQUIRED + RUNTIME_PROOF_REQUIRED |
| MEMORY_SCOPE_GAP | RUNTIME_PROOF_REQUIRED |
| CONTROL_PLANE_GAP | MULTI_MACHINE_REVIEW_REQUIRED |
| SKILL_REGISTRY_GAP | REVIEW_REQUIRED |
| TRACE_EVAL_GAP | RUNTIME_PROOF_REQUIRED |
| OBSERVABILITY_GAP | REVIEW_REQUIRED |
| BRANCH_CHANTIER_GAP | REVIEW_REQUIRED |

## Gates interdites a WHY lint

Les gates suivantes ne sont JAMAIS declenchees par WHY lint :

| Gate | Raison |
| --- | --- |
| GATE_SECRET | WHY lint ne traite pas les secrets |
| GATE_TRADE | WHY lint n'execute pas de trading |
| GATE_GIT_PUSH | WHY lint ne fait pas de push |
| GATE_GLOBAL_INDEX | WHY lint ne modifie pas les index globaux |
| GATE_OLLAMA_INSTALL | WHY lint n'installe rien |
| GATE_DOC_WRITE | WHY lint n'ecrit pas dans les documents source |

## Regle de franchissement

1. Un gate est franchi quand la condition est satisfaite (revue, preuve, alignement).
2. WHY lint ne franchit jamais un gate.
3. WHY lint recommande seulement le franchissement.
4. Le franchissement effectif est toujours humain ou documente par l'axe source.
