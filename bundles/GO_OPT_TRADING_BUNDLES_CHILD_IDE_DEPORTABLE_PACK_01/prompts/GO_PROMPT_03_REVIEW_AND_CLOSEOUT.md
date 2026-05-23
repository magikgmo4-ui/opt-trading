# GO_PROMPT_03_REVIEW_AND_CLOSEOUT

## OBJECTIF

Reviewer le bundle appliqué, préparer le commit et le closeout minimal.

## COMMANDES

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

git diff --check
git diff --name-only
find bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 -maxdepth 5 -type f | sort

grep -RniE 'token|secret|api_key|apikey|password|passwd|bearer|PRIVATE KEY' \
  bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 \
  docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md \
  docs/index/inbox/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md || true
```

## ROOT PATCH CHECK

```bash
find . -maxdepth 1 -type f -name '*.patch' -print
```

Aucun `.patch` racine ne doit être inclus dans le commit. Les patchs conservés doivent vivre sous `bundles/<GO_ID>/patches/`.

## COMMIT SI VALIDÉ

```bash
git add \
  docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md \
  docs/index/inbox/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md \
  bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 \
  docs/chantiers/GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01 \
  docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md \
  docs/governance/GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md \
  docs/index/inbox/GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01.md \
  tools/session_transport

git diff --cached --check
git commit -m "docs: add session patch transport and IDE deportable bundle"
```

## CLOSEOUT MINIMAL

Retourner :

```text
BRANCH:
COMMIT:
FILES:
VALIDATION:
NO_SECRETS:
ROOT_PATCHES:
OUT_OF_SCOPE:
PR_READY:
RESUME_POINT:
```
