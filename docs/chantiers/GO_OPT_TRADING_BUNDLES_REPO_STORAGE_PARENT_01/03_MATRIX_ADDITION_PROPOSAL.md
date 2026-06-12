---
doc_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_MATRIX_ADDITION_PROPOSAL
doc_type: matrix_addition_proposal
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
status: draft
lifecycle_stage: governance_proposal
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - opt-trading
  - bundles
  - matrix
  - governance
  - github
  - retrieval
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/03_MATRIX_ADDITION_PROPOSAL.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/01_BUNDLE_STORAGE_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/02_BUNDLE_RETRIEVAL_METHOD.md
---

# 03_MATRIX_ADDITION_PROPOSAL — ajout matrice bundles

## 1_MASTER_TARGET

Proposer un ajout à la matrice documentaire pour encadrer l'enregistrement et la récupération des bundles IDE via GitHub.

Ce document est une proposition. Il ne modifie pas directement `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.

## 3_INITIAL_NEED

Besoin utilisateur : prévoir dans la matrice une méthode pour enregistrer et récupérer les bundles sur GitHub.

## 4_MASTER_PROJECT_PLAN

Ajouter à la matrice une règle de placement et de récupération pour les bundles :

- surface canonique : `bundles/<GO_ID>/` ;
- forme principale : dossier décompressé ;
- forme secondaire : ZIP de transport ;
- indexation minimale : lien depuis chantier ou entrée d'index ;
- récupération : Git direct, sparse checkout ou miroir `/shared`.

## 7_CANONICAL_STATE

La matrice actuelle définit déjà les surfaces : governance, architecture, index, chantiers, registry, journal, racine.

Les bundles ne sont pas encore explicitement couverts comme surface durable.

## 11_KEY_DECISIONS_PROPOSED

- Ajouter `bundles/` comme surface de support IDE durable.
- Garder `docs/chantiers/` comme source du cadrage et du closeout.
- Garder `bundles/<GO_ID>/` comme support d'exécution/reprise IDE.
- Ne pas laisser un bundle uniquement en ZIP de session.
- Ne pas mettre les bundles dans `docs/chantiers/` sauf s'il s'agit de documentation de bundle, pas de support exécutable.

## 12_INVARIANTS_PROPOSED

- GitHub versionne les bundles durables.
- ZIP = transport secondaire.
- `/shared` = miroir machine optionnel.
- Google Drive = lecture humaine optionnelle.
- Aucun secret dans les bundles.
- Manifest obligatoire.
- README obligatoire.
- Les bundles ne remplacent pas les chantiers.
- Les chantiers ne remplacent pas les bundles IDE.

## 20_PROPOSED_MATRIX_SECTION

Section proposée à ajouter à la matrice :

```markdown
### Bundles IDE / supports d'exécution

Les bundles IDE durables sont stockés dans le repo sous forme décompressée :

`bundles/<GO_ID>/`

Rôle :
- fournir un support d'exécution ou de reprise IDE ;
- conserver prompts, checklists, scripts et manifest ;
- permettre la récupération par Git sans dépendre d'un artefact de session.

Règles :
- `README_BUNDLE.md` obligatoire ;
- `bundle_meta/manifest.json` obligatoire ;
- prompts dans `prompts/` ;
- checklists dans `checklists/` ;
- scripts dans `scripts/` ;
- aucun secret ;
- aucun gros binaire sans justification ;
- ZIP seulement comme transport secondaire ;
- `/shared` seulement comme miroir machine ;
- Google Drive seulement comme lecture humaine si nécessaire.

Relation aux chantiers :
- le chantier documente le pourquoi, le statut, le closeout ;
- le bundle fournit les artefacts opérables ;
- un bundle doit pointer vers son GO ;
- un GO doit pointer vers son bundle si le bundle est canonique.
```

## 21_PROPOSED_PLACEMENT_TABLE_ROW

Ligne proposée pour la table de placement :

| Objet | Surface canonique | Indexation minimale | Ce que l'objet ne doit pas devenir |
|---|---|---|---|
| bundle IDE durable | `bundles/<GO_ID>/` | lien depuis `docs/chantiers/<GO_ID>/`, `docs/index/*` si actif | un remplacement du dossier chantier ou du closeout |

## 22_PROPOSED_RETRIEVAL_RULE

Règle proposée :

```text
La récupération durable d'un bundle se fait par Git : repo complet, checkout de branche ou sparse checkout sur bundles/<GO_ID>/. Les ZIP de session ne sont jamais la source canonique.
```

## 23_PROPOSED_BRANCH_RULE

Si un bundle est créé sur branche dédiée :

```text
Créer immédiatement une entrée d'indexation ou déclarer GAP_INDEXATION.
Tracer la branche dans BRANCH_STATE.md si la branche reste ouverte.
```

## 24_PROPOSED_ACCEPTANCE

Un bundle GitHub est accepté si :

```text
README_BUNDLE=present
MANIFEST=present
GO_ID=clear
NO_SECRETS=pass
STRUCTURE=pass
RETRIEVAL_METHOD=defined
INDEX_LINK=present_or_gap_declared
```

## 25_MATRIX_PATCH_SCOPE

Ce document ne patch pas directement la matrice. Le patch matrice doit être un sous-GO ou une passe de gouvernance séparée si l'utilisateur valide l'ajout.

GO possible :

```text
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_CHILD_MATRIX_PATCH_01
```

## 17_RESUME_POINT

```text
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

Fichier:
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/03_MATRIX_ADDITION_PROPOSAL.md

État:
proposition d'ajout à la matrice créée, non appliquée.

Prochaine action:
créer 90_PARENT_CHECKPOINT.md
```

## RISKS

- À qualifier.
