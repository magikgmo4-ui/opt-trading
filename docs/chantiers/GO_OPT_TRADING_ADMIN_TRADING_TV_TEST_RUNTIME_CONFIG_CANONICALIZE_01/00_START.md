---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01
machine: admin-trading
status: active
lifecycle_stage: config_canonicalize
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01/95_EXECUTION_RESULTS.md
---

# 00_START — GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01

## Objet

Canoniser la configuration runtime `TV_TEST` qui a permis le PASS 11/11,
sans exposer de secret et sans activer de trading reel.

Cela remplit le gap : `TV_TEST` fonctionne sur admin-trading, mais la
necessite d'avoir une entree dans `risk_config.json` n'est documentee
que dans le closeout d'execution, pas sous forme canonique.

## Contexte

- `TV_TEST` flux `/tv -> record_event` valide (11/11 PASS)
- `state/risk_config.json` est local a admin-trading, non tracke (`.gitignore`)
- `state/` entier est dans `.gitignore` → pas de fichier example possible dans `state/`
- La config `TV_TEST` est identique a `PAPER_TEST` en structure
- Aucun secret dans cette config (equity=10000, risk_pct=0.01 sont des valeurs safe par defaut)

## Structure

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_CURRENT_RUNTIME_STATE.md` | Etat actuel de `risk_config.json` sur admin-trading |
| `20_TV_TEST_CONFIG_DECISION.md` | Decision : documenter le pattern sans fichier example |
| `30_SAFE_CONFIG_PATTERN.md` | Pattern canonique (reproductible) |
| `40_VERIFICATION_PLAN.md` | Plan de verification runtime |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Contraintes

- Aucun secret dans le repo
- Aucun fichier dans `state/` (gitignore)
- Aucun `.env` reel
- Aucun trade reel
- `trade_allowed=false`
- `admin_trading_runtime=false`
- Patch minimal
