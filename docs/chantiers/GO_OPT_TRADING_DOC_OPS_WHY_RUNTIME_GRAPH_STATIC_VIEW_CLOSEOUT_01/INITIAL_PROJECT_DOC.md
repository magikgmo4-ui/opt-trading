---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_STATIC_VIEW_CLOSEOUT_01_INITIAL_PROJECT_DOC
 doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: doc_ops_why_runtime_graph_static_view
go_id: GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_STATIC_VIEW_CLOSEOUT_01
status: reference
lifecycle_stage: closeout
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-14
topic_keys:
  - opt-trading
  - doc_ops
  - why
  - runtime_graph
  - static_view
  - closeout
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_SYSTEM_01/120_RUNTIME_GRAPH_EVOLUTION_ROADMAP.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_SYSTEM_01/140_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_CONVERGENCE_ARCHITECTURE_01/120_CONVERGENCE_FUTURE_RUNTIME_GRAPH_TRAVERSAL.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_GOVERNANCE_DASHBOARD_01/110_CLOSEOUT.md
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_STATIC_VIEW_CLOSEOUT_01/INITIAL_PROJECT_DOC.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_STATIC_VIEW_CLOSEOUT_01/RESUME_POINT.md
---

# INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Fermer la phase documentaire `WHY runtime graph static view` et stabiliser la base canonique permettant d'ouvrir, apres merge, les premiers chantiers runtime reels: render graph local, export JSON, traversal runtime, dashboard prototype, overlays WHY/runtime et observabilite multi-machine.

## 3_INITIAL_NEED

La documentation existante a deja pose:
- le systeme WHY runtime graph;
- la roadmap d'evolution;
- les limites d'autonomie;
- les vues dashboard governance/runtime;
- les traversals candidats;
- les contraintes d'observabilite et de review humaine.

Il manque une fermeture documentaire explicite de la `static view`, c'est-a-dire une couche de synthese qui dit ce qui est stabilise, ce qui reste hors-scope et quels GO sont admissibles ensuite.

## 4_MASTER_PROJECT_PLAN

1. Relire les surfaces canoniques existantes.
2. Produire une synthese architecture static view.
3. Produire un closeout complet et borne.
4. Produire une readiness map vers le runtime reel.
5. Produire un corps de PR doc-only.
6. Ne modifier aucun runtime, script, dashboard executable, export JSON reel ou traversal reel.

## 5_GO_PLAN

GO courant:

`GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_STATIC_VIEW_CLOSEOUT_01`

Role:
- doc-only;
- fermeture static view;
- preparation du futur runtime reel;
- aucun deploiement;
- aucun index global modifie.

## 6_FINAL_TARGET

PR documentaire vers `sot/mainline` contenant:
- `INITIAL_PROJECT_DOC.md`;
- `STATIC_VIEW_ARCHITECTURE_SYNTHESIS_01.md`;
- `STATIC_VIEW_CLOSEOUT_01.md`;
- `STATIC_VIEW_TO_RUNTIME_READINESS_01.md`;
- `PR_BODY_GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_STATIC_VIEW_CLOSEOUT_01.md`;
- `RESUME_POINT.md`;
- entree atomique `docs/index/inbox/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_STATIC_VIEW_CLOSEOUT_01.md`.

## 7_CANONICAL_STATE

| Surface | Etat retenu |
| --- | --- |
| `WHY_RUNTIME_GRAPH_SYSTEM` | PASS, architecture runtime graph documentee |
| `WHY_GOVERNANCE_DASHBOARD` | PASS, cadrage dashboard documente |
| `WHY_CONVERGENCE_ARCHITECTURE` | traversals et risques futurs documentes |
| Static view | presente comme base documentaire, non encore closee explicitement |
| Runtime reel | hors-scope du present GO |
| Export JSON reel | hors-scope du present GO |
| Dashboard executable | hors-scope du present GO |
| Multi-machine live | hors-scope du present GO |

## 8_VALIDATED_PLAN

- Creer uniquement le dossier chantier et son entree inbox.
- Ecrire les documents de fermeture.
- Conserver les index globaux intacts.
- Ouvrir une PR doc-only.
- Apres merge seulement, ouvrir un nouveau GO runtime reel.

## 12_INVARIANTS

- `DOC_ONLY`
- `NO_RUNTIME_CHANGE`
- `NO_EXPORT_JSON_REAL`
- `NO_GRAPH_RENDER_REAL`
- `NO_TRAVERSAL_REAL`
- `NO_DASHBOARD_EXECUTABLE`
- `NO_GLOBAL_INDEX_TOUCH`
- `MERGE_BEFORE_RUNTIME_REAL`
- `HUMAN_REVIEW_GATE_REQUIRED_FOR_CRITICAL_TRAVERSALS`

## 17_RESUME_POINT

Reprendre depuis `RESUME_POINT.md` apres merge de la PR doc-only.