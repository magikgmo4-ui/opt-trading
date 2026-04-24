---
doc_id: GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: naming_normalizer
go_id: GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - naming
  - module
  - audit_only
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Livrables V1"
updated_at: 2026-04-22
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/NAMING_CANON_POLICY_01.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md
---

# 00_cadrage - GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01

## Identite
- GO : `GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01`
- Repo : `opt-trading`
- Module : `naming_normalizer`
- Statut : `open`
- Type : module durable audit-only

## Intention
Creer un module durable capable de :
- detecter les ecarts de nommage
- verifier la structure canonique GO du repo
- proposer un nom canonique seulement quand la source structurelle est suffisante
- generer un rapport markdown + json

## Hors perimetre V1
- renommage automatique
- deplacement automatique
- modification Git
- correction de contenu interne
- canonisation implicite d'un nouveau `<PRODUCT_OR_SURFACE>`

## Livrables V1
- `README.md`
- `cmd.sh`
- `menu.sh`
- `sanity_check.sh`
- moteur Python audit-only
- config declarative
- script `audit_naming.sh`

## PASS / FAIL
- PASS : le module fonctionne en audit-only sur un repo local
- FAIL : le module modifie le repo ou exige un refactor global
