# GO_PROMPT_02_DOC_ONLY_APPLY

## OBJECTIF

Appliquer un patch doc-only préparé par la session conversationnelle.

## SI PATCH FOURNI À LA RACINE

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

PATCH_FILE="./<patch-file>.patch"

git apply --check "$PATCH_FILE"
git apply "$PATCH_FILE"
git diff --check
git status --short --untracked-files=all
```

## BOOTSTRAP DU PATCH VERS SON EMPLACEMENT CANONIQUE

Après application, si le patch racine doit être conservé :

```bash
tools/session_transport/bootstrap_patch_inbox.sh "$PATCH_FILE" GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 initial_bundle
```

## VALIDATION DU SCOPE

Le diff doit se limiter à :

```text
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md
docs/index/inbox/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md
bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/
tools/session_transport/
docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md
docs/governance/GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md
```

## INTERDITS

- Ne pas corriger au passage un autre fichier.
- Ne pas modifier les index globaux.
- Ne pas modifier runtime.
- Ne pas ajouter de script destructif.
- Ne pas ajouter de secret.
- Ne pas committer un patch depuis la racine.

## SORTIE ATTENDUE

Retourner :

```text
APPLY_STATUS:
DIFF_CHECK:
FILES_CHANGED:
OUT_OF_SCOPE:
PATCH_STORED:
NEXT_STEP:
```
