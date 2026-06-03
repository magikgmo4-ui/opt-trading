# Validation Plan

## Tests

```bash
python3 -m pytest tests/test_telegram_screener_parser.py tests/test_telegram_screener_normalizer.py -q
```

### Cas de test prevus

1. `test_coinglass_dict_to_candidate_valid` - Conversion d'un dict coinglass valide
2. `test_coinglass_dict_to_candidate_minimal` - Dict avec seulement les champs obligatoires
3. `test_screener_signal_to_candidate_trade` - ScreenerSignal trade -> SignalCandidate
4. `test_screener_signal_to_candidate_news` - ScreenerSignal news -> SignalCandidate
5. `test_screener_signal_to_candidate_alpha` - ScreenerSignal alpha -> SignalCandidate
6. `test_candidate_to_screener_signal_full` - SignalCandidate complet -> ScreenerSignal
7. `test_candidate_to_screener_signal_partial` - SignalCandidate partiel -> ScreenerSignal
8. `test_normalize_coinglass_dict` - Integration : dict coinglass -> ScreenerSignal
9. `test_screener_signal_roundtrip` - ScreenerSignal -> SignalCandidate -> ScreenerSignal preserve les champs
10. `test_to_dict_output` - SignalCandidate.to_dict() produit un dict attendu

## Verification Git

```bash
git diff --check
git status -sb
```

## Rollback

```bash
git checkout -- modules/telegram_screener/schema.py modules/telegram_screener/normalizer.py tests/test_telegram_screener_normalizer.py
git checkout -- docs/chantiers/GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01/
git checkout -- docs/index/inbox/GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01.md
```

## Criteres d'acceptation

1. `34 + N` tests passed (34 existants + nouveaux tests normalizer).
2. `git diff --check` ne produit aucun warning.
3. `git status -sb` montre uniquement les fichiers du FILE_SCOPE.
4. Aucune modification des parseurs existants.
5. Aucune modification des fixtures existantes.
