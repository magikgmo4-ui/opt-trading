---
doc_id: OPT_TRADING_NEXT_GO_CANDIDATES
doc_type: next_candidate
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: next
topic_keys:
  - opt-trading
  - next
  - continuity
search_tags:
  - surface:chantier
  - doc_role:index
  - flow:next_surface
  - closeout:reference
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Matrice - parent actif -> next GO primaire"
updated_at: 2026-05-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# NEXT_GO_CANDIDATES — opt-trading

## Règle canonique

- 1 parent produit → 1 target ou 1 next GO primaire
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` gouverne la lecture produit/parent/GO/Git
- `docs/index/GO_INDEX.md` reste la vérité de liste

## Matrice — parent actif → target / next GO

| parent produit | produit | statut | next target / next GO | condition | refs |
|---|---|---|---|---|---|
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | doctrine multi-agents | OPEN | surveiller prochains INDEX_PATCH | aucun runtime | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md` |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | parent machine admin-trading | OPEN | ouvrir child si besoin produit | besoin produit prouvé | `docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md` |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | parent machine db-layer | OPEN | ouvrir child si besoin produit | besoin produit prouvé | `docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md` |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | classification lignées runtime | ACTIVE | aucun nouveau GO | consolider en gap-only | `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md` |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | canonique modules/reseau_ssh | OPEN | aucun nouveau GO | réduire compat dans ce GO | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | cadrage tmux-ide | ACTIVE | `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` | machine cible vérifiée | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` |
| `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | intégration UI producer-consumer | OPEN | `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01` | reprise recommandée | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | architecture équipe d'agents | OPEN | aucun nouveau GO | base pour GO enfant d'audit | `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md` |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | runtime tmux/opencode/openclaw | ACTIVE | ouvrir suite si besoin produit | besoin produit prouvé | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
