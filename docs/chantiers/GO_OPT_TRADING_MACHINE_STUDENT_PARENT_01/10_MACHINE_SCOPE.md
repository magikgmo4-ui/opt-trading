---
doc_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01_MACHINE_SCOPE
doc_type: machine_scope
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01
status: open
lifecycle_stage: machine_scope
topic_keys:
  - opt-trading
  - machine_parent
  - student
  - machine_scope
  - local_ollama
  - openclaw_lab
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/00_START.md
point_de_reprise: "7_CANONICAL_STATE"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/00_START.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/20_EXISTING_BRANCHES_INVENTORY.md
---

# GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01 — 10_MACHINE_SCOPE

## Perimetre machine

```text id="machine_student_scope"
Machine : student
Role : Local Ollama / Student OpenClaw Lab / modeles locaux / experimentation machine
Type : parent machine
Statut : ouvert doc-only
```

## Assignation

```text id="machine_student_assignment"
OLLAMA = student
student = Local Ollama / Student OpenClaw Lab
```

La machine `student` heberge tout ce qui concerne :
- l'execution et la gestion d'Ollama en local ;
- le Student OpenClaw Lab (configuration, tests, experimentation) ;
- les modeles locaux (pull, evaluation, qualification) ;
- l'experimentation machine (isolee du runtime trading).

## Frontiere avec les autres machines

| Machine | Frontiere | Interaction |
|---------|-----------|-------------|
| cursor-ai | Aucun partage direct | Pas de runtime commun |
| fantome | Machine support distincte | Pas de melange |
| admin-trading | Ne pas activer maintenant | Pas de runtime admin-trading ici |
| db-layer | Garder disponible | Pas d'ingestion pour le moment |

## Rattachement aux branches existantes

```text id="machine_student_existing_branches"
Parent famille :
- go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01

Children famille :
- go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_*
```

## Invariants machine

- Ne pas melanger les surfaces Git avec les autres machines.
- Chaque branche modifie son propre dossier `docs/chantiers/<GO_ID>/`.
- Pas de modification des index globaux sauf inbox atomique.
- Pas de runtime trading sur cette machine.
- Pas d'installation Ollama dans ce GO.

## Prochain GO

`GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_PARENT_RECONCILIATION_01`
Objectif : reconcilier les branches Local Ollama existantes avec le parent machine student.
