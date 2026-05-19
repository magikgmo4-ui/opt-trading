---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01
surface: ADMIN_TRADING
source_kind: findings
updated_at: 2026-05-19
---

# 10_TIMEOUT_FINDINGS

## Base observee

Le GO P0 precedent a produit :

| Page ID | Resultat |
| --- | --- |
| `tv_btc_h1` | PASS complet |
| `tv_xau_h1` | timeout `networkidle` |
| `cg_btc_flow` | timeout `networkidle` |

## Hypothese

`networkidle` est trop strict pour des pages qui gardent des connexions ouvertes ou qui chargent continuellement des donnees.

## Nouveaux constats

Deux smokes dynamiques ont ete executes.

### Smoke A

Fenetre : `2026-05-19T04:02:45-04:00` a `2026-05-19T04:05:12-04:00`.

| Page ID | Strategy | Resultat |
| --- | --- | --- |
| `tv_btc_h1` | `networkidle`, 30s, wait 3s | PASS capture + ingestion + extraction |
| `tv_xau_h1` | `domcontentloaded`, 60s, wait 10s | PNG + JSON + ingestion + extraction, mais spinner |
| `cg_btc_flow` | `domcontentloaded`, 60s, wait 12s | timeout avant screenshot |

### Smoke B

Fenetre : `2026-05-19T04:07:22-04:00` a `2026-05-19T04:09:54-04:00`.

Profil ajuste : XAU wait 30s, Coinglass URL simplifiee `https://www.coinglass.com/pro/futures/LiquidationHeatMap?coin=BTC`.

| Page ID | Strategy | Resultat |
| --- | --- | --- |
| `tv_btc_h1` | `networkidle`, 30s, wait 3s | timeout intermittent |
| `tv_xau_h1` | `domcontentloaded`, 60s, wait 30s | timeout avant screenshot |
| `cg_btc_flow` | `domcontentloaded`, 60s, wait 20s | timeout avant screenshot |

## Interpretation

- L'ajout de `domcontentloaded` corrige partiellement le blocage initial : XAU a franchi `goto` dans Smoke A.
- La capture XAU de Smoke A n'est pas exploitable visuellement, car elle montre un spinner.
- Coinglass ne franchit pas `domcontentloaded` dans les deux essais.
- `networkidle` est intermittent pour TradingView et ne doit pas etre considere fiable pour le profil P0.

## Conclusion

La strategie configurable est necessaire et implementee, mais elle ne suffit pas encore a valider P0. Il faut un GO supplementaire pour une strategie de fallback apres timeout, une validation d'URLs plus stables, ou un skip JSON explicite pour les pages non capturables.
