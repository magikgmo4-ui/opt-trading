---
doc_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_CHILD_PAPER_STABILITY_WINDOW_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_CHILD_PAPER_STABILITY_WINDOW_01
parent_go: GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_PAPER_STABILITY_FIRST_JOB_PARENT_01
status: open
lifecycle_stage: cadrage
created_at: 2026-05-30
machine_cible: db-layer
machine_operateur: fantome
surface: docs/chantiers
source_kind: canonical
topic_keys:
  - openclaw
  - db-layer
  - orchestrator
  - paper
  - stability_window
---

# 00_INITIAL_PROJECT_DOC — Child : Fenêtre Stabilité PAPER db-layer

## 1_MASTER_TARGET

Documenter et valider la fenêtre de stabilité PAPER de l'orchestrateur sur db-layer :
enregistrer les runs consécutifs (run ID + modules + résultats) sur 7 jours glissants,
confirmer la conformité au seuil du PAPER_PROMOTION_GATE, et produire un rapport
de stabilité servant de pré-requis au premier job boucle (CHILD_FIRST_LOOP_JOB_01).

## 2_PRECONDITIONS

```text
PAPER_PROMOTION_GATE_01 = PASS
Seuil gate : runs >= 4, 11/11 OK, 0 failed, NO_ACTION/PREPARE_LONG/PREPARE_SHORT seulement
Runs précédents enregistrés :
  - desk_run_20260518_094615 (READONLY_WORKFLOW_SMOKE_01)
  - desk_run_20260518_195528 (PAPER_FIRST_REGULAR_OPERATION_01)
SSH fantome → db-layer = validé
```

## 3_SCOPE

- Runs PAPER via `desk_pro_orchestrator` sur db-layer depuis fantome (SSH)
- Collecte : run_id, timestamp, modules, actions, verdict
- Fenêtre : 7 jours glissants à partir du 2026-05-30
- Seuil minimal doc : 4 runs supplémentaires documentés (en plus des 2 existants)
- Aucun runtime modifié — logs et rapport doc only

## 4_COMMANDE_REFERENCE

```bash
# depuis fantome — SSH vers db-layer
ssh db-layer "cd /opt/trading && python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator run \
  --config modules/desk_pro_orchestrator/config/run_config.example.json"
```

## 5_STRUCTURE_RAPPORT

```text
STABILITY_WINDOW_REPORT.md :
  - tableau des runs (run_id | timestamp | modules_ok | actions | verdict)
  - seuil gate : PASS / NO_GO
  - observations comportementales
  - recommandation : prêt pour CHILD_FIRST_LOOP_JOB_01 ou non
```

## 6_CRITERES_PASS

| Critère | Requis |
| --- | --- |
| Runs documentés (nouveaux) | >= 4 |
| modules_ok | 11/11 sur chaque run |
| actions autorisées | NO_ACTION / PREPARE_LONG / PREPARE_SHORT uniquement |
| failed | 0 |
| secrets dans commits | 0 |
| live trading | aucun |
| git status post-run | clean |

## 12_INVARIANTS

```text
- Mode PAPER exclusif — aucun ordre réel
- 0 runtime modifié
- FILE_SCOPE.txt présent dès J1
- Rapport = doc only, run_ids et logs seulement
```

## 17_RESUME_POINT

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_CHILD_PAPER_STABILITY_WINDOW_01/00_INITIAL_PROJECT_DOC.md
Prochain : exécuter les runs PAPER + rédiger STABILITY_WINDOW_REPORT.md + 20_ACCEPTANCE_REPORT.md
```
