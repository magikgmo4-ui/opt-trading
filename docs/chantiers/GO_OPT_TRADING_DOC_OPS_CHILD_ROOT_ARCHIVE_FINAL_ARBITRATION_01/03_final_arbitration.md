---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01_FINAL
doc_type: chantier_arbitration
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01
status: open
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - governance
  - arbitration
  - root
  - archive
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/REPO_ROOT_POLICY.md
point_de_reprise: "Section Arbitrages"
updated_at: 2026-04-29
links:
  - bitget_bridge.py
  - modules/simex_bitget_bridge/README.md
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md
---

# 03_final_arbitration

## Arbitrages

### A1 — `bitget_bridge.py`

Décision :
- le fichier ne reste plus en `arbitrage ouvert`
- il est qualifie comme shim legacy de compatibilite explicite en racine

Justification :
- son contenu est un simple relais vers le module canonique `modules/simex_bitget_bridge`
- aucun caller repo direct n'est prouve
- la documentation du module conserve explicitement le shim comme support historique disponible
- aucun move n'est necessaire pour stabiliser la politique racine

### A2 — Bundles locaux ignores a la racine

Décision :
- ils sont classes local-only et non canoniques

Justification :
- ils sont ignores par Git
- ils ne sont ni sources de verite ni prerequis de lecture canonique
- ils ne reouvrent pas le GO racine

### A3 — Parent obsolete/archive

Décision :
- la matrice d'audit est jugee suffisante pour closeout

Justification :
- les lots deja executes sont documentes
- les reliquats ont une qualification ou un report explicite
- aucune nouvelle action physique n'est requise dans ce lot d'arbitrage final
