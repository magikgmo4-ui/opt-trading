---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01_CONSOLIDATION_MAP
doc_type: chantier_consolidation_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: opening
topic_keys:
  - why_lint
  - consolidation
  - governance
  - runtime_security
  - why_runtime_graph
  - openclaw_central
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_VIEW_REAL_01/00_INITIAL_PROJECT_DOC.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 00_CONSOLIDATION_MAP_01

## Objet

Cette carte de consolidation fixe les frontieres logiques entre les 4 axes structurants + l'orchestrateur central, en lecture documentaire, sans autorisation runtime.

## Axes et definitions

### Axe 1 — Gouvernance

- **Perimetre** : regles stables, permissions, gates de revue, traces, evals, deny-by-default, frontmatter, nommage, indexation, branches, continuite produit.
- **Source souveraine** : `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- **Role** : fixer le cadre stable que tout autre axe doit respecter.
- **Ne remplace pas** : runtime security, WHY graph, WHY lint, cible produit.

### Axe 2 — Runtime Security

- **Perimetre** : garde-fous d'execution pour skills, workers, agents, surfaces runtime, permissions operationnelles, anti prompt-injection, anti auto-fix destructif.
- **Source souveraine** : `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01`
- **Role** : rendre chaque action IA explicable, tracable, bornee et non destructive par defaut.
- **Ne remplace pas** : la gouvernance generale, le WHY graph, le WHY lint, la cible produit.

### Axe 3 — WHY / WHY-runtime graph

- **Perimetre** : representation explicable du systeme, overlays, snapshots, review outputs, visualisation statique des dependances et de la coherence.
- **Source souveraine** : `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_VIEW_REAL_01`
- **Role** : rendre lisible la logique de construction du systeme sans execution live.
- **Ne remplace pas** : la gouvernance, la securite runtime, le WHY lint, la cible produit.

### Axe 4 — WHY lint

- **Perimetre** : couche warning-only de detection de contradictions entre les axes.
- **Source souveraine** : le present chantier `GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`
- **Role** : detecter et signaler les gaps de coherence. N'autorise aucune action. Ne bloque pas la CI. N'applique aucun correctif automatique.
- **Ne remplace pas** : la gouvernance, la securite runtime, le WHY graph, la cible produit.
- **Invariant fondamental** : WHY lint ne cree pas une 5e verite. WHY lint detecte et signale seulement.

### Axe 5 — OpenClaw orchestrateur central (cible produit)

- **Perimetre** : cible operationnelle Telegram/Gateway/Supervisor/Workers/Memory/Machines.
- **Role** : cible produit a stabiliser, sans autorisation runtime tant que les garde-fous ne sont pas prouves.
- **Ne remplace pas** : les axes documentaires de controle (gouvernance, runtime security, WHY, WHY lint).
- **Depend de** : tous les axes de controle pour etre operationnel en securite.

## Regles de non-concurrence

1. Aucun axe ne remplace un autre.
2. WHY lint ne cree pas une 5e verite.
3. WHY lint detecte et signale seulement.
4. La gouvernance reste souveraine pour les regles stables.
5. La securite runtime reste souveraine pour les garde-fous d'execution.
6. Le WHY graph reste souverain pour la representation explicable.
7. OpenClaw central reste la cible produit, pas une couche de controle.
8. Toute contradiction detectee par WHY lint doit etre resolue par l'axe source, pas par WHY lint lui-meme.

## Mode de consolidation

- Ce chantier parent consolide les 4 axes documentaires de controle + la cible produit.
- Il ne reecrit aucun axe existant.
- Il n'autorise aucune action runtime.
- Il ne modifie aucun index global.
- Il pose les frontieres pour eviter les doublons, contradictions et autorisations implicites.

## RISKS

- À qualifier.
