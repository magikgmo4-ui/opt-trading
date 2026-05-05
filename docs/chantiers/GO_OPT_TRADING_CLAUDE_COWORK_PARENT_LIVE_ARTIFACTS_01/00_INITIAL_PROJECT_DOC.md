---
doc_id: OPT_TRADING_CLAUDE_COWORK_LIVE_ARTIFACTS_PARENT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01
status: open
lifecycle_stage: cadrage_parent
topic_keys:
  - opt-trading
  - claude_cowork
  - live_artifacts
  - attention_center
  - openclaw
  - github
  - orchestration
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-04-26
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/BRANCH_STATE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/01_FULL_RESPONSE_CAPTURE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/02_REMAINING_GAP.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/BRANCH_STATE.md
---

# GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01 — Initial Project Doc

## 1_MASTER_TARGET

Documenter et cadrer l'utilisation des Live Artifacts de Claude Cowork comme cockpit dynamique pour le workflow `opt-trading`, sans remplacer le canon repo/docs/Git.

Synthese stable :

```text
Repo / docs / commits / closeouts = verite canonique
Live Artifact Claude = vue dynamique de pilotage
Claude Cowork = operateur / assistant d'execution
OpenClaw = orchestrateur local / agent runtime
GitHub / Drive / fichiers locaux = sources consultees
```

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche de reference initiale du chantier parent.

Il fige :
- la demande initiale ;
- le verdict adapte au workflow ;
- la position canonique du Live Artifact ;
- le plan d'integration ;
- les invariants ;
- les gaps restants ;
- le point de reprise.

Surface canonisee pour le nommage GO :

```text
PRODUCT_OR_SURFACE = CLAUDE_COWORK
```

Rattachement produit/famille :

```text
Famille de soutien principale : openclaw / agents / prompt factory
Couche transverse : methode / transmission / continuite
```

## 3_INITIAL_NEED

Demande utilisateur initiale :

```text
Artefacts en direct
Creez des artefacts dynamiques qui restent a jour grace aux donnees en direct de vos connecteurs.
Creez votre premier artefact.
Ce qui necessite mon attention
c'est quoi ?
```

Precision utilisateur :

```text
dans Claude
```

Demande de suite :

```text
commence par documenter l'integralite de ta reponse dans un chantier parent sur une branche dediee, ensuite remaining gap.
```

## 4_MASTER_PROJECT_PLAN

Plan maitre retenu :

1. Creer un chantier parent dedie.
2. Ouvrir une branche dediee depuis `sot/mainline`.
3. Documenter l'integralite de la reponse de cadrage precedente.
4. Isoler les Remaining Gaps dans un document separe.
5. Ajouter un `BRANCH_STATE.md` local au chantier.
6. Ajouter un checkpoint parent.
7. Ajouter un point de reprise executable.
8. Reporter explicitement le gap d'indexation si `GO_INDEX.md` n'est pas modifie dans ce lot.

## 5_GO_PLAN

GO parent :

```text
GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01
```

Branche dediee :

```text
go/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01
```

Type :

```text
doc-only / cadrage parent / orchestration Claude Cowork
```

## 6_FINAL_TARGET

Cible de phase courante :

- produire un dossier chantier lisible et reprenable ;
- figer le verdict et l'architecture proposes ;
- separer l'usage dynamique des Live Artifacts de la verite canonique Git/docs ;
- preparer le prochain lot : traitement des gaps restants et creation eventuelle d'un prompt Claude Cowork executable.

## 7_CANONICAL_STATE

ETABLI :

- Le repo canonique est `magikgmo4-ui/opt-trading`.
- La branche canonique est `sot/mainline`.
- Le connecteur GitHub est actif avec droits d'ecriture.
- Le document de gouvernance `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` a ete consulte.
- La branche dediee a ete creee depuis `sot/mainline@79b54f6f004ccb9b637a18d3ae02966e1afca07c`.

NEXT_GO :

```text
GO_OPT_TRADING_CLAUDE_COWORK_CHILD_REMAINING_GAP_01
```

## 8_VALIDATED_PLAN

Plan valide pour ce lot :

