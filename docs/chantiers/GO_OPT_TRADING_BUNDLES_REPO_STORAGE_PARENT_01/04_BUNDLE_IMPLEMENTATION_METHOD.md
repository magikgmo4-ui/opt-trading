---
doc_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_IMPLEMENTATION_METHOD
doc_type: bundle_implementation_method
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
  - implementation
  - github
  - ide
  - prompts
  - checklist
  - scripts
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04_BUNDLE_IMPLEMENTATION_METHOD.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/00_PARENT_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/01_BUNDLE_STORAGE_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/02_BUNDLE_RETRIEVAL_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/03_MATRIX_ADDITION_PROPOSAL.md
---

# 04_BUNDLE_IMPLEMENTATION_METHOD — méthode d'implémentation des bundles

## 1_MASTER_TARGET

Définir comment implémenter concrètement un bundle IDE dans le repo `opt-trading`, depuis une intention de GO jusqu'à un dossier `bundles/<GO_ID>/` exploitable par IDE, machine ou opérateur.

Ce document complète :

- `01_BUNDLE_STORAGE_METHOD.md` : où stocker le bundle ;
- `02_BUNDLE_RETRIEVAL_METHOD.md` : comment le récupérer ;
- `03_MATRIX_ADDITION_PROPOSAL.md` : comment inscrire la méthode dans la matrice.

## 3_INITIAL_NEED

Besoin utilisateur :

> Méthode d'implémentation des bundles

Le besoin n'est pas seulement de stocker un bundle. Il faut une méthode reproductible pour créer, structurer, valider, versionner et utiliser un bundle.

## 4_MASTER_PROJECT_PLAN

Cycle d'implémentation :

```text
GO / besoin
  -> cadrage bundle
    -> structure dossiers
      -> prompts / checklists / scripts
        -> manifest
          -> validation no-secrets
            -> indexation
              -> commit
                -> récupération IDE / machine
```

## 5_GO_PLAN

Étapes :

1. identifier le GO servi par le bundle ;
2. choisir le type de bundle ;
3. créer la structure `bundles/<GO_ID>/` ;
4. écrire le README ;
5. ajouter les prompts ;
6. ajouter les checklists ;
7. ajouter les scripts si nécessaires ;
8. créer `manifest.json` ;
9. vérifier sécurité et secrets ;
10. vérifier exécution minimale ;
11. lier le bundle au chantier ;
12. indexer ou déclarer explicitement le point d'entrée ;
13. commit et push.

## 6_FINAL_TARGET

Un bundle implémenté doit permettre à un opérateur ou IDE de reprendre sans la conversation ChatGPT :

- quoi faire ;
- dans quel ordre ;
- avec quelles commandes ;
- dans quel périmètre ;
- avec quelles contraintes ;
- où journaliser les résultats ;
- quand s'arrêter.

## 7_CANONICAL_STATE

Surface d'implémentation cible :

```text
bundles/<GO_ID>/
```

Surface de documentation du pourquoi :

```text
docs/chantiers/<GO_ID>/
```

Les deux doivent être liés, mais ne se remplacent pas.

## 8_VALIDATED_PLAN

Règle de base :

```text
Un bundle n'est pas un chantier.
Un chantier n'est pas un bundle.
Le chantier porte le contexte et le verdict.
Le bundle porte les artefacts opérables.
```

## 9_SELECTED_SOLUTION — structure standard

Structure recommandée :

```text
bundles/<GO_ID>/
├── README_BUNDLE.md
├── prompts/
│   ├── GO_PROMPT_01_*.md
│   ├── GO_PROMPT_02_*.md
│   └── GO_PROMPT_03_*.md
├── checklists/
│   └── CHECKLIST_EXECUTION.md
├── scripts/
│   ├── README_SCRIPTS.md
│   ├── *.sh
│   ├── *.ps1
│   └── *.py
├── docs/
│   └── notes_operateur.md
└── bundle_meta/
    ├── manifest.json
    └── validation_report.md
```

Structure minimale si bundle léger :

```text
bundles/<GO_ID>/
├── README_BUNDLE.md
├── prompts/
│   └── GO_PROMPT_01_MAIN.md
└── bundle_meta/
    └── manifest.json
```

## 10_SELECTED_SETUP — types de bundle

