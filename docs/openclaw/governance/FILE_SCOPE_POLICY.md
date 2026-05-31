---
doc_id: OPENCLAW_FILE_SCOPE_POLICY
doc_type: governance_policy
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_FILESCOPE_COMPLIANCE_01
updated_at: 2026-05-30
---

# FILE_SCOPE_POLICY — Règle obligatoire pour tous les child GOs

## Contexte

La gate `gate/file-scope` du workflow `gated-pr.yml` vérifie que :

1. Le diff PR ne touche qu'un seul répertoire `docs/chantiers/<GO_ID>/`
2. `docs/chantiers/<GO_ID>/FILE_SCOPE.txt` existe au moment du run CI
3. Tous les fichiers modifiés sont couverts par les patterns de `FILE_SCOPE.txt`

Les child GOs #972 (extraction) et #973 (loop_contract) ont été mergés
avec `gate/file-scope = FAIL` car `FILE_SCOPE.txt` était absent dans les deux cas.

## Règle

```
TOUT child GO ouvert dans ce repo doit inclure FILE_SCOPE.txt
dans son répertoire docs/chantiers/<GO_ID>/ DÈS LE PREMIER COMMIT.
```

Un child GO sans `FILE_SCOPE.txt` = gate/file-scope FAIL garanti.

## Template obligatoire

```
# FILE_SCOPE — <GO_ID>
# Only these paths may be modified by this GO.

docs/chantiers/<GO_ID>/**
<tout autre chemin que ce GO modifie>
```

## Syntaxe des patterns

| Pattern | Signification |
| --- | --- |
| `docs/chantiers/<GO_ID>/**` | Tout fichier sous ce répertoire (wildcard récursif) |
| `docs/openclaw/modules/foo.md` | Fichier exact |
| `docs/openclaw/loop_contract/**` | Tout fichier sous ce sous-répertoire |

Le moteur de matching est bash `[[ ]]` — pas de glob POSIX, pas de regex.

## Checklist d'ouverture d'un child GO

```
[ ] Branch créée depuis sot/mainline
[ ] docs/chantiers/<GO_ID>/ créé
[ ] FILE_SCOPE.txt créé et listé dans lui-même (docs/chantiers/<GO_ID>/**)
[ ] 00_INITIAL_PROJECT_DOC.md créé
[ ] FILE_SCOPE.txt liste tous les fichiers que ce GO touchera
[ ] Premier commit inclut FILE_SCOPE.txt avant tout autre fichier hors scope
```

## Retrofix GOs concernés

| GO | PR | Statut retrofix |
| --- | --- | --- |
| `GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01` | #972 | retrofix PR à merger |
| `GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_LOOP_CONTRACT_01` | #973 | retrofix PR à merger |

## Vérification locale avant push

```bash
# Simuler la gate file-scope localement
BASE="sot/mainline"
git fetch origin "$BASE"
git diff --name-only "origin/${BASE}...HEAD" > /tmp/changed.txt

# Vérifier qu'un seul GO est touché
grep -E '^docs/chantiers/GO_' /tmp/changed.txt \
  | sed -E 's#^docs/chantiers/(GO_[A-Z0-9_]+)/.*#\1#' \
  | sort -u

# Vérifier que FILE_SCOPE.txt existe
GO_ID="<GO_ID>"
ls docs/chantiers/${GO_ID}/FILE_SCOPE.txt
```
