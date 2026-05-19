---
doc_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_STORAGE_METHOD
doc_type: bundle_storage_method
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
status: draft
lifecycle_stage: method_definition
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - opt-trading
  - bundles
  - github
  - storage
  - ide
  - manifest
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/01_BUNDLE_STORAGE_METHOD.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/00_PARENT_CADRAGE.md
  - docs/index/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_INDEX_ENTRY.md
---

# 01_BUNDLE_STORAGE_METHOD — méthode de stockage bundles GitHub

## 1_MASTER_TARGET

Définir la méthode canonique pour enregistrer les bundles IDE dans GitHub afin qu'ils restent accessibles sans dépendre du téléchargement d'une session ChatGPT.

## 3_INITIAL_NEED

Problème : un bundle généré en ZIP dans une session est utile mais fragile.

Limites du ZIP de session :

- dépend de l'artefact ChatGPT ;
- peut être perdu hors session ;
- n'est pas lisible directement par IDE ;
- ne participe pas naturellement à la continuité Git ;
- ne permet pas de diff fichier par fichier.

Objectif : ancrer les bundles dans GitHub sous une forme lisible, versionnée, récupérable et exploitable par IDE.

## 4_MASTER_PROJECT_PLAN

Règle proposée :

```text
GitHub = source durable et versionnée des bundles
bundles/<GO_ID>/ = bundle décompressé canonique
ZIP = artefact secondaire de transport
/shared = miroir machine optionnel
Google Drive = lecture humaine optionnelle, non source canonique IDE
```

## 7_CANONICAL_STATE

Ce chantier est doc-only.

Aucun bundle réel n'est encore ancré dans `bundles/` par ce fichier.

## 9_SELECTED_SOLUTION

Stocker chaque bundle comme dossier décompressé :

```text
bundles/
└── <GO_ID>/
    ├── README_BUNDLE.md
    ├── prompts/
    │   ├── GO_PROMPT_01_*.md
    │   └── GO_PROMPT_02_*.md
    ├── checklists/
    │   └── CHECKLIST_*.md
    ├── scripts/
    │   └── *.sh / *.ps1 / *.py si nécessaire
    ├── docs/
    │   └── notes ou consignes longues si nécessaire
    └── bundle_meta/
        └── manifest.json
```

## 10_SELECTED_SETUP

### Dossier racine

```text
bundles/
```

### Dossier par bundle

```text
bundles/<GO_ID>/
```

### Identifiant de bundle

Le nom de bundle doit reprendre le GO principal qu'il sert :

```text
<GO_ID>_bundle
```

Exemple :

```text
bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/
```

## 11_KEY_DECISIONS

- Un bundle durable doit être lisible sans extraction ZIP.
- Le ZIP devient secondaire.
- Le dossier `bundles/<GO_ID>/` est la forme principale pour GitHub.
- Les prompts doivent être séparés des checklists et scripts.
- Un `manifest.json` est obligatoire.
- Aucun secret ne doit être stocké dans un bundle.
- Les scripts inclus doivent être explicites, paste-safe, et non destructifs par défaut.

## 12_INVARIANTS

- Pas de secrets.
- Pas de tokens.
- Pas de `.env` réel.
- Pas de logs sensibles.
- Pas de gros binaires sans justification.
- Pas de ZIP comme seule source.
- Pas de bundle sans manifest.
- Pas de bundle sans README.
- Pas de script destructif sans garde-fous et avertissement.
- Pas de mélange avec `docs/chantiers/` sauf liens de référence.

## 13_ESTABLISHED — contenu minimal obligatoire

Chaque bundle doit contenir :

```text
README_BUNDLE.md
bundle_meta/manifest.json
```

Recommandé :

```text
prompts/
checklists/
scripts/
docs/
```

## 14_MANIFEST_SCHEMA

Schéma minimal :

```json
{
  "bundle_id": "<GO_ID>_bundle",
  "go_id": "<GO_ID>",
  "parent_go": "<PARENT_GO_ID|null>",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "repo": "opt-trading",
  "branch": "<branch>",
  "purpose": "...",
  "mode": "ide_bundle|execution_bundle|doc_bundle|transfer_bundle",
  "constraints": ["..."],
  "files": ["..."],
  "entrypoints": ["..."],
  "no_secrets": true
}
```

## 15_SIZE_POLICY

Politique de taille proposée :

| Type | Politique |
|---|---|
| Markdown / txt / json | autorisé |
| scripts légers | autorisé |
| images légères | à justifier |
| zip | secondaire, éviter en source principale |
| binaires lourds | éviter ; préférer release/artifact externe |
| données sensibles | interdit |
| logs bruts | interdit sauf filtrage explicite |

## 16_TODO — méthode d'ajout d'un bundle

Procédure recommandée :

1. créer `bundles/<GO_ID>/` ;
2. ajouter `README_BUNDLE.md` ;
3. ajouter `bundle_meta/manifest.json` ;
4. classer les prompts dans `prompts/` ;
5. classer les checklists dans `checklists/` ;
6. classer les scripts dans `scripts/` ;
7. vérifier absence de secrets ;
8. ajouter une entrée dans le chantier ou index concerné ;
9. commit avec message `docs: add <GO_ID> IDE bundle`.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

Fichier:
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/01_BUNDLE_STORAGE_METHOD.md

État:
méthode de stockage GitHub définie.

Prochaine action:
créer 02_BUNDLE_RETRIEVAL_METHOD.md
```
