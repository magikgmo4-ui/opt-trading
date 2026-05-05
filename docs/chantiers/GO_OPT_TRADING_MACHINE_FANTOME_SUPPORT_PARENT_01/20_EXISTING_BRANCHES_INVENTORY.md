---
doc_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01_EXISTING_BRANCHES_INVENTORY
doc_type: branch_inventory
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01
status: open
lifecycle_stage: branch_inventory
topic_keys:
  - opt-trading
  - machine_parent
  - fantome
  - branch_inventory
  - ai_team
  - strict_workers
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/00_START.md
point_de_reprise: "Branches inventoriees"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/00_START.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/10_MACHINE_SCOPE.md
---

# GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01 — 20_EXISTING_BRANCHES_INVENTORY

## Parent AI Team Architecture

```yaml
branche: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
type: parent_doc
statut: KEEP_ACTIVE
canonise: oui (docs/chantiers/ present)
contenu_docs:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/02_journal_technique.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/03_decisions.md
remote: oui
note: |
  Parent actif et documente. Cadre l'architecture d'equipe d'agents specialises.
  Ne pas recréer. Assigner comme thread/parent lie a fantome.
```

## Parent Strict Workers

```yaml
branche: go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
type: parent_doc
statut: a_auditer
canonise: partiel (docs/chantiers/ present sur la branche, non sur sot/mainline)
contenu_docs:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/01_PROGRESS_MODEL_VALIDATION_AND_SMOKE_PACKET.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/02_READONLY_SMOKE_EXEC_REPORT.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/03_READONLY_SMOKE_VALIDATION.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/BRANCH_STATE.md
remote: oui
inbox: docs/index/inbox/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01.md
note: |
  Le parent Strict Workers existe et contient des documents.
  Cependant il necessite un audit avant promotion complete.
  L'inbox associee est deja presente sur sot/mainline.
```

## Branche save/fantome

```yaml
branche: save/fantome-YYYY-MM-DD
type: save
statut: backup
remote: oui
note: |
  Branche de sauvegarde historique.
  Contenu non audite dans ce GO.
```

## Branches connexes (contenu agents/strict_workers)

Le dossier `docs/agents/strict_workers/` contient les documents suivants (sur la branche STRICT_WORKERS) :

| Fichier | Description |
|---------|-------------|
| `MODELS_MATRIX_01.md` | Matrice des modeles |
| `MODEL_ID_VALIDATION_01.md` | Validation des IDs de modeles |
| `OPENCODE_ZEN_MODEL_ID_AUDIT_01.md` | Audit model ID OpenCode Zen |
| `STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` | Autonomie etroite des Strict Workers |

## Verdict

Inventaire termine. Les elements existants :
- 1 parent AI Team Architecture (KEEP_ACTIVE, canonise)
- 1 parent Strict Workers (a auditer, partiellement canonise)
- 1 branche save/fantome (backup)
- 4 documents agents/strict_workers sur la branche STRICT_WORKERS

Tous les elements sont a reconcilier avec le parent machine fantome via le GO enfant `GO_OPT_TRADING_FANTOME_AI_TEAM_STRICT_WORKERS_RECONCILIATION_01`.
