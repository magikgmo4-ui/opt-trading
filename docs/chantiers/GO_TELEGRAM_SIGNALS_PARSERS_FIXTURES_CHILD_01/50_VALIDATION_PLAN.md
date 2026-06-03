# Validation Plan

## Commands

```bash
git status -sb
git diff --check
python3 -m pytest tests/test_telegram_screener_parser.py modules/collector_telegram/tests/test_collector_telegram_real_fixtures.py
```

## Expected results

- nouveau chantier docs present
- fixtures `coinglass_alerts` presentes
- parseur minimal coinglass parse les 5 exemples reels
- aucun acces reseau
- aucune fuite de secret dans les fichiers ajoutes

## Rollback

1. supprimer le dossier `docs/chantiers/GO_TELEGRAM_SIGNALS_PARSERS_FIXTURES_CHILD_01/`
2. supprimer `docs/index/inbox/GO_TELEGRAM_SIGNALS_PARSERS_FIXTURES_CHILD_01.md`
3. supprimer le parseur et la fixture ajoutes
4. retirer les imports et tests associes
