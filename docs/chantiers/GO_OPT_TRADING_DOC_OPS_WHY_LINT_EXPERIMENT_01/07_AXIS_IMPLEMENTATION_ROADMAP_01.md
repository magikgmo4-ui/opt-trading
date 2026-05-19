---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01_IMPLEMENTATION_ROADMAP
doc_type: chantier_implementation_roadmap
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: opening
topic_keys:
  - why_lint
  - roadmap
  - implementation_order
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/01_IMPLEMENTATION_MASTER_PLAN_4_AXES_01.md
---

# 07_AXIS_IMPLEMENTATION_ROADMAP_01

## Ordre recommande

### Phase 1 — Gouvernance : referencer, ne pas reecrire

- **Action** : utiliser `MATRICE_DOC_OPS_MASTER_MATRIX_01.md` comme source souveraine.
- **Livrable WHY lint** : mapping des regles de gouvernance vers les familles de warnings.
- **Ne pas** : rouvrir la matrice maitre, modifier les regles, creer de nouveaux documents de gouvernance.

### Phase 2 — WHY / WHY-runtime graph : referencer, ne pas reecrire

- **Action** : utiliser `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_VIEW_REAL_01` comme reference.
- **Livrable WHY lint** : mapping des overlays et snapshots WHY vers les familles de warnings.
- **Ne pas** : modifier le scope du WHY graph, ajouter des overlays, lancer le render local.

### Phase 3 — WHY lint : ecrire maintenant comme consolidation warning-only

- **Action** : le present chantier `GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`.
- **Livrables** :
  1. Consolidation map (00)
  2. Master plan (01)
  3. Boundary matrix (02)
  4. Source manifest (03)
  5. Dependency graph (04)
  6. Warning model (05)
  7. Gate binding (06)
  8. Implementation roadmap (07, ce document)
  9. SPEC (SPEC_WHY_LINT_EXPERIMENT_01.md)
  10. Closeout opening (90)
- **Ne pas** : implementer de linter, modifier les index globaux, toucher au runtime.

### Phase 4 — OpenClaw central : stabiliser ensuite comme cible produit

- **Action** : futur chantier dedie.
- **Depend de** : la completion des phases 1-3 pour avoir une base de controle coherente.
- **Ne pas** : autoriser d'execution runtime tant que les garde-fous ne sont pas prouves.

## Futures phases separees (hors scope present chantier)

### Child GO : WHY lint static validator spec

- **GO propose** : `GO_OPT_TRADING_DOC_OPS_CHILD_WHY_LINT_STATIC_VALIDATOR_SPEC_01`
- **Scope** : specification d'un validateur statique de warnings WHY lint.
- **Mode** : DOC_ONLY, pas de code executable.

### Child GO : WHY lint fixture corpus

- **GO propose** : `GO_OPT_TRADING_DOC_OPS_WHY_LINT_CHILD_FIXTURE_CORPUS_01`
- **Scope** : corpus de fixtures pour tester les regles de warnings.
- **Mode** : DOC_ONLY.

### Child GO : WHY lint implementation (eventuel)

- **GO propose** : `GO_OPT_TRADING_DOC_OPS_WHY_LINT_CHILD_IMPLEMENTATION_01`
- **Scope** : implementation d'un linter statique (Python ou Rust).
- **Mode** : DOC_ONLY en spec, CODE en implementation.
- **Contrainte** : can_fail_ci: false, mode WARNING_ONLY perpetuel.

## Etat des lieux a l'ouverture

| Axe | Statut | Action WHY lint |
| --- | --- | --- |
| Gouvernance | MATRICE_MAITRE_CANONICAL | Referencer |
| Runtime Security | PARENT_OUVERT + CHILDS_DRAFT | Referencer |
| WHY graph | LOCAL_VIEW_ACTIVE | Referencer |
| WHY lint | OUVERTURE_PARENT | Ecrire |
| OpenClaw central | NON_SPECIFIE | Reporter a phase 4 |