| Type | Usage | Contenu typique |
|---|---|---|
| `doc_bundle` | reprise documentaire | prompts + checklist |
| `ide_bundle` | exécution IDE | prompts + scripts + checklist |
| `machine_bundle` | test machine | commandes Bash/PowerShell + validation |
| `migration_bundle` | déplacement/reclassement | plan + rollback + checks |
| `audit_bundle` | audit repo/file/system | prompts d'audit + grilles |
| `transport_bundle` | copie inter-machine | ZIP secondaire + manifest |

## 11_KEY_DECISIONS

- Toujours créer un README.
- Toujours créer un manifest.
- Séparer prompts, checklists et scripts.
- Garder les scripts lisibles et courts.
- Garder les commandes paste-safe.
- Ne pas inclure de secrets.
- Inclure les contraintes dans le README et le manifest.
- Lier le bundle au GO parent/enfant.
- Ne pas exécuter sans validation humaine si le bundle touche au runtime.

## 12_INVARIANTS

- Pas de secrets.
- Pas de `.env` réel.
- Pas de clé API.
- Pas de token GitHub.
- Pas de commande destructive sans garde-fou.
- Pas de script opaque.
- Pas de binaire lourd.
- Pas de runtime patch caché.
- Pas de bundle sans GO_ID.
- Pas de bundle sans point de reprise.

## 13_ESTABLISHED — README obligatoire

`README_BUNDLE.md` doit contenir :

```text
# Bundle <GO_ID>

## Objet
## GO servi
## Branche recommandée
## Sources canoniques
## Contraintes
## Ordre d'exécution
## Entrypoints
## Sortie attendue
## Stop conditions
## Journalisation
## Point de reprise
```

## 14_MANIFEST obligatoire

`bundle_meta/manifest.json` doit contenir :

```json
{
  "bundle_id": "<GO_ID>_bundle",
  "go_id": "<GO_ID>",
  "parent_go": "<PARENT_GO_ID|null>",
  "repo": "opt-trading",
  "branch": "<branch>",
  "bundle_type": "ide_bundle",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "purpose": "...",
  "entrypoints": [
    "README_BUNDLE.md",
    "prompts/GO_PROMPT_01_MAIN.md"
  ],
  "constraints": [
    "doc-only",
    "no secrets",
    "no runtime patch without GO"
  ],
  "files": [
    "..."
  ],
  "validation": {
    "no_secrets": true,
    "readme_present": true,
    "manifest_present": true,
    "scripts_review_required": true
  }
}
```

## 15_PROMPTS_METHOD

Prompts dans `prompts/` :

- un prompt = une action ou une phase ;
- nom préfixé par ordre : `GO_PROMPT_01_*` ;
- inclure objectifs, sources, contraintes, sortie attendue ;
- ne pas inclure de secrets ;
- ne pas donner d'instructions destructives sans garde-fou ;
- inclure `STOP_IF` si risque.

Exemple :

```text
GO_PROMPT_01_AUDIT.md
GO_PROMPT_02_APPLY_DOC_ONLY.md
GO_PROMPT_03_CLOSEOUT.md
```

## 16_CHECKLIST_METHOD

Checklist dans `checklists/` :

```text
CHECKLIST_EXECUTION.md
CHECKLIST_VALIDATION.md
CHECKLIST_ROLLBACK.md si nécessaire
```

Chaque checklist doit contenir :

- prérequis ;
- commandes ou contrôles ;
- critères PASS/FAIL ;
- stop conditions ;
- sortie attendue.

## 17_SCRIPTS_METHOD

Scripts dans `scripts/` seulement si utiles.

Règles :

- scripts lisibles ;
- pas de minification ;
- Bash : `set -Eeuo pipefail` + trap ERR ;
- PowerShell : `$ErrorActionPreference = 'Stop'` ;
- vérifier `$LASTEXITCODE` après commandes critiques ;
- pas de suppression sans confirmation explicite ;
- pas de modification système sans GO ;
- `README_SCRIPTS.md` obligatoire si scripts présents.

## 18_VALIDATION_METHOD

Avant commit :

```text
README_PRESENT=PASS
MANIFEST_PRESENT=PASS
PROMPTS_READABLE=PASS
CHECKLIST_PRESENT=PASS_IF_NEEDED
SCRIPTS_REVIEWED=PASS_IF_PRESENT
NO_SECRETS=PASS
GO_ID_MATCH=PASS
BRANCH_MATCH=PASS
INDEX_LINK=PASS_OR_DECLARED_GAP
```

