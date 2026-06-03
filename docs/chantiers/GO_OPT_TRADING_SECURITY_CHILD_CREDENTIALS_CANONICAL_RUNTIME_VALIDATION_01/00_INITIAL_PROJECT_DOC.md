---
doc_id: GO_OPT_TRADING_SECURITY_CHILD_CREDENTIALS_CANONICAL_RUNTIME_VALIDATION_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_SECURITY_CHILD_CREDENTIALS_CANONICAL_RUNTIME_VALIDATION_01
parent_go: GO_OPT_TRADING_SECURITY_CREDENTIALS_REGISTRY_FULL_MAP_01
status: impl
created_at: 2026-06-03
base_commit: eb927cfa
---

# GO_OPT_TRADING_SECURITY_CHILD_CREDENTIALS_CANONICAL_RUNTIME_VALIDATION_01

## Objectif

Valider post-merge le panneau credentials LocalCMS et le CLI de rotation, puis
produire la méthode canonique credentials + intégrations actives pour référence
opérationnelle permanente.

## Contexte de rattachement

- Parent : `GO_OPT_TRADING_SECURITY_CREDENTIALS_REGISTRY_FULL_MAP_01`
- PR mergée : #1085 — `feat(localcms): credentials panel + rotation CLI form`
- Base : `sot/mainline @ eb927cfa`
- Smoke local : PASS (voir `10_RUNTIME_VALIDATION_REPORT.md`)

## Périmètre (doc-only)

Ce GO ne modifie pas de code. Il documente et valide l'état post-merge.

```
docs/chantiers/GO_OPT_TRADING_SECURITY_CHILD_CREDENTIALS_CANONICAL_RUNTIME_VALIDATION_01/
  00_INITIAL_PROJECT_DOC.md         — ce fichier
  10_RUNTIME_VALIDATION_REPORT.md   — PASS/FAIL par check
  20_CREDENTIALS_CANONICAL_METHOD.md — méthode canonique storage + rotation
  30_EXTERNAL_INTEGRATIONS_ACTIVE_MAP.md — cartographie intégrations actives/absentes
  40_GAPS_AND_NEXT_GO.md            — gaps identifiés + candidats GO suivants
  FILE_SCOPE.txt
```

## Livrables PR #1085 validés

| Livrable | Path | Statut |
|----------|------|--------|
| Panel HTML | `GET /credentials` | PASS syntax + runtime |
| API JSON | `GET /credentials/json` | PASS |
| CLI form | `scripts/credentials_form.py` | PASS --status |
| Chantier doc | `GO_OPT_TRADING_LOCALCMS_CREDENTIALS_PANEL_01` | MERGED |
| Sidebar link | LocalCMS UI / Security | MERGED |
| FILE_SCOPE.txt | gate/file-scope | PASS |

## Règle anti-fuite

Aucun document de ce chantier n'affiche de valeur secrète.
Statuts uniquement : `SET` / `ABSENT` / `UNKNOWN` / `FUTURE`.
