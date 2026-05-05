---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01_30_PATTERN
doc_type: chantier/pattern
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01
machine: admin-trading
status: active
lifecycle_stage: config_canonicalize
---

# 30_SAFE_CONFIG_PATTERN — Pattern canonique TV_TEST

## Emplacement

```
/opt/trading/state/risk_config.json
```

Non tracke par git (`state/` dans `.gitignore`). Applique localement sur admin-trading.

## Structure minimale requise pour TV_TEST

```json
{
  "accounts": {
    "TV_TEST": {
      "equity": 10000,
      "risk_pct": 0.01,
      "min_qty": 0.001,
      "qty_step": 0.001
    }
  }
}
```

## Champs expliques

| Champ | Valeur safe | Role |
| --- | --- | --- |
| `equity` | `10000` | Capital fictif pour le risk sizing. Valeur de test uniquement. |
| `risk_pct` | `0.01` | 1% du capital par trade. `risk_usd = 10000 * 0.01 = 100` |
| `min_qty` | `0.001` | Quantite minimale (arrondi) |
| `qty_step` | `0.001` | Pas d'arrondi de quantite |

Avec `price=100, sl=95` :
- `distance = |100-95| = 5`
- `risk_usd = 10000 * 0.01 = 100`
- `qty = 100 / 5 = 20`
- `risk_real = 20 * 5 = 100`

## Structure complete (avec engines existants)

```json
{
  "accounts": {
    "TV_TEST": {
      "equity": 10000,
      "risk_pct": 0.01,
      "min_qty": 0.001,
      "qty_step": 0.001
    },
    "PAPER_TEST": {
      "equity": 10000,
      "risk_pct": 0.01,
      "min_qty": 0.001,
      "qty_step": 0.001
    },
    "COINM_SHORT": {
      "equity": 10000,
      "risk_pct": 0.01,
      "min_qty": 0.001,
      "qty_step": 0.001
    }
  },
  "gold_cfd": {
    "units_are_oz": true
  }
}
```

## Regles de securite

- `equity` doit etre une valeur fictive de test (pas le solde reel du compte)
- `risk_pct` doit etre faible (0.01 ou moins) pour les engines de test
- Aucun token, URL, cle API dans cette config
- Les engines de trading reel (`COINM_SHORT`, `USDTM_LONG`, `GOLD_CFD_LONG`) utilisent des valeurs reelles
  mais ces valeurs ne sont pas dans le repo non plus (`.gitignore`)

## Commande de validation

```bash
python3 -c "
import json
with open('state/risk_config.json') as f:
    cfg = json.load(f)
assert 'TV_TEST' in cfg.get('accounts', {}), 'TV_TEST missing'
tv = cfg['accounts']['TV_TEST']
assert tv['equity'] > 0, 'equity must be > 0'
assert tv['risk_pct'] > 0, 'risk_pct must be > 0'
print('PASS: TV_TEST config valid')
"
```

## Correspondance code

Cette config est consommee par :
- `webhook_server.py:225` : `load_risk_config()` → lit `state/risk_config.json`
- `webhook_server.py:229` : `risk_calc.calculate_quote(acct, engine, price, sl, cfg)`
- `modules/risk_engine/app/risk_calculator.py:66` : `calculate_quote()` utilise `equity` et `risk_pct`

Les engines reconnus qui passent par ce chemin :
- `TV_TEST` (bypass perf ledger, pas de PAPER_TEST)
- `PAPER_TEST` (execution papier)
- `COINM_SHORT`, `USDTM_LONG`, `GOLD_CFD_LONG` (trading reel, hors scope de ce GO)
