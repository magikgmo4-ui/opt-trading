---
doc_id: GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01
status: open
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
---

# GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 — INITIAL PROJECT DOC

## 1_MASTER_TARGET

Mettre en place ClickUp comme couche de pilotage opérationnel pour `opt-trading`, alignée avec GO_XXXX, GitHub, docs canonisées, branches, machines et modules.

ClickUp ne remplace pas le canon repo. Le repo, les commits, les PR et `docs/` restent la preuve.

## 3_INITIAL_NEED

Comparer ClickUp au workflow trading / multi-machines / modules, définir le setup optimal pour `opt-trading`, mapper ClickUp vers GO_XXXX et ouvrir un chantier parent avec branche dédiée.

## 4_MASTER_PROJECT_PLAN

1. Fixer ClickUp comme cockpit de pilotage.
2. Mapper GO, parent, sous-GO, branche, doc, commit, PR, machine et module.
3. Produire un bundle IDE autonome pour l'implémentation.
4. Préparer l'import initial contrôlé depuis les index repo.
5. Définir les règles de synchronisation et de non-dérive.

## 6_FINAL_TARGET

Chaque GO actif doit être visible dans ClickUp avec GO_ID, statut, module, machine, branche, doc path, PR/commit, validation, NEXT_GO et RESUME_POINT.

## 7_CANONICAL_STATE

- Repo : `magikgmo4-ui/opt-trading`
- Base : `sot/mainline`
- Branche dédiée : `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01`
- Gouvernance : `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- Type actuel : doc/architecture, aucun runtime modifié.

## 11_KEY_DECISIONS

- ClickUp = pilotage uniquement.
- Repo = vérité.
- Docs = mémoire canonique.
- Tâche ClickUp sans preuve repo = intention non validée.

## 12_INVARIANTS

- Ne pas remplacer `GO_INDEX.md`, `REPRISE.md`, `BRANCH_STATE.md`.
- Ne pas inventer de GO depuis ClickUp.
- Ne pas marquer PASS sans preuve repo.
- Ne pas créer de doctrine `1 GO = 1 branche`.

## 16_TODO

1. Créer le bundle IDE d'implémentation.
2. Préparer le schéma ClickUp.
3. Préparer l'import initial.
4. Préparer le runbook d'exécution.
5. Valider la cohérence avec la matrice.

## 17_RESUME_POINT

Reprendre depuis la branche `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01`, dossier `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/`, puis exécuter le bundle IDE.

## RISKS

- À qualifier.
