---
doc_id: OPT_TRADING_SESSION_PATCH_IDE_APPLICATION_MATRIX_01
doc_type: governance_method
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_SESSION_PATCH_IDE_APPLICATION_MATRIX_01
status: draft
lifecycle_stage: governance_candidate
surface: governance
source_kind: canonical_candidate
updated_at: 2026-05-21
topic_keys:
  - opt-trading
  - session_patch
  - ide_application
  - patch_transport
  - bootstrap
  - pr_review
reference_canonique_principale: docs/governance/SESSION_PATCH_IDE_APPLICATION_MATRIX_01.md
point_de_reprise: "Section 4 - Matrice IDE standard"
links:
  - docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md
  - docs/governance/GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md
  - tools/session_transport/README.md
  - bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/docs/EXEMPLE_MATRICE_APPLICATION_PATCH.md
---

# SESSION_PATCH_IDE_APPLICATION_MATRIX_01

## 1. Objet

Définir l'instruction unique que l'IDE doit lire après production et validation d'un patch GitHub en session conversationnelle.

Nom court attendu dans les prompts :

```text
exemple_matrice_application_patch
```

## 2. But

Réduire le travail IDE à une procédure stable :

```text
bootstrap patch -> apply -> commit -> verify -> push -> PR -> review -> merge si conforme
```

## 3. Emplacement pratique et canonique

### Entrée temporaire IDE

L'utilisateur dépose le patch téléchargé à la racine du repo local :

```text
./<patch>.patch
```

### Emplacement canonique après bootstrap

```text
bundles/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
```

### Règle de commit

```text
Aucun .patch à la racine ne doit être committé.
```

## 4. Matrice IDE standard

| Étape | Objectif | Commande / action | Sortie attendue |
|---|---|---|---|
| 1 | Identifier le job IDE | lire ce document ou `exemple_matrice_application_patch` | GO_ID, branch, patch path |
| 2 | Déposer le patch | placer le `.patch` à la racine repo | `./<patch>.patch` |
| 3 | Bootstrap / nommage | déplacer le patch vers `bundles/<GO_ID>/patches/` | patch canonique créé, root nettoyé |
| 4 | Application locale | `git apply --check` puis `git apply` | diff appliqué |
| 5 | Commit local | `git add` + `git commit` | commit SHA |
| 6 | Vérif avant push | status, diff, root patch check | scope conforme |
| 7 | Push + PR | push branche + créer PR | PR ouverte |
| 8 | Review | demander review ChatGPT/GitHub | verdict |
| 9 | Merge | merge si diff conforme | branche livrée |

## 5. Commandes Bash prêtes

Remplacer les variables seulement.

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

GO_ID="GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01"
BRANCH="go/${GO_ID}"
PATCH_IN="./GO_OPT_TRADING_DOC_OPS_SESSION_PATCH_TRANSPORT_FINAL_COMBINED_01.patch"
PATCH_SLUG="final_combined"

git fetch --prune origin
git switch sot/mainline
git pull --ff-only origin sot/mainline
git switch -c "$BRANCH" || git switch "$BRANCH"

# 1) Bootstrap / nommage canonique du patch téléchargé
tools/session_transport/bootstrap_patch_inbox.sh "$PATCH_IN" "$GO_ID" "$PATCH_SLUG"

PATCH_CANONICAL="$(find "bundles/$GO_ID/patches" -maxdepth 1 -type f -name "*_${GO_ID}_${PATCH_SLUG}.patch" | sort | tail -n 1)"

# 2) Application locale
git apply --check "$PATCH_CANONICAL"
git apply "$PATCH_CANONICAL"

# 3) Vérifications
git diff --check
git status --short --untracked-files=all
find . -maxdepth 1 -type f -name '*.patch' -print
git diff --name-only

# 4) Commit
git add \
  docs/chantiers \
  docs/governance \
  docs/index/inbox \
  bundles \
  tools/session_transport

git diff --cached --check
git commit -m "docs: add session patch transport and IDE deportable bundle"

# 5) Vérification locale avant push
git status --short --branch
git log --oneline -1
git diff --check HEAD~1..HEAD
git show --stat --oneline --name-only HEAD
find . -maxdepth 1 -type f -name '*.patch' -print

# 6) Push
git push -u origin HEAD
```

## 6. Création PR

```bash
gh pr create \
  --base sot/mainline \
  --head "$BRANCH" \
  --title "docs: add session patch transport and IDE deportable bundle" \
  --body-file - <<'EOF'
# docs: add session patch transport and IDE deportable bundle

## Summary

Adds a doc-only method and bundle for transporting ChatGPT session-produced documentation into Git via `.patch` files.

## Scope

- Adds IDE deportable bundle under `bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/`
- Adds canonical patch transport method under `docs/governance/`
- Adds local session transport scripts under `tools/session_transport/`
- Adds inbox entries only
- Does not modify global indexes

## Key rules

- Root repo is temporary patch inbox only
- Canonical patch storage is `bundles/<GO_ID>/patches/`
- `.patch` files are transport artifacts, not final source of truth
- IDE/local workflow is reduced to `bootstrap -> apply -> validate -> commit -> report`
- Global indexes update only when master target / horizon changes

## Validation

- `git diff --check`: PASS
- no runtime files modified
- no trading/live surfaces modified
- no global indexes modified
- no root-level `.patch` committed
EOF
```

## 7. Review demandée à ChatGPT

Après PR :

```text
REVIEW_REQUEST:
Repo: magikgmo4-ui/opt-trading
PR: <number>
Demande:
review diff complet, vérifier doc-only, no global indexes, no runtime, no root patch, cohérence méthode .patch, puis donner verdict merge.
```

## 8. Merge si conforme

```bash
gh pr view --json mergeStateStatus,state,isDraft,headRefName,baseRefName
gh pr checks
gh pr merge --merge
```

Si le repo impose une méthode différente, suivre la politique GitHub réelle.

## 9. Stop conditions

Arrêter si :

- un `.patch` racine est staged;
- un index global est modifié sans demande explicite;
- un fichier runtime est modifié;
- un secret apparaît;
- `git apply --check` échoue;
- `git diff --check` échoue;
- la PR contient des fichiers hors scope.

## 10. Souvenir ChatGPT canonique

```text
Après production et validation d’un patch GitHub en session conversationnelle, l’IDE doit simplement lire `exemple_matrice_application_patch` : déposer le patch à la racine repo, bootstrapper vers `bundles/<GO_ID>/patches/`, appliquer avec `git apply --check` puis `git apply`, valider, commit, vérifier avant push, pousser, ouvrir PR et demander review. Le patch est un artefact de transport, jamais la source canonique finale.
```
