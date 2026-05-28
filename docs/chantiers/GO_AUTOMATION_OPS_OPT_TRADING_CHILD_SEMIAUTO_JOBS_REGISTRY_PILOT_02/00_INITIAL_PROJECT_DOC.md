---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: automation_ops
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02
parent_go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01
status: open
lifecycle_stage: in_progress
topic_keys:
  - opt-trading
  - automation_ops
  - semiauto_pilot
  - jobs_registry
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-28
working_branch: go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02
links:
  - docs/registry/JOBS_REGISTRY.md
  - modules/automation_ops/semiauto_pilot/pilot_runner.py
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_REAL_CASE_01/40_GAPS_AND_NEXT_GO.md
---

# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02

## 1_OBJECTIF

Connecter le pilote semi-auto v1 au registre `docs/registry/JOBS_REGISTRY.md`.

Produire un run réel qui lit les job_packets en statut `DRAFT_ONLY` ou `experimental`,
identifie les candidats à promotion, et génère une preuve JSON + Markdown soumise au gate humain.

## 2_CONTEXTE

`MASTER_TARGET_AUTOMATION_OPS_SEMIAUTO_V1` est fermé/prouvé (PR #929, 2026-05-28).
Le pilote `modules/automation_ops/semiauto_pilot/pilot_runner.py` est opérationnel — 17/17 tests PASS.

Le run précédent (`GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_REAL_CASE_01`) a prouvé
le pilote sur un audit doc-only (448 chantiers sans closeout). Ce GO est le **premier run sur
un objet métier structuré** : le `JOBS_REGISTRY.md`.

Gap documenté dans `40_GAPS_AND_NEXT_GO.md` du REAL_CASE_01 :
> `GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02` —
> connecter le pilote au jobs registry.

## 3_CAS_RÉEL

Lecture de `docs/registry/JOBS_REGISTRY.md` :
- Cibler les entrées `status: DRAFT_ONLY` (22 job_packets) et `status: experimental` (4 entries).
- Identifier les candidats à promotion vers `candidate` ou `active`.
- Proposer un `next_action` par entrée selon les critères du registre.

Aucune mutation du registre dans ce GO. Lecture seule. Gate humain obligatoire avant toute action.

## 4_CONTRAINTES

- Mode `dry_run` uniquement — aucune modification de fichier.
- Pas de merge automatique.
- Pas de création de branches sans gate humain.
- `human_gate_required: true` dans le handoff contract.
- `secrets/` non touché.
- Le pilot_runner ne gère pas encore l'exécution d'actions réelles (gap G02 REAL_CASE_01) —
  les `actions_executed` seront le résultat de la lecture seule du registre.

## 5_LIVRABLES

```
docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02/
  00_INITIAL_PROJECT_DOC.md         ← ce fichier
  10_REGISTRY_READ_SCOPE.md         ← périmètre de lecture : sections ciblées, critères
  20_RUN_REPORT.md                  ← rapport de run + verdicts par entrée
  30_PROOF_INDEX.md                 ← index vers artifacts
  40_GAPS_AND_NEXT_GO.md            ← gaps + GO suivant

artifacts/automation_ops/semiauto_pilot/pilot_<run_id>/
  proof.json
  proof_summary.md
```

## 6_CRITÈRES_DE_FERMETURE

```
- run_id généré
- proof.json présente avec verdict PASS_DRY_RUN
- proof_summary.md présente
- JOBS_REGISTRY.md non modifié (diff clean)
- gate humain : décision opérateur documentée dans 20_RUN_REPORT.md
- 17/17 tests PASS (inchangés)
```

## 7_HORS_PÉRIMÈTRE

- Modification des job_packets.
- Promotion automatique d'entrées dans le registre.
- Connexion au CI/CD ou déclenchement de workflows.
- Enrichissement de `pilot_runner.py` (gap G01/G02 — GO futur séparé).
