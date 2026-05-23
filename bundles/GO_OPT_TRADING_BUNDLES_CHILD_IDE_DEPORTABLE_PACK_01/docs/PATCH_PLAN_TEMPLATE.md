# PATCH_PLAN_TEMPLATE

## OBJECTIF

<objectif concret>

## PATCH INPUT

```text
<patch root path or bundles/<GO_ID>/patches/path>
```

## PATCH STORAGE

```text
bundles/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
```

## SCOPE AUTORISÉ

```text
<paths>
```

## HORS SCOPE

```text
<paths interdits>
```

## CHANGEMENTS

1. <changement 1>
2. <changement 2>
3. <changement 3>

## RISQUES

| Risque | Mitigation |
|---|---|
| <risque> | <mitigation> |

## VALIDATIONS

```bash
git apply --check <patch>
git apply <patch>
git diff --check
git status --short --untracked-files=all
```

## SORTIE ATTENDUE

```text
FILES_CHANGED:
VALIDATION:
PATCH_STORED:
NEXT_STEP:
```
