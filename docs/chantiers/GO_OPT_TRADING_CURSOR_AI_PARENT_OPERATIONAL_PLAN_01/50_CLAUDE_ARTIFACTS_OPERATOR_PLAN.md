---
doc_id: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01_50_CLAUDE_ARTIFACTS_PLAN
doc_type: chantier/claude_artifacts_plan
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 50_CLAUDE_ARTIFACTS_OPERATOR_PLAN

## GO candidat

```text
GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
```

## Objectif

Creer un pack operateur Claude artifacts qui documente :
- les artefacts produits pendant les sessions Claude cowork ;
- les live artifacts generes comme materiel de session ;
- le lien avec l'IDE bundle deja merge (PR #201) ;
- les regles de conservation/reprise des artefacts.

## Contexte

- PR #201 a merge le parent Claude cowork / live artifacts / IDE bundle.
- La matiere Claude artifacts est integree dans le repo.
- Le pack operateur vient structurer cette matiere pour reprise future.

## Fichiers attendus (candidat)

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Demarrage GO |
| `10_CLAUDE_ARTIFACTS_INVENTORY.md` | Inventaire des artefacts existants |
| `20_CLAUDE_ARTIFACTS_OPERATOR_GUIDE.md` | Guide operateur |
| `30_CLAUDE_ARTIFACTS_BUNDLE_MAP.md` | Mapping avec Bundles |
| `40_CLAUDE_ARTIFACTS_REPRISE_RULES.md` | Regles de reprise |
| `90_CLOSEOUT.md` | Closeout |

## Lien avec Bundles

Le pack utilisera Bundles (`GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01`) pour structurer et packager ses livrables documentaires.

## Position dans la sequence

GO recommande en **position 1** de la sequence post-parent (voir `80_NEXT_GO_SEQUENCE.md`).

## Regles

- Doc-only, pas de runtime.
- Pas d'ouverture admin-trading.
- Pas de modification de code.

## RISKS

- À qualifier.