## 19_NO_SECRET_CHECK

Contrôles recommandés :

```bash
grep -RniE 'token|secret|api_key|apikey|password|passwd|bearer|PRIVATE KEY' bundles/<GO_ID>/ || true
find bundles/<GO_ID> -type f -maxdepth 4 -print
```

Interprétation : toute occurrence doit être examinée. Les mots dans une checklist peuvent être acceptables ; les valeurs réelles sont interdites.

## 20_IMPLEMENTATION_COMMANDS_BASH

Exemple de création d'un bundle :

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

GO_ID="GO_EXAMPLE_01"
BUNDLE_DIR="bundles/$GO_ID"

mkdir -p "$BUNDLE_DIR/prompts" \
         "$BUNDLE_DIR/checklists" \
         "$BUNDLE_DIR/scripts" \
         "$BUNDLE_DIR/docs" \
         "$BUNDLE_DIR/bundle_meta"

touch "$BUNDLE_DIR/README_BUNDLE.md"
touch "$BUNDLE_DIR/bundle_meta/manifest.json"
```

## 21_IMPLEMENTATION_COMMANDS_POWERSHELL

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$GO_ID = 'GO_EXAMPLE_01'
$BundleDir = "bundles/$GO_ID"

New-Item -ItemType Directory -Force "$BundleDir/prompts" | Out-Null
New-Item -ItemType Directory -Force "$BundleDir/checklists" | Out-Null
New-Item -ItemType Directory -Force "$BundleDir/scripts" | Out-Null
New-Item -ItemType Directory -Force "$BundleDir/docs" | Out-Null
New-Item -ItemType Directory -Force "$BundleDir/bundle_meta" | Out-Null

New-Item -ItemType File -Force "$BundleDir/README_BUNDLE.md" | Out-Null
New-Item -ItemType File -Force "$BundleDir/bundle_meta/manifest.json" | Out-Null
```

## 22_INDEXATION_METHOD

Un bundle canonique doit être référencé depuis au moins un des emplacements suivants :

- dossier chantier du GO servi ;
- entrée d'index dédiée ;
- README du bundle avec retour vers chantier ;
- manifest avec `go_id`, `parent_go`, `branch`.

Règle : si le bundle est créé sur branche dédiée, appliquer immédiatement la trace d'indexation ou déclarer `GAP_INDEXATION`.

## 23_COMMIT_METHOD

Commit recommandé :

```bash
git add bundles/<GO_ID>/ docs/chantiers/<GO_ID>/ docs/index/
git commit -m "docs: add <GO_ID> IDE bundle"
git push
```

Si seulement bundle :

```bash
git add bundles/<GO_ID>/
git commit -m "docs: add <GO_ID> IDE bundle"
```

## 24_ACCEPTANCE_CRITERIA

Un bundle est accepté si :

| Critère | Verdict |
|---|---|
| structure standard | PASS |
| README | PASS |
| manifest | PASS |
| prompts séparés | PASS |
| checklists si nécessaires | PASS |
| scripts lisibles si présents | PASS |
| no secrets | PASS |
| récupération Git documentée | PASS |
| lien chantier | PASS |
| indexation ou gap déclaré | PASS |

## 25_FAILURE_MODES

| Problème | Correctif |
|---|---|
| bundle seulement ZIP | décompresser dans `bundles/<GO_ID>/` |
| pas de manifest | créer `bundle_meta/manifest.json` |
| pas de README | créer `README_BUNDLE.md` |
| prompts mélangés | déplacer vers `prompts/` |
| scripts non documentés | créer `scripts/README_SCRIPTS.md` |
| secrets présents | retirer, réécrire historique si nécessaire |
| pas d'indexation | créer entrée index ou déclarer gap |
| bundle trop gros | déplacer binaires hors Git |

## 26_SELECTED_SOLUTION

Méthode retenue :

```text
Implémenter les bundles comme dossiers Git décompressés, structurés, manifestés et reliés au GO servi.
```

## 27_NEXT_STEP

Après ce document :

- créer ou finaliser le checkpoint parent ;
- décider si un premier bundle réel doit être ancré sous `bundles/` dans un sous-GO séparé.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

Fichier:
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04_BUNDLE_IMPLEMENTATION_METHOD.md

État:
méthode d'implémentation concrète des bundles documentée.

Prochaine action:
checkpoint parent ou sous-GO d'ancrage d'un premier bundle réel.
```
