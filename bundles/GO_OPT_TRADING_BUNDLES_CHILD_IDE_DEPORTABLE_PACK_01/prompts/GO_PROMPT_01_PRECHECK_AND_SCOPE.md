# GO_PROMPT_01_PRECHECK_AND_SCOPE

## ROLE

Tu es ChatGPT IDE opérant dans le repo `opt-trading`.

## OBJECTIF

Préparer ou reprendre la branche `GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01` sans modifier le repo hors scope.

## RÈGLE PATCH

Les patchs téléchargés depuis la session peuvent être placés temporairement à la racine du repo.

Ils doivent ensuite être déplacés vers :

```text
bundles/<GO_ID>/patches/
```

Ne jamais committer un patch depuis la racine.

## COMMANDES BASH

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

git status --short --branch
git fetch --prune origin
git switch sot/mainline
git pull --ff-only origin sot/mainline
git switch -c go/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 || git switch go/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
git status --short --branch
```

## COMMANDES POWERSHELL

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

git status --short --branch
if ($LASTEXITCODE -ne 0) { throw "git status failed" }

git fetch --prune origin
if ($LASTEXITCODE -ne 0) { throw "git fetch failed" }

git switch sot/mainline
if ($LASTEXITCODE -ne 0) { throw "git switch sot/mainline failed" }

git pull --ff-only origin sot/mainline
if ($LASTEXITCODE -ne 0) { throw "git pull failed" }

git switch -c go/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
if ($LASTEXITCODE -ne 0) {
  git switch go/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
  if ($LASTEXITCODE -ne 0) { throw "git switch/create GO branch failed" }
}

git status --short --branch
if ($LASTEXITCODE -ne 0) { throw "git status final failed" }
```

## SCOPE AUTORISÉ

```text
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md
docs/index/inbox/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md
bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/
```

## HORS SCOPE

```text
docs/index/GO_INDEX.md
docs/index/ACTIVE_STREAMS.md
docs/index/NEXT_GO_CANDIDATES.md
docs/index/REPRISE.md
docs/index/BRANCH_STATE.md
modules/
registry/
runtime
.env
secrets
```

## STOP_IF

- branche divergente non comprise ;
- fichiers hors scope déjà modifiés ;
- conflits Git ;
- index global touché ;
- runtime touché ;
- patch racine sur le point d'être committé.
