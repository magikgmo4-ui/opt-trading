---
doc_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_PARENT_CADRAGE
doc_type: chantier_parent_cadrage
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
status: open
lifecycle_stage: cadrage_parent
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - opt-trading
  - bundles
  - github
  - ide
  - storage
  - retrieval
  - continuity
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/00_PARENT_CADRAGE.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01 — Cadrage parent

## 1_MASTER_TARGET

Créer un chantier parent séparé pour définir une méthode durable d'enregistrement, de versionnement et de récupération des bundles IDE dans GitHub.

Ce chantier est distinct du chantier Ollama. Ollama est mis en pause et repris plus tard sur son propre parent.

## 2_INITIAL_PROJECT_DOC

Ce document est le document transporteur initial du chantier parent bundles.

Il fixe :
- le besoin ;
- la séparation avec Ollama ;
- la cible GitHub ;
- les règles de stockage ;
- les règles de récupération ;
- la propagation minimale d'indexation ;
- les prochaines étapes.

## 3_INITIAL_NEED

Demande utilisateur :

> Ok sépare les 2 ... Nouveau chantier parent + branche dédiée pour les bundles et ollama on revient plus tard.

Contexte : un bundle IDE avait été généré en ZIP dans la session, mais l'utilisateur veut une méthode pour avoir les bundles accessibles sans téléchargement depuis la session.

## 4_MASTER_PROJECT_PLAN

Direction : créer une méthode canonique où les bundles IDE sont stockés dans le repo GitHub en version décompressée, lisible, versionnée et récupérable par IDE ou machine.

Principe :

```text
GitHub = source versionnée des bundles
ZIP = support secondaire de transport
/shared = éventuel miroir machine
Google Drive = lecture humaine éventuelle, non source canonique IDE
```

## 5_GO_PLAN

Phases prévues :

1. définir la structure canonique `bundles/<GO_ID>/` ;
2. définir le manifest minimal ;
3. définir la méthode d'ajout d'un bundle ;
4. définir la méthode de récupération depuis GitHub ;
5. définir la relation avec `/srv/sftp/shared_files/shared/bundles/` ;
6. proposer une mise à jour future de la matrice documentaire ;
7. produire un closeout ou checkpoint.

## 6_FINAL_TARGET

Livrables attendus :

- `00_PARENT_CADRAGE.md` — présent document ;
- `01_BUNDLE_STORAGE_METHOD.md` — méthode de stockage GitHub ;
- `02_BUNDLE_RETRIEVAL_METHOD.md` — méthode de récupération IDE/machine ;
- `03_MATRIX_ADDITION_PROPOSAL.md` — ajout proposé à la matrice ;
- `90_PARENT_CHECKPOINT.md` — checkpoint de pause ou closeout.

## 7_CANONICAL_STATE

État initial :

- Repo : `magikgmo4-ui/opt-trading`.
- Branche source : `sot/mainline`.
- Branche dédiée : `go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01`.
- Nature : doc-only.
- Ollama : hors périmètre actif ; reprise plus tard sur `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`.
- Aucun runtime patch.
- Aucun bundle réel ancré dans ce commit initial.

## 8_VALIDATED_PLAN

Plan validé pour l'ouverture :

1. créer une branche dédiée ;
2. créer le dossier chantier parent ;
3. poser le cadrage parent ;
4. appliquer une trace d'indexation minimale ;
5. ne pas modifier Ollama ;
6. ne pas toucher au runtime.

## 9_SELECTED_SOLUTION

Solution visée : stocker les bundles dans GitHub sous forme décompressée.

Structure cible proposée :

```text
bundles/
└── <GO_ID>/
    ├── README_BUNDLE.md
    ├── prompts/
    ├── checklists/
    ├── scripts/
    └── bundle_meta/
        └── manifest.json
```

## 10_SELECTED_SETUP

Chantier :

```text
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/
```

Branche :

```text
go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
```

## 11_KEY_DECISIONS

- Séparer le chantier bundles du chantier Ollama.
- Créer une branche dédiée propre aux bundles.
- Utiliser GitHub comme source durable de récupération des bundles.
- Garder les ZIP comme artefacts secondaires, non source principale.
- Prévoir un ajout futur à la matrice documentaire.
- Appliquer immédiatement une trace d'indexation minimale.

## 12_INVARIANTS

- Ne pas mélanger ce chantier avec Ollama.
- Ne pas modifier la branche Ollama depuis ce chantier.
- Ne pas toucher au runtime.
- Ne pas traiter Google Drive comme source canonique IDE.
- Ne pas laisser un chantier parent sans trace d'indexation.
- Ne pas stocker de secrets dans un bundle.
- Ne pas versionner d'artefacts lourds sans règle de taille.

## 13_ESTABLISHED

Établi :

- un ZIP de bundle en session est pratique mais non durable ;
- GitHub est mieux adapté pour un bundle IDE lisible et versionné ;
- les bundles doivent être décompressés pour être utiles directement ;
- un manifest est nécessaire pour traçabilité ;
- les prompts/checklists/scripts doivent être séparés.

## 14_HYPOTHESIS

À valider :

- `bundles/<GO_ID>/` peut devenir la surface canonique repo pour bundles IDE ;
- `/srv/sftp/shared_files/shared/bundles/<GO_ID>/` peut devenir miroir machine ;
- Google Drive peut rester surface de lecture humaine, pas d'exécution IDE.

## 15_REMAINING_GAP

Manques :

- méthode finale d'ajout ;
- méthode finale de récupération ;
- taille maximale recommandée ;
- politique ZIP vs décompressé ;
- placement exact dans la matrice ;
- relation avec docs/chantiers.

## 16_TODO

Prochaines actions :

1. créer `01_BUNDLE_STORAGE_METHOD.md` ;
2. créer `02_BUNDLE_RETRIEVAL_METHOD.md` ;
3. créer `03_MATRIX_ADDITION_PROPOSAL.md` ;
4. produire un checkpoint ;
5. décider ensuite si un premier bundle réel est ancré dans `bundles/`.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

Branche:
go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

État:
chantier parent bundles ouvert, séparé d'Ollama.

Prochaine action:
créer 01_BUNDLE_STORAGE_METHOD.md

Invariants:
doc-only, pas Ollama, pas runtime, indexation minimale obligatoire.
```

## 18_TO_DOCUMENT

À documenter :

- méthode de stockage bundles GitHub ;
- méthode de récupération bundles depuis GitHub ;
- proposition d'ajout à la matrice ;
- relation GitHub / ZIP / shared / Drive.

## 19_TO_REMEMBER

Memory candidate éventuelle :

```text
Les bundles IDE durables doivent être ancrés en version décompressée dans GitHub sous `bundles/<GO_ID>/`, avec manifest, prompts, checklists et scripts séparés. Le ZIP reste un artefact de transport secondaire.
```

## RISKS

- À qualifier.
