---
doc_id: GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01_SCOPE
doc_type: chantier_note
repo: opt-trading
project: opt-trading
module: naming_normalizer
go_id: GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01
status: open
lifecycle_stage: analyse
topic_keys:
  - opt-trading
  - naming
  - inventory
  - scope
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/NAMING_CANON_POLICY_01.md
point_de_reprise: "Section Surfaces auditees"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/00_cadrage.md
  - modules/naming_normalizer/output/naming_audit_report.md
  - modules/naming_normalizer/output/naming_audit_report.json
---

# 01_inventory_scope

## Surfaces auditees
- `docs/chantiers/`
- `docs/governance/`
- `modules/`
- scripts racine et `scripts/`
- branches locales

## Methode
- lecture canonique du parent naming, de la politique naming et de la matrice maitre
- execution du module `naming_normalizer` en audit-only
- controle complementaire specifique sur scripts racine et `scripts/`, hors perimetre direct du module
- aucune correction appliquee au repo

## Cardinalite auditée
- dossiers directs `docs/chantiers/` : `98`
- fichiers sous `docs/chantiers/<GO_...>/` : `433`
- fichiers `docs/governance/` : `53`
- dossiers directs `modules/` : `84`
- scripts directs des modules (`.sh` / `.py`) : `93`
- scripts racine + `scripts/` (`.sh` / `.py`) : `156`
- branches locales : `54`

## Total items audites
`971`

## Rapports bruts generes
- `modules/naming_normalizer/output/naming_audit_report.md`
- `modules/naming_normalizer/output/naming_audit_report.json`

## RISKS

- À qualifier.
