---
doc_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_FILESCOPE_COMPLIANCE_01_INIT
doc_type: initial_project_doc
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_FILESCOPE_COMPLIANCE_01
status: open
created_at: 2026-05-30
---

# 00_INITIAL_PROJECT_DOC — Child File Scope Compliance

## 1_MASTER_TARGET

Adresser GAP 4 : stabiliser la gate/file-scope pour tous les child GOs
du parent research library. Les child #972 (extraction) et #973 (loop_contract)
ont été mergés avec gate/file-scope FAIL — cause : FILE_SCOPE.txt absent.

## 2_ROOT_CAUSE

```
gate/file-scope exige :
  1. Exactement 1 GO dans docs/chantiers/ dans le diff PR
  2. docs/chantiers/<GO_ID>/FILE_SCOPE.txt présent au moment du run
  3. Tous les fichiers modifiés couverts par FILE_SCOPE.txt

child_extraction (PR #972)  — FILE_SCOPE.txt ABSENT → gate FAIL
child_loop_contract (PR #973) — FILE_SCOPE.txt ABSENT → gate FAIL
```

## 3_SCOPE

Ce child produit :

- Son propre `FILE_SCOPE.txt` (ce PR est le premier child research library à passer la gate)
- `docs/openclaw/governance/FILE_SCOPE_POLICY.md` — règle obligatoire going forward
- Plan de retrofix pour child_extraction et child_loop_contract (PRs séparées)

## 4_DELIVERABLES

| Fichier | Contenu |
| --- | --- |
| `docs/chantiers/.../FILE_SCOPE.txt` | Scope de ce GO (gate passe) |
| `docs/chantiers/.../00_INITIAL_PROJECT_DOC.md` | Ce document |
| `docs/chantiers/.../20_ACCEPTANCE_REPORT.md` | Rapport PASS |
| `docs/openclaw/governance/FILE_SCOPE_POLICY.md` | Règle obligatoire + template |

Retrofix (PRs séparées atomiques) :
| PR | Contenu |
| --- | --- |
| PR retrofix-extraction | `docs/chantiers/GO_*_CHILD_EXTRACTION_01/FILE_SCOPE.txt` |
| PR retrofix-loop-contract | `docs/chantiers/GO_*_CHILD_LOOP_CONTRACT_01/FILE_SCOPE.txt` |

## 5_INVARIANTS

- 0 runtime modifié
- Parent non fermé
- Index globaux non touchés
- Ce PR doit passer gate/file-scope (preuve que la mécanique est correcte)

## 6_ACCEPTANCE_CRITERIA

```
gate/file-scope = PASS sur ce PR
FILE_SCOPE_POLICY.md créé et documenté
Retrofix extraction + loop_contract mergés (PRs séparées)
20_ACCEPTANCE_REPORT.md rédigé
```
