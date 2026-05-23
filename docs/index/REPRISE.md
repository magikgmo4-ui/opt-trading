---
doc_id: OPT_TRADING_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - reprise
  - continuity
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Matrice de reprise canonique"
updated_at: 2026-05-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
---

# REPRISE — opt-trading

## Point de reprise global

Base de pilotage active : parents produits actifs dans `GO_INDEX.md` + correction structurante `PRODUCT_FINAL_SURFACE_REGISTRY_01.md`.

Canon décisionnel : état réel du repo `opt-trading`, relu sous la matrice maître et le registre des produits/surfaces finales `PF_*`.

## Correction active

`GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01` ouvre une correction canonique : distinguer produits finaux utilisables, chaînes produit complètes, surfaces opérables, supports critiques et artefacts de transport.

## Parents produits actifs

| PARENT_PRODUCT | STATUT | TARGET | NEXT ACTION |
|---|---|---|---|
| `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01` | OPEN | registre produits/surfaces finales `PF_*` | `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_CLOSE_GATE_AUDIT_01` |
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | OPEN | canoniser méthode multi-agents | surveiller prochains INDEX_PATCH |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | OPEN | parent machine admin-trading | ouvrir child si besoin produit |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | OPEN | parent machine db-layer | ouvrir child si besoin produit |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | ACTIVE | consolider lignées runtime | figer survivant/transition/legacy/archive |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | OPEN | réduire compat réseau/ssh | ouvrir lot réduction compat |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | ACTIVE | implémentation tmux-ide | exécuter GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01 |
| `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | OPEN | intégration UI producer-consumer | reprise sur GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01 |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | OPEN | architecture équipe d'agents | base pour GO enfant d'audit |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | ACTIVE | runtime tmux/opencode/openclaw | maintenir ; ouvrir suite si besoin |

## Prochaine action forte

`GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_CLOSE_GATE_AUDIT_01`

## Reprise opérationnelle

1. Lire `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md`.
2. Lire `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01_PRODUCT_SURFACE_ALIGNMENT_01.md`.
3. Auditer les parents actifs de `GO_INDEX.md` contre les `PF_*`.
4. Corriger les `MASTER_TARGET` abstraits ou trop techniques.
5. Ne fermer aucun parent si son produit final utilisable n'est pas atteint.

## Hors pilotage immédiat

- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` — parent réel, chaîne TMUX close, prochaine passe canonique non prioritaire
- `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` — bundle doc-only mergé, closeout produit, parent non fermé
- `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` — branche-only, continuité canonique basculée sur PR #645/#646
