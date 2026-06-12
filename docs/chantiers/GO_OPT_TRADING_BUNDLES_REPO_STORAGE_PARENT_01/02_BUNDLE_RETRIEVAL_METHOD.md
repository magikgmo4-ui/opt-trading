---
doc_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_RETRIEVAL_METHOD
doc_type: bundle_retrieval_method
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
  - retrieval
  - ide
  - sparse-checkout
  - shared
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/02_BUNDLE_RETRIEVAL_METHOD.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/00_PARENT_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/01_BUNDLE_STORAGE_METHOD.md
---

# 02_BUNDLE_RETRIEVAL_METHOD — méthode de récupération bundles GitHub

## 1_MASTER_TARGET

Définir comment récupérer et utiliser un bundle IDE stocké dans GitHub sans dépendre d'un téléchargement depuis une session ChatGPT.

## 3_INITIAL_NEED

Les bundles doivent être accessibles :

- depuis un IDE ;
- depuis une machine Linux ;
- depuis Windows ;
- depuis `/shared` si nécessaire ;
- sans artefact ChatGPT temporaire ;
- avec traçabilité Git.

## 4_MASTER_PROJECT_PLAN

Modes de récupération :

1. repo complet déjà cloné ;
2. checkout de branche ;
3. sparse checkout du dossier `bundles/<GO_ID>/` ;
4. copie vers `/srv/sftp/shared_files/shared/bundles/<GO_ID>/` ;
5. lecture directe depuis GitHub web ;
6. ZIP recréé localement seulement si transport nécessaire.

## 7_CANONICAL_STATE

Ce document définit la méthode. Il ne récupère aucun bundle réel.

## 10_SELECTED_SETUP

Structure cible :

```text
bundles/<GO_ID>/
```

Miroir machine optionnel :

```text
/srv/sftp/shared_files/shared/bundles/<GO_ID>/
```

## 11_KEY_DECISIONS

- La récupération privilégiée est Git.
- L'IDE doit lire le dossier décompressé.
- Le ZIP est recréé localement si besoin, pas traité comme source principale.
- `/shared` sert de miroir de transport, pas de vérité canonique.
- Google Drive reste optionnel pour lecture humaine.

## 12_INVARIANTS

- Ne pas télécharger depuis ChatGPT comme source durable.
- Ne pas modifier le bundle récupéré sans commit ou copie de travail explicite.
- Ne pas exécuter scripts sans lecture préalable.
- Ne pas copier secrets dans `/shared`.
- Ne pas confondre branche de bundle et branche runtime.

## 13_METHOD_A — repo déjà cloné

### Linux / Bash

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

cd /opt/trading
git fetch origin
git checkout go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
git pull --rebase
ls -la bundles/<GO_ID>/
```

### Windows PowerShell

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

Set-Location C:\Users\ghost\opt-trading
git fetch origin
git checkout go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
git pull --rebase
Get-ChildItem bundles\<GO_ID>
```

## 14_METHOD_B — sparse checkout bundle seul

Utile si la machine n'a pas besoin de tout le repo.

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

mkdir -p ~/bundle-work
cd ~/bundle-work
git clone --filter=blob:none --no-checkout https://github.com/magikgmo4-ui/opt-trading.git opt-trading-bundle
cd opt-trading-bundle
git sparse-checkout init --cone
git sparse-checkout set bundles/<GO_ID>
git checkout go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
find bundles/<GO_ID> -maxdepth 3 -type f -print
```

## 15_METHOD_C — miroir vers /shared

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

SRC="/opt/trading/bundles/<GO_ID>"
DST="/srv/sftp/shared_files/shared/bundles/<GO_ID>"

mkdir -p "$DST"
rsync -a --delete "$SRC/" "$DST/"
find "$DST" -maxdepth 3 -type f -print
```

Rôle : rendre le bundle accessible aux autres machines via le partage.

## 16_METHOD_D — recréer un ZIP localement

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

cd /opt/trading
zip -r "/srv/sftp/shared_files/shared/bundles/<GO_ID>.zip" "bundles/<GO_ID>"
```

Le ZIP reste un artefact secondaire.

## 17_METHOD_E — usage IDE

Dans l'IDE :

1. ouvrir le repo `opt-trading` ;
2. basculer sur la branche contenant le bundle ;
3. ouvrir `bundles/<GO_ID>/README_BUNDLE.md` ;
4. exécuter les prompts dans l'ordre ;
5. journaliser les résultats dans le chantier correspondant ;
6. ne pas modifier le runtime sans GO dédié.

## 18_ACCEPTANCE_CHECK

Un bundle récupéré est valide si :

```text
README_BUNDLE.md présent
bundle_meta/manifest.json présent
prompts/ lisible si applicable
checklists/ lisible si applicable
scripts/ lisible si applicable
aucun secret détecté
branche Git identifiée
GO_ID clair
```

## 19_FAILURE_MODES

| Problème | Correctif |
|---|---|
| branche absente | `git fetch origin` puis vérifier nom |
| dossier bundle absent | vérifier `bundles/<GO_ID>/` |
| sparse checkout vide | vérifier branche avant `sparse-checkout set` |
| scripts non exécutables | `chmod +x scripts/*.sh` après lecture |
| `/shared` absent | créer miroir plus tard ou utiliser Git direct |
| bundle trop gros | déplacer binaire hors Git ou utiliser release/artifact |

## 20_RETRIEVAL_PRIORITY

Priorité :

1. Git direct dans repo complet ;
2. sparse checkout ;
3. miroir `/shared` ;
4. ZIP local recréé ;
5. Google Drive lecture humaine.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

Fichier:
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/02_BUNDLE_RETRIEVAL_METHOD.md

État:
méthode de récupération GitHub définie.

Prochaine action:
créer 03_MATRIX_ADDITION_PROPOSAL.md
```

## RISKS

- À qualifier.
