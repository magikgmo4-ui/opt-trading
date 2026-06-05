---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01_ASSIGNMENT_RULES
doc_type: regles
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - assignment_rules
  - parent
  - go
  - governance
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Regles"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
---

# 04_assignment_rules — Regles d'affectation

## Regle 1 : unicite du parent canonique

Chaque GO doit avoir exactement 1 parent canonique.

- un GO peut etre cite dans plusieurs surfaces (GO_INDEX, ACTIVE_STREAMS, REPRISE)
- mais un seul parent canonique gouverne son rattachement
- si aucun parent n'est prouve, le GO est lu comme GO simple et `PARENT = CHANTIER`

## Regle 2 : unicite du fil de continuite principal

Chaque GO doit avoir exactement 1 fil de continuite principal.

- le fil principal decrit la sequence logique qui relie le GO a son parent et a ses eventuels enfants
- les rattachements secondaires sont descriptifs seulement et non souverains

## Regle 3 : separation machine / projet / gouvernance

- un GO machine ne doit pas etre deplace vers un parent machine sans preuve
- un parent machine ne doit pas absorber les GO projet ou gouvernance
- les parents machine restent doc-only sauf instruction runtime explicite

## Regle 4 : BRANCH_STATE.md reste surface branche

- `BRANCH_STATE.md` ne gouverne que la surface branches
- il ne determine pas le parent canonique d'un GO
- il ne remplace pas `GO_INDEX.md` pour la structure parent / GO

## Regle 5 : REPRISE.md ne devient pas verite de liste

- `REPRISE.md` est un support de pilotage operatoire
- il ne remplace pas `GO_INDEX.md` comme source de liste canonique
- les rattachements dans REPRISE sont indicatifs

## Regle 6 : preuve de rattachement

Tout rattachement GO -> parent doit etre prouve par au moins une source :
- `GO_INDEX.md` (ligne canonique)
- dossier chantier parent (presence du dossier)
- document d'ouverture parent (reference explicite)
- closeout ou audit (reference dans un closeout)

## Regle 7 : GO simple par defaut

Si aucun parent n'est prouve pour un GO :
- le GO est lu comme GO simple
- `GO_INDEX.md` peut normaliser `PARENT = CHANTIER`
- on ne fabrique pas de parent artificiel

## Regle 8 : sous-GO herite du parent

Un sous-GO :
- herite du fil de continuite du parent par defaut
- sert un objectif local borne
- ne ferme pas implicitement le parent

## Regle 9 : non-deplacement sans preuve

On ne deplace pas un GO d'un parent a un parent machine sans preuve que :
- le GO concerne reellement cette machine
- le rattachement machine est prouve dans le repo
- le deplacement ne casse pas la lecture produit

## Regle 10 : matrice draft avant matrice canonique

La matrice draft reste dans le dossier chantier. On ne cree pas `docs/index/GO_PARENT_THREAD_MAP.md` dans ce lot sauf necessite prouvee et documentee.

## RISKS

- À qualifier.
