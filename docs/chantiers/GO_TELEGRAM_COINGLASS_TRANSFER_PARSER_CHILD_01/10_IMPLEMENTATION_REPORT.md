# Implémentation parser transfer `大额转账` Coinglass

**Generated:** 2026-06-03 05:30 UTC  
**Branch:** `go/GO_TELEGRAM_COINGLASS_TRANSFER_PARSER_CHILD_01`  
**Base:** `sot/mainline` (PR #1073 merged: `fd0e1163`)

---

## 1. Problème

Le parser coinglass (`parse_coinglass_alert`) ne reconnaissait que le format **Hyperliquid whale alert** (positions leviers). Un format différent — **`大额转账`** (large transfer notification) — retournait `None`, compté comme `UNKNOWN_RAW` dans les métriques de capture.

Sur 20 messages coinglass : **1 unknown** = message `215043` : transfer `6,368 WBTC ($422M)`.

---

## 2. Solution

### Fichier modifié : `modules/telegram_screener/parser/coinglass_parser.py`

- Nouvelle regex `_COINGLASS_TRANSFER_RE` pour le format `大额转账`
- Nouvelle fonction `parse_coinglass_transfer()` retournant `telegram_transfer_candidate.v1`
- `parse_coinglass_alert()` essaie d'abord whale alert, puis transfer, puis `None`

### Champs extraits (transfer)

| Champ | Source | Exemple |
|---|---|---|
| `asset` | `#ASSET` | `WBTC` |
| `amount_asset` | `**AMOUNT**` | `6368.0` |
| `amount_usd` | `(**AMOUNT** USD)` | `422638351.0` |
| `from_entity` | `从 X 钱包` | `未知` ou exchange |
| `to_entity` | `转移到 Y 钱包` | `未知` ou exchange |
| `from_identified` | `from_entity ≠ 未知` | `false` |
| `to_identified` | `to_entity ≠ 未知` | `false` |
| `transaction_type` | constant | `TRANSFER` |
| `confidence` | MEDIUM si both identified, LOW sinon | `LOW` |
| `parse_status` | PARSED si both identified, PARTIAL sinon | `PARTIAL` |

### Gestion des entités identifiées

Quand `from_entity` ou `to_entity` = `未知` (unknown), le parseur signale `from_identified=false` / `to_identified=false` et abaisse le confidence à `LOW` / `PARTIAL`. Si les deux entités sont nommées, `confidence=MEDIUM` / `PARSED`.

---

## 3. Fixtures

### Fichier modifié : `tests/fixtures/telegram_screener/coinglass_alert_samples.json`

Ajout d'un 6e sample — le message réel `215043` (WBTC transfer, `from=未知`, `to=未知`).

---

## 4. Tests

### Tests ajoutés dans `tests/test_telegram_screener_parser.py`

| Test | Description |
|---|---|
| `test_coinglass_transfer_format_parses` | Vérifie que le transfer sample retourne `telegram_transfer_candidate.v1` avec tous les champs |
| `test_coinglass_whale_still_parses_after_transfer_addition` | Vérifie que les 5 whale samples existants retournent toujours `telegram_trade_signal_candidate.v1` |

### Tests modifiés

- `test_valid_coinglass_alert_samples_parse` — devient type-aware (vérifie `schema` avant d'accéder aux champs spécifiques)
- `TestCoinglassDictToCandidate.test_valid_coinglass_dict` — filtre uniquement les whale samples
- `TestNormalizeCoinglassDict.test_integration` — filtre uniquement les whale samples

---

## 5. Résultat

```text
53 tests passed (parser + normalizer)
6 tests passed (collector_telegram)
59 total — 0 failed
```

---

## 6. Fichiers modifiés

| Fichier | Type |
|---|---|
| `modules/telegram_screener/parser/coinglass_parser.py` | Ajout regex transfer + `parse_coinglass_transfer()` |
| `tests/fixtures/telegram_screener/coinglass_alert_samples.json` | Ajout sample transfer #215043 |
| `tests/test_telegram_screener_parser.py` | Ajout tests transfer + protection type-aware |
| `tests/test_telegram_screener_normalizer.py` | Protection type-aware (filtre whale samples) |

---

## 7. Prochaines étapes

1. Merger cette PR
2. Re-capturer coinglass_alerts limit=20 — le unknown précédent devrait passer à PARSED
3. Passer à la stabilisation scheduler production coinglass_alerts + whale_alert_io
4. Traiter glassnode (filtrer messages vides) si pertinent
