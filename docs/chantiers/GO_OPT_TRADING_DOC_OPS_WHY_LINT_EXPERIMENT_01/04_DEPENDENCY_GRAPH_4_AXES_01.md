---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01_DEPENDENCY_GRAPH
doc_type: chantier_dependency_graph
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: opening
topic_keys:
  - why_lint
  - dependency_graph
  - cross_axis
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_CONSOLIDATION_MAP_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md
---

# 04_DEPENDENCY_GRAPH_4_AXES_01

## Graphe logique

```
OpenClaw Central Target (cible produit)
├── requires Runtime Security (garde-fous d'execution)
├── constrained by Governance MCP Policy (regles stables)
├── represented by WHY/runtime Graph (representation explicable)
└── checked by WHY lint (detection de contradictions)
    ├── emits Warnings
    ├── emits Review Gates requirements
    ├── emits Trace requirements
    └── emits Eval requirements
```

## Regle de dependance

Une couche aval ne redefinit pas une couche amont.

### Couche amont → aval

```
Gouvernance (amont)
  → Runtime Security (aval)
    → OpenClaw Central Target (aval)
      → WHY/runtime Graph (representation)
        → WHY lint (verification)
```

### Sens de dependance

1. **Gouvernance** → fixe le cadre pour tous les autres axes.
2. **Runtime Security** → derive de la gouvernance, contraint l'execution.
3. **WHY/runtime Graph** → represente les relations entre gouvernance, securite et cible.
4. **WHY lint** → verifie la coherence entre tous les axes, en dernier.
5. **OpenClaw Central Target** → consomme gouvernance + securite, est represente par WHY graph, est verifie par WHY lint.

## Cycle interdit

- WHY lint ne remonte pas de regle vers la gouvernance.
- WHY lint ne definit pas de permission runtime.
- WHY lint ne redefinit pas la cible produit.
- La gouvernance ne definit pas de regle d'execution runtime (delegue a Runtime Security).
- Runtime Security ne redefinit pas la structure de gouvernance.

## Flux de verification

```
Source canonique (gouvernance, runtime security, WHY graph)
  → WHY lint scan
    → Warning emission (WARNING_ONLY)
      → Review gate recommendation
        → Human decision
          → Correction dans l'axe source (jamais dans WHY lint)
```

## Invariant de graphe

1. WHY lint est toujours le dernier maillon de verification.
2. WHY lint ne produit jamais de verite nouvelle.
3. WHY lint ne corrige jamais un axe source.
4. Toute correction remonte a l'axe source, pas a WHY lint.
5. Le graphe est acyclique dans le sens de l'autorite : gouvernance → runtime security → cible produit → WHY lint.
