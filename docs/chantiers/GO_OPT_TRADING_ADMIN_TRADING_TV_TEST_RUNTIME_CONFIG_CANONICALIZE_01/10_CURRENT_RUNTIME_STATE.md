---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01_10_STATE
doc_type: chantier/state
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01
machine: admin-trading
status: active
lifecycle_stage: config_canonicalize
---

# 10_CURRENT_RUNTIME_STATE — Etat actuel

## Fichier

`/opt/trading/state/risk_config.json` (sur admin-trading, non tracke par git)

## Contenu actuel (apres fix TV_TEST)

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

## Historique

| Date | Action |
| --- | --- |
| Avant 2026-05-05 | `accounts` : `PAPER_TEST`, `COINM_SHORT` (pas de `TV_TEST`) |
| 2026-05-05 17:57 | Ajout runtime de `TV_TEST` sur admin-trading (fix local) |
| 2026-05-05 17:57 | Test 11/11 PASS avec `TV_TEST` |

## Pourquoi le fix etait necessaire

```text
POST /tv engine=TV_TEST
  -> risk_quote('TV_TEST', price=100, sl=95)
    -> load_risk_config() -> accounts.get('TV_TEST', {}) -> acct={}
    -> _get_equity_and_risk_pct(acct={}) -> equity=0, risk_pct=0
    -> risk_usd = 0 * 0 = 0
    -> calculate_quote() returns qty=0
  -> webhook_server.py:407 -> HTTP 400 "Risk quote invalid (qty/risk is 0)"
```

Avec `TV_TEST` dans `accounts` :
```text
  -> accounts.get('TV_TEST') -> {equity:10000, risk_pct:0.01}
  -> equity=10000, risk_pct=0.01 -> risk_usd=100
  -> distance=|100-95|=5 -> qty=100/5=20
  -> qty=20, risk_usd=100 -> VALIDE
  -> 200 {"ok": true}
```

## Verifications de securite

- `equity: 10000` est une valeur fictive de test (pas le solde reel)
- `risk_pct: 0.01` est une valeur safe (1% du fictif)
- Aucun token, URL, cle privee dans cette config
- La config est strictement locale a admin-trading

## RISKS

- À qualifier.
