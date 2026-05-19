---
doc_id: GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: structure
go_id: GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - structure
  - surfaces
  - architecture
surface: chantier
source_kind: canonical
updated_at: 2026-04-18
links:
  - docs/INDEX.md
  - docs/ARCHITECTURE.md
  - registry/README.md
  - registry/ui_surfaces_registry.yaml
---

# 00_cadrage — GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01

## Classification
**patch local — doc-only — carte canonique des surfaces**

## Besoin initial
Produire une carte humaine des surfaces réelles du repo sans dupliquer les registres machine-readable.

## Cible finale
- `docs/architecture/REPO_SURFACES_MAP.md` posé comme référence de lecture humaine
- `docs/INDEX.md` et `docs/ARCHITECTURE.md` réalignés avec cette carte

## Contraintes
- ne pas recopier `registry/*`
- pointer vers `registry/*` comme source de vérité machine-readable
- documenter uniquement les changements réels

## REPRISE
Point de reprise local :
- `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/02_journal_technique.md`
