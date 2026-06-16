# GO_MULTITF_SIGNAL_CALIBRATION_LIVE_01 — Initial Project Doc

## Objectif

Valider en live que les signaux CDP TradingView font monter/descendre les grades multi-TF correctement. Pas de nouvelle couche — seulement calibration, preuves live, tests.

## Règles

- Pas de nouveau contrat Data Center
- Pas de nouveau producer majeur
- Pas de broker, pas d'ordre, pas d'auto-trading
- Monitor-only strict
- Pas de termes execution/order/buy/sell dans les sorties

## Attendus

| Actif | État baseline | Trigger CDP attendu | Grade cible |
|---|---|---|---|
| SPCX | B+/62 vwap_reclaim | vwap_reclaim frais | B+ maintenu |
| BTC | C/34 support_watch | vwap_loss / vwap_reclaim / ORB | B/B+ |
| ETH | C/34 support_watch | vwap_loss / vwap_reclaim / ORB | B/B+ |
| SOL | C/34 support_watch | vwap_loss / vwap_reclaim / ORB | B/B+ |
| XAUUSD | C/34 support_watch | trigger + DXY/VIX cohérent | B/B+ |

## Critères PASS

- baseline capturée
- CDP events parsés
- SPCX B+/62 expliqué par vwap_reclaim
- BTC/ETH/SOL/XAUUSD restent C sans trigger fort
- downgrade stale testé
- Voice reflète les transitions
- 0 fallback, 0 crash
