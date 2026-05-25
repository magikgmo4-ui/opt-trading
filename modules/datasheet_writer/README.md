# datasheet_writer

Persiste les `TradeRecord` (résultats de trade) en JSONL + CSV dans `data/datasheet/`.

## Flow

```
TradeRecord → DatasheetWriter → trades_YYYYMMDD.jsonl + trades_YYYYMMDD.csv
```

## Commands

```bash
cmd.sh sanity   # validation complète
cmd.sh test     # 13 tests unitaires
cmd.sh write    # écrire un record via CLI
```

## Output

- JSONL : append, un objet JSON par ligne
- CSV : append, header écrit au premier write du jour
