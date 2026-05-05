---
doc_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01_STRICT_WORKERS_LINK
doc_type: link
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01
status: open
lifecycle_stage: link
topic_keys:
  - opt-trading
  - machine_parent
  - fantome
  - strict_workers
  - link
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/00_START.md
point_de_reprise: "Lien etabli"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/00_START.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/20_EXISTING_BRANCHES_INVENTORY.md
---

# GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01 — 50_STRICT_WORKERS_LINK

## Lien vers le parent Strict Workers existant

Le parent `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` existe sur la branche `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`.
Il est rattache a la machine `fantome` via l'arbitrage `AI_TEAM + STRICT_WORKERS = fantome`.

```text id="strict_workers_link"
Machine : fantome
Parent rattache : GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
Branche : go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
Dossier : docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/
Statut : a_auditer (non promu)
Inbox : docs/index/inbox/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01.md
```

## Contenu du parent Strict Workers

Le parent Strict Workers contient les documents suivants (sur sa branche) :

| Fichier | Description |
|---------|-------------|
| `00_INITIAL_PROJECT_DOC.md` | Document initial du projet Strict Workers |
| `01_PROGRESS_MODEL_VALIDATION_AND_SMOKE_PACKET.md` | Validation modele et smoke packet |
| `02_READONLY_SMOKE_EXEC_REPORT.md` | Rapport d'execution smoke read-only |
| `03_READONLY_SMOKE_VALIDATION.md` | Validation smoke read-only |
| `90_CLOSEOUT.md` | Closeout du parent |
| `BRANCH_STATE.md` | Etat de la branche |

Documents connexes (sur la branche STRICT_WORKERS, dans `docs/agents/strict_workers/`) :

| Fichier | Description |
|---------|-------------|
| `MODELS_MATRIX_01.md` | Matrice des modeles |
| `MODEL_ID_VALIDATION_01.md` | Validation des IDs de modeles |
| `OPENCODE_ZEN_MODEL_ID_AUDIT_01.md` | Audit model ID OpenCode Zen |
| `STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` | Autonomie etroite des Strict Workers |

## Instructions

```text id="strict_workers_instructions"
1. NE PAS promouvoir STRICT_WORKERS sans audit prealable.
2. Auditer le contenu existant avant toute promotion.
3. La reconciliation GO_CHILD_01 devra etablir le lien formel et evaluer le contenu.
4. Si l'audit est satisfaisant, STRICT_WORKERS pourra etre promu et integre a la machine fantome.
5. Si l'audit revele des gaps, un GO enfant de correction sera necessaire avant promotion.
```

## Verdict

Lien etabli. Le parent Strict Workers est reference, non modifie, non promu.
L'audit STRICT_WORKERS est requis avant toute promotion (GO_CHILD_02).
