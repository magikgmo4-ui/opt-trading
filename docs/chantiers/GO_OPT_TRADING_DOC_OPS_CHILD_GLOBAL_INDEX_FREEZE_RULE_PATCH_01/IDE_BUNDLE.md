---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01_IDE_BUNDLE
doc_type: ide_bundle
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01
status: ready_for_ide
lifecycle_stage: execution_bundle
machine: cursor-ai
surface: chantier
source_kind: canonical_draft
updated_at: 2026-05-09
topic_keys:
  - opt-trading
  - doc_ops
  - global_index_freeze
  - ide_bundle
  - cursor-ai
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01/IDE_BUNDLE.md
point_de_reprise: "Appliquer ce bundle depuis cursor-ai IDE sur branche recréée depuis sot/mainline."
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# IDE_BUNDLE — GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01

## 1_MASTER_TARGET

Préparer l'application IDE du patch doc-only qui ajoute à la matrice doc ops une règle explicite de gel des index globaux.

## 6_FINAL_TARGET

Appliquer plus tard depuis `cursor-ai` :

- section `8.5` dans `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` ;
- rattachement du GO au bloc `CURSOR_AI` dans `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` ;
- cadrage chantier ;
- closeout chantier ;
- inbox courte.

## 12_INVARIANTS

Ne pas modifier :

```text
 docs/index/GO_INDEX.md
 docs/index/NEXT_GO_CANDIDATES.md
 docs/index/ACTIVE_STREAMS.md
 docs/index/REPRISE.md
 docs/index/BRANCH_STATE.md
```

Ne pas toucher :

```text
 runtime
 modules applicatifs
 services
 secrets
 Google Drive
```

## 16_TODO — fichiers à créer ou modifier

Autorisé :

```text
 docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
 docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
 docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01/00_CADRAGE.md
 docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01/90_CLOSEOUT.md
 docs/index/inbox/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01.md
```

## GO_PROMPT — à coller dans l'IDE

```text
GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01

Contexte:
Repo opt-trading. Base canonique: sot/mainline. Machine: cursor-ai.

Objectif:
Appliquer un patch doc-only qui ajoute une règle explicite de gel des index globaux dans la matrice doc ops, quand l'utilisateur dit “ne touche pas aux index globaux” ou équivalent.

Branche:
go/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01

Étapes Git obligatoires:
1. git fetch --all --prune
2. git switch sot/mainline
3. git pull --rebase origin sot/mainline
4. supprimer/recréer localement la branche si nécessaire depuis sot/mainline à jour
5. travailler uniquement sur la branche dédiée

Fichiers autorisés:
- docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
- docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
- docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01/00_CADRAGE.md
- docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01/90_CLOSEOUT.md
- docs/index/inbox/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01.md

Fichiers interdits:
- docs/index/GO_INDEX.md
- docs/index/NEXT_GO_CANDIDATES.md
- docs/index/ACTIVE_STREAMS.md
- docs/index/REPRISE.md
- docs/index/BRANCH_STATE.md

Patch matrice:
Dans docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md, ajouter après 8.4:

### 8.5 Règle de gel explicite des index globaux

Quand une consigne opérateur explicite indique “ne touche pas aux index globaux”,
“pas d'index global”, “index globaux bloqués” ou équivalent, les surfaces suivantes
sont gelées pour le lot courant :

- `docs/index/GO_INDEX.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/REPRISE.md`
- `docs/index/BRANCH_STATE.md`

Ce gel bloque toute modification directe ou indirecte de ces surfaces, même si un
parent, une branche dédiée ou un child GO est ouvert.

La continuité doit alors rester limitée à :

- `docs/chantiers/<GO_PARENT>/`
- `docs/index/inbox/<GO_PARENT>.md`

Exception recevable uniquement si :

- l'utilisateur lève explicitement le gel ;
- ou un changement global prouvé impose une propagation immédiate ;
- et cette exception est documentée dans le dossier chantier avant modification.

Effet :

- un parent ne déclenche pas automatiquement une mise à jour des index globaux ;
- une branche dédiée ne déclenche pas automatiquement une mise à jour des index globaux ;
- un child GO ne déclenche pas automatiquement une mise à jour des index globaux ;
- une consigne explicite de gel prime sur la propagation documentaire habituelle.

Patch MACHINE_WORK_SPLIT:
Dans le bloc CURSOR_AI, ajouter après DOC_OPS — BLOCKED:

### DOC_OPS — ACTIVE LOCAL PATCH

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01` | Patch matrice doc-only — règle de gel explicite des index globaux ; machine cursor-ai ; ne pas modifier GO_INDEX/NEXT_GO/ACTIVE_STREAMS/REPRISE/BRANCH_STATE |

Créer 00_CADRAGE.md, 90_CLOSEOUT.md et l'inbox courte avec les invariants ci-dessus.

Validation obligatoire:
- git diff --name-only
- échouer si un des fichiers interdits apparaît dans le diff
- commit message: docs: add explicit global index freeze rule
- push branche
- PR doc-only
```

## COMMANDES_BASH

```bash
set -Eeuo pipefail
trap 'echo "ERR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

git fetch --all --prune
git switch sot/mainline
git pull --rebase origin sot/mainline

git branch -D go/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01 2>/dev/null || true
git switch -c go/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01
```

Validation avant commit :

```bash
set -Eeuo pipefail
trap 'echo "ERR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

git diff --name-only

for f in \
  docs/index/GO_INDEX.md \
  docs/index/NEXT_GO_CANDIDATES.md \
  docs/index/ACTIVE_STREAMS.md \
  docs/index/REPRISE.md \
  docs/index/BRANCH_STATE.md
do
  if git diff --name-only | grep -qx "$f"; then
    echo "FAIL: index global interdit modifié: $f" >&2
    exit 1
  fi
done

git status --short --branch
```

Commit/push :

```bash
git add \
  docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md \
  docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md \
  docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01/00_CADRAGE.md \
  docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01/90_CLOSEOUT.md \
  docs/index/inbox/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01.md

git commit -m "docs: add explicit global index freeze rule"
git push -u origin go/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01
```

## 17_RESUME_POINT

Reprendre depuis ce fichier :

```text
 docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_FREEZE_RULE_PATCH_01/IDE_BUNDLE.md
```

Puis appliquer dans IDE sur `cursor-ai`, après réalignement de la branche sur `sot/mainline`.
