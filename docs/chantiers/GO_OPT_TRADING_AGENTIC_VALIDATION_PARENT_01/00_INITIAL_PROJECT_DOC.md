---
doc_id: OPT_TRADING_AGENTIC_VALIDATION_INITIAL_PROJECT_DOC_01
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agentic_validation
go_id: GO_OPT_TRADING_AGENTIC_VALIDATION_PARENT_01
status: initial_locked
lifecycle_stage: parent_opening
surface: docs_chantiers
source_kind: canonical
updated_at: 2026-05-09
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_AGENTIC_VALIDATION_PARENT_01/01_PARENT_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_AGENTIC_VALIDATION_PARENT_01/02_SESSION_INTEGRAL_DOC.md
  - docs/index/inbox/GO_OPT_TRADING_AGENTIC_VALIDATION_PARENT_01.md
topic_keys:
  - opt-trading
  - agentic_validation
  - strict_worker
  - self_validation
  - why_aware_validation
  - proof_driven_workflow
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AGENTIC_VALIDATION_PARENT_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
---

# 2_INITIAL_PROJECT_DOC — GO_OPT_TRADING_AGENTIC_VALIDATION_PARENT_01

## 1_MASTER_TARGET

Construire une fondation documentaire canonique pour la validation agentique dans `opt-trading` : génération séparée de la vérification, validation outillée, respect du WHY, protection des invariants, worker strict automatisé et arrêt propre en cas d’ambiguïté.

## 3_INITIAL_NEED

À partir de l’article transmis : `https://towardsdatascience.com/how-to-make-claude-code-validate-its-own-work/`, formaliser pour `opt-trading` une méthode robuste où les agents ne se contentent pas de produire du code ou des documents, mais valident leur propre travail contre des preuves réelles.

Besoin validé :
- intégrer le principe `generate -> verify -> repair -> revalidate` ;
- éviter la validation auto-référentielle ;
- imposer des ancres réelles : tests, diff, logs, schémas, screenshots, compilateurs, artefacts ;
- protéger les invariants, le WHY et la continuité documentaire ;
- définir un strict worker automatisé, borné, non souverain.

## 4_MASTER_PROJECT_PLAN

Direction validée : créer un chantier parent dédié à la validation agentique.

Axes majeurs :
1. `SPEC_AGENTIC_VALIDATION_PIPELINE_01.md` — boucle de validation agentique.
2. `SPEC_WHY_AWARE_VALIDATION_01.md` — validation sensible au WHY et aux invariants.
3. `SPEC_STRICT_WORKER_AUTOMATION_01.md` — worker strict automatisé, borné, fail-closed.
4. Taxonomie FAIL canonique.
5. Règles de preuve PASS/FAIL.
6. Plan opérationnel jusqu’au final target.

## 11_KEY_DECISIONS

- Parent validé par l’utilisateur.
- Branche dédiée validée.
- Documentation indépendante de session validée.
- Initial project doc obligatoire.
- Plan opérationnel jusqu’au final target obligatoire.
- Continuité locale parent prioritaire.
- Pas de modification automatique des index globaux.

## 12_INVARIANTS

- Aucun PASS sans preuve réelle.
- Aucun auto-fix destructif.
- Aucun changement d’architecture par un worker strict.
- Aucun changement de WHY ou d’invariants sans décision explicite.
- Aucun mélange de machines dans une branche.
- Aucun index global modifié sans instruction ou changement global prouvé.
- En cas d’ambiguïté : STOP + rapport FAIL.

## 17_RESUME_POINT

Reprendre depuis `01_PARENT_PLAN.md`, section `16_TODO`, puis ouvrir le premier child GO :

`GO_OPT_TRADING_AGENTIC_VALIDATION_CHILD_STRICT_WORKER_AUTOMATION_01`
