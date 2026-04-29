---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_MATRIX_CONSOLIDATION_CLOSEOUT_01_CONSOLIDATION_PLAN
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_MATRIX_CONSOLIDATION_CLOSEOUT_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - governance
  - consolidation
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_MATRIX_CONSOLIDATION_CLOSEOUT_01/02_validation_matrix.md
point_de_reprise: "Section Blocs consolides"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/architecture/REPO_SURFACES_MAP.md
---

# 03_consolidation_plan

## Blocs consolides

### Matrice Doc Ops

- garder `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` ouvert
- ne pas faire de closeout par inertie
- traiter la matrice maitre comme socle de lecture, pas comme flux actif de patch

### Metadata derivation

- considerer `GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01` comme clos
- propager sa sortie des surfaces actives
- garder la doctrine comme annexe stable et reouvrable sous condition

### Root policy / reclass

- garder `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01` actif
- considerer `GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01` comme clos fonctionnellement
- garder le parent `ROOT_POLICY_AND_RECLASS` actif sans refermer artificiellement le parent par son sous-lot

### Registry scope

- considerer `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01` comme clos fonctionnellement
- sortir le GO des surfaces actives
- garder `registry/README.md` comme source canonique unique

### Canon structure / continuity index / obsolete audit

- garder ces trois parents actifs
- limiter ce lot a la correction d index prouvee
- ne pas transformer ce closeout en chantier transverse supplementaire

### Naming canon

- garder `GO_OPT_TRADING_PARENT_NAMING_CANON_01` et ses deux enfants ouverts
- ne pas close tant que l inventaire et le normalizer ne sont pas reellement termines

### Parent thread map

- garder `GO_PARENT_THREAD_MAP.md` comme vue derivee
- corriger seulement les statuts faux
- ne pas en faire une nouvelle verite de liste

### Multi agents

- lecture obligatoire seulement
- aucune absorption ni fermeture dans ce lot
