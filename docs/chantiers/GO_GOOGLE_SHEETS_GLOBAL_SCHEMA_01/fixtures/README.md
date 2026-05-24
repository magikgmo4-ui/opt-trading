---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_FIXTURES_README
doc_type: fixtures_readme
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
source_kind: canonical
updated_at: 2026-05-24
---

# fixtures/ — Google Sheets global schema

## Objectif

Matérialiser des fixtures-first pour le schéma global Google Sheets sans API live.

## Format cible (par défaut)

- CSV (un fichier par feuille)
- UTF-8
- en-têtes = colonnes canoniques
- timestamps ISO UTC
- une fixture minimale doit couvrir :
  - 1 ligne “happy path”
  - 1 ligne “optional fields missing”

## Règles

```text
- pas de sheet_id
- pas de credentials
- pas d’URL docs.google.com
- pas de données sensibles
```

