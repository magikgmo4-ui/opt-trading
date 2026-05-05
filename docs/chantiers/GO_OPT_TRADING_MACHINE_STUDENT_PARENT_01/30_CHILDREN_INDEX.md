---
doc_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01_CHILDREN_INDEX
doc_type: children_index
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01
status: open
lifecycle_stage: children_index
topic_keys:
  - opt-trading
  - machine_parent
  - student
  - children_index
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/00_START.md
point_de_reprise: "Children cadres"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/00_START.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/10_MACHINE_SCOPE.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/20_EXISTING_BRANCHES_INVENTORY.md
---

# GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01 — 30_CHILDREN_INDEX

## GO enfants proposes

### GO_CHILD_01 — Reconciliation Local Ollama (IMMEDIAT)

```yaml
go_id: GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_PARENT_RECONCILIATION_01
statut: a_ouvrir
priorite: P1
branche_proposee: go/GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_PARENT_RECONCILIATION_01
objectif: |
  Reconciller les branches existantes :
  - GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
  - GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_*
  avec le parent machine student.
dependance: aucun (GO courant)
```

### GO_CHILD_02 — Reprise implementation Ollama / OpenClaw Lab

```yaml
go_id: GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_IMPL_REPRISE_01
statut: a_ouvrir_apres_reconciliation
priorite: P2
branche_proposee: go/GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_IMPL_REPRISE_01
objectif: |
  Reprendre l'implementation reelle Ollama/OpenClaw Lab sur student.
  Repartir de l'etat etabli dans le parent Local Ollama et ses children.
dependance: GO_CHILD_01 (reconciliation)
```

### GO_CHILD_03 — Evaluation modeles locaux

```yaml
go_id: GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_MODEL_EVALUATION_02
statut: candidat
priorite: P3
branche_proposee: go/GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_MODEL_EVALUATION_02
objectif: |
  Evaluer les modeles Ollama disponibles localement pour le contexte opt-trading.
  Repartir des evaluations existantes (MODEL_PULL_EVAL_*) et les consolider.
dependance: GO_CHILD_02 (implementation reprise)
```

### GO_CHILD_04 — Experimentation machine

```yaml
go_id: GO_OPT_TRADING_STUDENT_EXPERIMENTATION_MACHINE_01
statut: candidat
priorite: P4
branche_proposee: go/GO_OPT_TRADING_STUDENT_EXPERIMENTATION_MACHINE_01
objectif: |
  Cadrer l'experimentation machine sur student :
  - tests isoles ;
  - benchmarks modeles ;
  - validation de configuration.
dependance: GO_CHILD_02 (implementation reprise)
```

## Ordre recommande

```text id="student_go_order"
1. GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_PARENT_RECONCILIATION_01 (P1, immediat)
2. GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_IMPL_REPRISE_01 (P2, apres reconciliation)
3. GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_MODEL_EVALUATION_02 (P3, candidat)
4. GO_OPT_TRADING_STUDENT_EXPERIMENTATION_MACHINE_01 (P4, candidat)
```

## Verdict

Children cadres. Le GO_CHILD_01 (reconciliation) est le prochain GO immediat.
Aucun child n'est ouvert dans ce parent.