| Phase | Action | Resultat attendu |
| --- | --- | --- |
| P1 | Creer branche dediee | Isolation Git du parent |
| P2 | Creer dossier chantier | Ancrage documentaire |
| P3 | Capturer la reponse complete | Perte de contexte evitee |
| P4 | Documenter Remaining Gap | Suite operatoire claire |
| P5 | Ajouter BRANCH_STATE local | Trace branche dediee |
| P6 | Ajouter checkpoint parent | Reprise stable |
| P7 | Ajouter GAP_INDEXATION si necessaire | Dette d'indexation explicite |

## 9_SELECTED_SOLUTION

Solution selectionnee :

```text
Live Artifact Claude = cockpit dynamique read-only par defaut.
Repo/docs/Git = verite canonique.
OpenClaw = orchestration runtime future, non remplacee par Claude.
```

Premier Live Artifact cible :

```text
OPT_TRADING_ATTENTION_CENTER_01
```

## 10_SELECTED_SETUP

Setup recommande :

```text
Claude Desktop / Claude Cowork
  -> Live Artifact OPT_TRADING_ATTENTION_CENTER_01
  -> sources lues en mode restreint
  -> refresh manuel/controle

Repo opt-trading
  -> docs/index/*
  -> docs/chantiers/*
  -> docs/governance/*
  -> GitHub PR/branches/issues si connecteur disponible
```

## 11_KEY_DECISIONS

- Un Live Artifact ne remplace pas le repo.
- Un Live Artifact ne remplace pas `GO_INDEX.md`.
- Un Live Artifact ne ferme pas un GO.
- Un Live Artifact ne valide pas une branche sans preuve Git.
- L'ecriture reste interdite sans GO explicite.
- Le premier cas d'usage doit etre `ATTENTION_CENTER`, pas un mega-dashboard global.

## 12_INVARIANTS

- Le repo prouve.
- Git historise.
- Les docs canonisent.
- Les closeouts ferment.
- Les Live Artifacts lisent et visualisent.
- Aucune modification repo/Drive/GitHub sans instruction explicite.
- Les etats machine ne doivent pas etre supposes sans verification reelle.

## 13_ESTABLISHED

- Besoin utilisateur : comprendre et exploiter les Live Artifacts Claude Cowork.
- Cible prioritaire : cockpit dynamique “ce qui necessite mon attention”.
- Mode d'integration : read-only par defaut.
- Role du repo : source canonique.
- Role du Live Artifact : surface dynamique de supervision.

## 14_HYPOTHESIS

A valider dans les prochains lots :

- Claude Cowork peut lire toutes les sources utiles selon les connecteurs disponibles.
- Un workspace local dedie peut limiter l'exposition des fichiers sensibles.
- Un snapshot repo read-only est preferable a l'acces direct au repo actif.
- L'Attention Center pourra etre derive proprement depuis `GO_INDEX`, `REPRISE`, `BRANCH_STATE`, PR GitHub et fichiers chantier.

## 15_REMAINING_GAP

Voir :

```text
docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/02_REMAINING_GAP.md
```

## 16_TODO

- Finaliser le prompt Claude Cowork pour `OPT_TRADING_ATTENTION_CENTER_01`.
- Decider le perimetre exact des sources autorisees.
- Preparer le dossier local `claude-workspace`.
- Valider le mode read-only pour les fichiers repo.
- Decider si GitHub, Drive, Calendar, Asana/ClickUp doivent entrer dans le premier artifact.
- Mettre a jour `GO_INDEX.md` dans un passage local complet ou via connecteur si contenu complet non tronque.

## 17_RESUME_POINT

Reprise minimale :

```text
Branche : go/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01
GO parent : GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01
Dossier : docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/
Prochaine action : traiter 02_REMAINING_GAP.md puis produire le prompt executable Claude Cowork pour OPT_TRADING_ATTENTION_CENTER_01.
```

## 18_TO_DOCUMENT

- `01_FULL_RESPONSE_CAPTURE.md`
- `02_REMAINING_GAP.md`
- `SESSION_REPRISE.txt`
- `GAP_INDEXATION.md`

## 19_TO_REMEMBER

Memory Bricks projet candidates, pas bio memory :

- `LIVE_ARTIFACT_AS_DYNAMIC_COCKPIT_NOT_CANON`
- `CLAUDE_COWORK_READONLY_FIRST`
- `OPT_TRADING_ATTENTION_CENTER_01`
- `REPO_DOCS_GIT_REMAIN_SOURCE_OF_TRUTH`
