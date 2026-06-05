---
doc_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01_CADRAGE
doc_type: cadrage_parent
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: closed
lifecycle_stage: closed
updated_at: 2026-05-30
---

# 00_CADRAGE_PARENT — OpenClaw Docs Research Library

## 1_MASTER_TARGET

Construire une cartographie documentaire exhaustive de l ecosysteme OpenClaw dans opt-trading, classifiee par surfaces strictement separees, servant de librairie de recherche pour les futurs GOs OpenClaw.

## 2_GAP_BUNDLE_SANDBOX

Le bundle ZIP `sandbox:/mnt/data/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01_IDE_BUNDLE_V1.zip` est inaccessible depuis l environnement operateur. Ce GO se base exclusivement sur les sources deja presentes dans `sot/mainline`.

## 3_INITIAL_NEED

Cartographier l ensemble des surfaces OpenClaw du repo pour:
- comprendre l etat reel de la documentation
- identifier les gaps et doublons
- servir de base pour les GOs enfants (source cartography, synthesis, bundles)

## 4_SURFACES_SCANNEES

| Surface | Contenu |
| --- | --- |
| `modules/*openclaw*/` | 9 modules runtime |
| `docs/chantiers/GO_*OPENCLAW*/` | 19 chantiers |
| `docs/hermes/*openclaw*/` | 10 docs Hermes bridge |
| `docs/ot/` | Project cards OpenClaw |
| `docs/product_targets/` | Cible canonique OpenClaw |
| Git branches `*openclaw*` | 37 branches |

## 12_INVARIANTS

- Doc-only, 0 runtime modifie
- Repo = source canonique
- Classification stricte, pas de melange surfaces
- Le bundle externe pourra etre reintegre plus tard si accessible

## 17_RESUME_POINT

```
docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/00_CADRAGE_PARENT.md
```

## RISKS

- À qualifier.
