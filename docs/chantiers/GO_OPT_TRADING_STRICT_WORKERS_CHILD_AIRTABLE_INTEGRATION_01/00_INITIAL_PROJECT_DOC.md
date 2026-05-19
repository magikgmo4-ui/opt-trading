---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
machine: fantome
status: draft_canonical
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - strict_workers
  - airtable
  - integration
  - worker
  - job_packets
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Definir le worker Airtable integration : job packets, mapping runner, dependance bridge"
updated_at: 2026-05-19
links:
  - modules/airtable_bridge/README.md
  - modules/airtable_bridge/app/client.py
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/20_JOB_PACKETS_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/10_WORKER_POOL_EXTENSION_MATRIX.md
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
---

# GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Definir un worker strict pour l'integration Airtable : job packets pour synchro modeles/matrices, mise a jour de statut GO, et journal de bord operateur — via le module `airtable_bridge` nouvellement cree.

## 2_INITIAL_NEED

Suite a la creation du module `airtable_bridge` et la validation GO_LIMITED d'Airtable comme cockpit data leger, un worker strict est necessaire pour :

1. Synchroniser les modeles VERIFIED/VERIFIED_FREE vers la table Airtable `GO_Status`
2. Reporter les verdicts de GO vers Airtable
3. Proposer un job packet PATCH_DRAFT pour mise a jour des matrices via Airtable
4. S'appuyer sur le bridge pour l'appel API, sans dupliquer la logique

## 3_BORNES_DU_CHILD

Ce child est strictement borne a :

1. **Job packets Airtable** — definir 2-3 job packets (READ_INVENTORY, PATCH_DRAFT, WRITE_GATED) pour Airtable
2. **Mapping runner** — documenter comment le runner strict_workers appelle `airtable_bridge`
3. **Dependance bridge** — le module `airtable_bridge` preexiste ; ce worker n'est qu'un client du bridge
4. **Doc-only** — aucun write Airtable réel, aucun appel API productif

## 4_JOB_PACKETS_PROJETES

### Job Packet 1: READ_INVENTORY — Lire les matrices depuis Airtable

```text
task_type: READ_INVENTORY
surface: airtable
modele: qwen3.5-plus (VERIFIED, A1)
dependance: airtable_bridge
inputs:
  - tableau: GO_Status
  - filtre: champs GO récents
output: reports/ai/workers/airtable_inventory_<ts>.md
denied:
  - ecriture Airtable
  - modification du bridge
required_sections:
  - ETAT_AIRTABLE
  - MODELE_SYNC
  - VERDICT_INVENTORY
```

### Job Packet 2: PATCH_DRAFT — Proposer mise a jour de modele dans les matrices

```text
task_type: PATCH_DRAFT
surface: airtable
modele: glm-5.1 (VERIFIED, A2)
dependance: airtable_bridge
inputs:
  - modele_id
  - nouveau_statut
  - justification
output: reports/ai/workers/airtable_patch_draft_<ts>.md
denied:
  - ecriture directe Airtable
  - modification du registry local
required_sections:
  - MODELE_CIBLE
  - PATCH_PROPOSE
  - DIFF_ATTENDU
  - VALIDATION_EXTERNE
```

### Job Packet 3: WRITE_GATED — Ecrire statut GO dans Airtable (apres approbation)

```text
task_type: WRITE_GATED
surface: airtable
modele: glm-5.1 / qwen3.6-plus (VERIFIED, A4)
dependance: airtable_bridge
approbation: explicite (dry-run puis write reel)
inputs:
  - go_id
  - status
  - next_go
output: reports/ai/workers/airtable_write_<ts>.md
required_sections:
  - APPROBATION_EXPLICITE
  - DRY_RUN
  - WRITE_EFFECTIF
  - VERDICT_WRITE
```

## 5_INVARIANTS

```text
- Aucun secret, token, credentials expose
- Aucune modification du module airtable_bridge (déjà stable)
- Aucune modification de tasks.index.json ou models.registry.json
- Aucun write Airtable réel sans approbation explicite
- Toute sortie = DRAFT_ONLY
- Le bridge est le seul point d'accès API ; pas d'appel direct
```

## 6_CANONICAL_STATE

```text
- Branche: go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01
- Base: sot/mainline
- Machine: fantome
- Perimetre: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01/
- Dépendance bridge: modules/airtable_bridge/ (PASS_AIRTABLE_BRIDGE_MODULE_CREATED)
- Statut initial: cadrage
```

## 7_NEXT_GO

```text
Apres PASS: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01
- Worker ClickUp pour suivi de tâches GO
- Pattern identique : bridge -> job packets -> runner mapping
```

## 8_RESUME_POINT

```text
fantome
→ STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01
→ Branche: go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01
→ Creer les job packets Airtable (3), mapping runner, closeout
→ Dépendance bridge: modules/airtable_bridge/ (ne pas modifier)
→ Doc-only, aucun write réel
```
