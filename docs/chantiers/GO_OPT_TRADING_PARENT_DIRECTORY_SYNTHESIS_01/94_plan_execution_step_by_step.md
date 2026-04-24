---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_EXECUTION_STEPS
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - execution
  - suivi
  - steps
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/91_arbre_references_dependances.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/92_plan_classement_optimal.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/93_priorisation_reclassements.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/95_step_04_alignement_documentaire.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/96_step_05_audit_exceptions_racine.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/97_step_06_verification_zones_grises.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/98_step_07_arbitrage_enfants.md
---

# Plan d'execution step-by-step

## Regle de suivi
Chaque step doit garder :
- un objectif clair
- un scope borne
- une preuve attendue
- un rollback simple
- un statut explicite

## Step 00 — baseline top-level
- statut : complete
- objectif : figer l'etat reel du top-level avant arbitrage
- scope : repertoires et fichiers racine
- preuve : listing top-level observe au `2026-04-24`
- sortie : base de comparaison pour l'arbre et le classement
- rollback : aucun, lecture seule

## Step 01 — arbre de references/dependances
- statut : complete
- objectif : formaliser les dependances repo-level structurantes
- scope : `docs/`, `registry/`, `workflow_ai/`, `webhook_server.py`, `perf/`, `adapters/`, `deploy_module_multi_machine/`
- preuve : [91_arbre_references_dependances.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/91_arbre_references_dependances.md)
- sortie : lecture upstream/downstream exploitable
- rollback : revert doc-only

## Step 02 — plan de classement optimal
- statut : complete
- objectif : transformer l'arbre en doctrine de placement
- scope : toutes les surfaces top-level actives
- preuve : [92_plan_classement_optimal.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/92_plan_classement_optimal.md)
- sortie : classes cibles et non-moves explicites
- rollback : revert doc-only

## Step 03 — priorisation des reclassements
- statut : complete
- objectif : separer `SAFE`, `VERIFY`, `FREEZE`
- scope : reclassements et arbitrages derives du plan
- preuve : [93_priorisation_reclassements.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/93_priorisation_reclassements.md)
- sortie : ordre de travail actionnable
- rollback : revert doc-only

## Step 04 — alignement documentaire top-level
- statut : complete
- objectif : corriger les ecarts doc/canon les plus simples avant tout move
- scope :
  - `docs/architecture/REPO_SURFACES_MAP.md`
  - `docs/governance/REPO_ROOT_POLICY.md`
- action attendue :
  - retirer ou requalifier les surfaces non presentes au top-level
  - expliciter les exceptions racine legitimes
  - rappeler la regle local-only
- preuve observee :
  - [95_step_04_alignement_documentaire.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/95_step_04_alignement_documentaire.md)
  - top-level doc aligne sur l'etat reel observe au `2026-04-24`
  - plus de divergence grossiere entre carte et top-level
- rollback :
  - revert doc-only sur les deux fichiers

## Step 05 — audit cible des exceptions racine
- statut : complete
- objectif : confirmer si la racine minimale est stabilisee
- scope :
  - `webhook_server.py`
  - `bitget_bridge.py`
  - fichiers racine restants
- action attendue :
  - confirmer les references repo et la legitimite des deux entrypoints
  - verifier qu'aucun nouvel artefact opportuniste n'est revenu a la racine
- preuve observee :
  - [96_step_05_audit_exceptions_racine.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/96_step_05_audit_exceptions_racine.md)
  - references tracees pour `webhook_server.py`
  - absence de caller repo explicite confirme pour `bitget_bridge.py`
  - decision explicite `keep` pour `webhook_server.py` et `hold` conservatoire pour `bitget_bridge.py`
- rollback :
  - aucun si audit seul

## Step 06 — verification des zones grises
- statut : complete
- objectif : traiter les points `VERIFY` sans casser le repo
- scope :
  - `packages/`
  - `tests/`
  - `student/`
  - `data/`
  - `audit/`
- action attendue :
  - qualifier chaque surface
  - detecter si un lot enfant est necessaire
- preuve observee :
  - [97_step_06_verification_zones_grises.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/97_step_06_verification_zones_grises.md)
  - note de decision par surface
  - frontieres clarifiees
  - divergence documentaire detectee sur `audit/` et tracee
- rollback :
  - aucun si analyse seule

## Step 07 — arbitrage enfants eventuels
- statut : complete
- objectif : n'ouvrir un enfant que si une profondeur supplementaire est justifiee
- candidats :
  - enfant `modules/`
  - enfant `scripts/`
  - enfant `student/data/audit`
- preuve observee :
  - [98_step_07_arbitrage_enfants.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/98_step_07_arbitrage_enfants.md)
  - aucun enfant n'est ouvert a ce stade
  - le parent couvre suffisamment la cartographie repo-level
  - le point `audit/` releve d'une hygiene documentaire ciblee, pas d'un enfant de synthese
- rollback :
  - ne pas ouvrir d'enfant si le besoin n'est pas prouve

## Step 08 — closeout parent ou maintien ouvert
- statut : pending
- objectif : decider si le parent devient reference suffisante
- options :
  - closeout parent si steps `04` a `06` suffisent
  - maintien ouvert si un enfant devient necessaire
- preuve attendue :
  - point de reprise clair
  - etat du parent coherent
- rollback :
  - aucun, decision de gouvernance

## Discipline de preuve
Pour chaque step execute ensuite :
- noter les fichiers cibles
- noter les commandes ou verifications utilisees
- noter la preuve observee
- noter la decision prise
- noter le rollback si le step modifie des fichiers

## Point de reprise
Passer a `Step 08`, closeout parent ou maintien ouvert selon traitement de l'hygiene documentaire restante.
