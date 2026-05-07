---
doc_id: OPT_TRADING_GUIDE_OPENCLAW_DOCS_LIBRARY
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/00_CADRAGE_PARENT.md
  - docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/01_SOURCE_CARTOGRAPHY.md
  - docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/02_COMPONENTS_UTILITAIRE.md
  - docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/90_CLOSEOUT.md
---

# Guide utilisateur - OpenClaw Docs Library

## Ce que c'est

OpenClaw Docs Library est une cartographie documentaire repo-first des surfaces OpenClaw presentes dans `opt-trading`.

## A quoi ca sert

Elle sert a lire l'ecosysteme OpenClaw, retrouver les sources utiles et preparer les prochains GOs OpenClaw.

## Quand l'utiliser

- pour comprendre quelles surfaces OpenClaw existent ;
- pour retrouver les modules, branches et docs pertinents ;
- pour preparer un deep dive ou une synthese future.

## Quand ne pas l'utiliser

- comme wiki final deja consolide ;
- comme preuve d'un runtime valide ;
- comme guide d'exploitation live.

## Prerequis

- acces au repo ;
- lecture du cadrage parent et de la closeout ;
- comprehension que la surface est `DOC_ONLY_READY`.

## Commandes / acces

- Cartographie source : `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/01_SOURCE_CARTOGRAPHY.md`
- Analyse composants : `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/02_COMPONENTS_UTILITAIRE.md`

## Procedure simple

1. Lire le cadrage parent pour comprendre le perimetre scanne.
2. Lire `01_SOURCE_CARTOGRAPHY.md` pour voir les classes de sources.
3. Lire `02_COMPONENTS_UTILITAIRE.md` pour distinguer modules specifiques et wrappers generiques.
4. Utiliser la closeout pour identifier le prochain GO OpenClaw utile.

## Verification PASS

- la cartographie couvre les surfaces annoncees ;
- le lecteur peut retrouver une source OpenClaw utile ;
- le lecteur sait quel GO enfant ouvre la suite.

## Limites

- ce n'est pas encore une synthese finale unifiee ;
- certaines surfaces bundle externes etaient absentes au moment du parent ;
- aucune conclusion runtime ne doit etre deduite de cette librairie seule.

## Depannage

- Si une surface manque, verifier d'abord si elle existe dans le repo courant.
- Si la lecture reste trop brute, ouvrir la cartographie child avant de produire une synthese.
- Si un besoin runtime apparait, ouvrir un GO runtime dedie ; ne pas forcer ce guide.

## Source canonique

- `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/00_CADRAGE_PARENT.md`
- `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/01_SOURCE_CARTOGRAPHY.md`
- `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/90_CLOSEOUT.md`

## NEXT_GO

`GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01`
