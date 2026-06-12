---
doc_id: GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: docs_trae
go_id: GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - trae
  - trae_pack_texts
  - docs
  - reclass
  - legacy
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/ot/trae/README.md
  - docs/ot/trae/OT_TRAE_CONTRADICTOIRE_CADRAGE_DECISION_01.md
---

# 00_cadrage — GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01

## Classification
**patch local — doc-only — révision du pack Trae legacy**

## Besoin initial
Sortir `trae_pack_texts/` de la racine, le relocaliser sous `docs/`, puis qualifier proprement ce qu’il reste utile de conserver comme helper Trae/IDE.

## Cible finale
- `docs/ot/trae/trae_pack_texts/` comme emplacement documentaire normalisé
- références documentaires réalignées vers ce nouveau chemin
- statut canonique clarifié : helper legacy, non opposable, non requis pour l’ouverture canonique

## Contraintes
- ne pas re-promouvoir ces packs au-dessus de `workflow_ai/`, du starter pack ou du kanban
- ne pas créer de doctrine parallèle
- documenter uniquement les usages et arbitrages réellement prouvés

## REPRISE
Point de reprise local :
- `docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/02_journal_technique.md`

## RISKS

- À qualifier.
