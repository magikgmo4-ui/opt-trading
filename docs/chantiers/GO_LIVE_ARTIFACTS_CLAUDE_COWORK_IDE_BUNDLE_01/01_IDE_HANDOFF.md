# 01_IDE_HANDOFF — Bundle IDE Live Artifacts Claude Cowork

## RÔLE

Ce fichier est le point d’entrée pour Trae, Claude Code, OpenCode ou tout autre IDE opérateur.

## 7_CANONICAL_STATE

Le bundle doit être utilisé comme pack de reprise documentaire. Il ne doit pas modifier le runtime, ne doit pas pousser de branche et ne doit pas merger.

## Worktree recommandé

```text
C:\Users\ghost\opt-trading\.codex_tmp\live_artifacts_parent_doc_01
```

## Branche parent locale annoncée

```text
go/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_PARENT_DOC_01
```

## Branche bundle remote

```text
go/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01
```

## GO_PROMPT — Installer le bundle dans le chantier parent local

```text
GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_INSTALL_01

RÔLE
Tu es opérateur repo sur opt-trading.
Objectif : intégrer le bundle IDE Live Artifacts Claude Cowork dans le chantier parent local déjà ouvert, sans runtime, sans merge, sans push.

WORKTREE OBLIGATOIRE
C:\Users\ghost\opt-trading\.codex_tmp\live_artifacts_parent_doc_01

BRANCHE ATTENDUE
go/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_PARENT_DOC_01

SOURCE BUNDLE
Branche remote : go/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01
Dossier source : docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/

MISSION
Copier ou reprendre le contenu du bundle dans le chantier parent :
docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_PARENT_DOC_01/

Fichiers cibles recommandés :
- 05_ARTIFACTS_MASTER_PLAN.md
- 06_SOURCE_SECURITY_MATRIX.md
- 07_ATTENTION_CENTER_PROMPT.md
- 08_ARTIFACT_ACCEPTANCE_TESTS.md
- 09_IDE_BUNDLE_HANDOFF.md
- 10_WORKSPACE_SNAPSHOT_PLAN.md

CONTRAINTES
- Doc-only strict.
- Ne pas modifier runtime.
- Ne pas modifier services.
- Ne pas modifier scripts applicatifs.
- Ne pas push.
- Ne pas merge.
- Ne pas commit avant rapport final.
- Toute info non vérifiée = HYPOTHESE ou REMAINING_GAP.

ÉTAPE 1 — Vérifier repo

```bash
set -Eeuo pipefail
trap 'echo "[ERR] line=$LINENO cmd=$BASH_COMMAND" >&2' ERR
pwd
git status --short --branch
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git remote -v
git fetch origin --prune
```

STOP si la branche n’est pas `go/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_PARENT_DOC_01`.

ÉTAPE 2 — Lire le bundle remote

```bash
git fetch origin go/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01
mkdir -p /tmp/live_artifacts_bundle
rm -rf /tmp/live_artifacts_bundle/*
git archive origin/go/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01 docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01 | tar -x -C /tmp/live_artifacts_bundle
find /tmp/live_artifacts_bundle -type f | sort
```

ÉTAPE 3 — Copier les contenus utiles

Créer ou mettre à jour les fichiers cibles dans le dossier parent local. Ne pas écraser les fichiers déjà validés sans fusion manuelle.

ÉTAPE 4 — Vérifier diff

```bash
git status --short --branch
git diff --stat
git diff -- docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_PARENT_DOC_01 docs/index
```

ÉTAPE 5 — Rapport final

Produire :
- 13_ESTABLISHED
- 15_REMAINING_GAP
- 16_TODO
- 17_RESUME_POINT

STOP.
NE PAS COMMIT.
NE PAS PUSH.
```

## 16_TODO

- Installer ce bundle dans le chantier parent local.
- Conserver la branche bundle comme source de reprise / transport.
- Committer le parent seulement après validation complète du diff local.

## RISKS

- À qualifier.
