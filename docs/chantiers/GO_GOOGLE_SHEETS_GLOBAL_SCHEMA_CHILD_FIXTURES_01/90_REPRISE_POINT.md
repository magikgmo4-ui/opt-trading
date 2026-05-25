---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01
status: open
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
---

# 90_REPRISE_POINT

## État

- Branche : `go/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01`
- Tests : 41 PASS (0 FAIL)
- Verdict : en cours → PR ouverte

## Fichiers clés

```text
tests/fixtures/google_sheets_global_schema/   ← 11 fixtures JSONL
tests/test_google_sheets_fixtures.py          ← validateur + 41 tests
docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01/
```

## Reprendre depuis ici

Pour étendre les fixtures :
1. Ajouter des rows dans le fichier JSONL concerné.
2. Relancer `python3 -m pytest tests/test_google_sheets_fixtures.py -q`.
3. Vérifier 0 FAIL.

Pour ajouter un nouveau tab :
1. Ajouter dans `CANONICAL_TABS` et `SCHEMA` dans `test_google_sheets_fixtures.py`.
2. Créer `tests/fixtures/google_sheets_global_schema/<tab>.jsonl`.
3. Ajouter tests `TestFixtureFilesExist` et `TestFixtureValidation`.

Pour câbler le writer Google Sheets :
- Voir `40_GAPS_AND_NEXT_GO.md` — prérequis credentials.
- Ne pas modifier ce child GO. Ouvrir un child dédié.

## Prochain GO recommandé

`GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01`
