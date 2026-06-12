---
doc_id: GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: structure
go_id: GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01
status: active
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - structure
  - surfaces
  - architecture
surface: chantier
source_kind: canonical
updated_at: 2026-04-18
links:
  - docs/architecture/REPO_SURFACES_MAP.md
  - registry/ui_surfaces_registry.yaml
  - registry/meta_index.yaml
---

# 03_decisions — GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01

## D1 — Carte humaine, registre machine
- `docs/architecture/REPO_SURFACES_MAP.md` est la carte humaine de référence
- `registry/*` reste la source de vérité machine-readable

## D2 — Règle anti-duplication
- ne pas copier intégralement les entrées `registry/*` dans la carte humaine
- référencer les registres et expliciter uniquement la lecture utile pour la continuité

## D3 — Périmètre PHASE 2 / LOT 3
- créer `REPO_SURFACES_MAP.md`
- réaligner `docs/INDEX.md`
- réaligner `docs/ARCHITECTURE.md`

## D4 — Parent actif PHASE 2 (justification continuité)
- `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01` est assumé comme parent actif réel (PHASE 2 / LOT 3)
- cela justifie sa présence dans les index de continuité et contribue au passage de 6 à 8 GO non clos

## REPRISE
Point de reprise unique :
- `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/02_journal_technique.md`

## RISKS

- À qualifier.
