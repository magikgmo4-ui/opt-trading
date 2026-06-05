---
doc_id: GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01_RESULTS
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
  - results
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/NAMING_CANON_POLICY_01.md
point_de_reprise: "Section Resultats"
updated_at: 2026-04-29
links:
  - modules/naming_normalizer/output/naming_audit_report.md
  - modules/naming_normalizer/output/naming_audit_report.json
  - docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/03_classification_matrix.md
---

# 02_inventory_results

## Resultats
- inventaire repo-first produit : `oui`
- findings module : `31`
- findings scripts racine / `scripts/` hors module : `0`
- items canoniques sans ecart retenu : `940`

## Nombre par classe
- `CANON` : `940`
- `LEGACY_TOLERE` : `5`
- `A_CORRIGER_PLUS_TARD` : `1`
- `REVIEW_REQUIRED` : `2`
- `REFERENCE_ONLY` : `23`

## Lecture surface par surface
- `docs/governance/` : aucun ecart remonte
- scripts racine et `scripts/` : aucun ecart remonte
- `docs/chantiers/` : ecarts concentres sur trois dossiers historiques et onze artefacts de preuve / support
- `modules/` : un seul script direct non conforme remonte
- branches locales : seize ecarts de forme, majoritairement branches de reference locale ou cas a revue

## Portee des propositions
- toutes les propositions restent indicatives
- aucun renommage reel n'est applique
- les cas ambigus ou a forte dependance de contexte restent en `REVIEW_REQUIRED`

## RISKS

- À qualifier.
