# 40_LIVE_OBSERVATION_LOG — Journal d'observation live

## 2026-06-15 17:15 UTC — Baseline

### SPCX — B+/62 vwap_reclaim
- **Trigger** : CDP vwap_reclaim @ 171.5 (écrit 15:14 UTC)
- **Biais** : neutral/neutral (pas de trend data SPCX → CDP override)
- **Score** : htf=8, ltf=15, vwap=8, vol=8, macro=5, fresh=8, rr=6, backtest=4 = 62
- **Verdict** : B+ correct. Le CDP trigger + H4 neutral donne un setup de reclaim valide.
- **Risque** : si le signal vieillit > 4h sans nouveau trigger → downgrade à B-

### BTC — C/34 support_watch
- **Biais** : bearish/bearish aligned — contexte favorable pour short
- **Aucun trigger CDP** — pas de vwap_loss, pas de sweep
- **Score** : htf=5, ltf=5, vwap=10, vol=5, macro=5, fresh=8, rr=4, backtest=2 = 34
- **Verdict** : C correct. Attend vwap_loss ou ORB pour monter à B+.

### ETH — C/34 support_watch
- **Même structure que BTC** — bearish aligné, pas de trigger
- **Verdict** : C correct.

### SOL — C/34 support_watch
- **Même structure que BTC** — bearish aligné, pas de trigger
- **Verdict** : C correct.

### XAUUSD — C/34 support_watch
- **Biais** : bearish/bearish aligné
- **Prix** : 4430.0 (live)
- **Aucun trigger CDP**
- **Verdict** : C correct. Contexte DXY/VIX non intégré dans le scoring actuel.

## 2026-06-15 17:30 UTC — Transition BTC: C→B+ vwap_loss

### BTC vwap_loss → B+/68 vwap_rejection
- **Trigger** : CDP vwap_loss @ 66700 envoyé via curl → /tv/cdp
- **Avant** : C/34 support_watch
- **Après** : **B+/68 vwap_rejection** (+34 pts, +3 grades)
- **Voice** : "setup vwap_rejection. grade B+. score 68/100. raison: H4 bearish; CDP vwap_loss"
- **Rapport marché** : BTC B+(68) maintenant #1 devant SPCX B+(62)
- **Latence** : <5 secondes du POST CDP à la réponse Voice
- **Pipeline** : /tv/cdp → signal_event.v1 → multitf_analysis_producer → multitf_setup_scorer → Voice

### Bug corrigé pendant le test
- **Symbol mismatch** : Les événements CDP utilisent `BTCUSDT.P` mais le producer indexait par `BTC`. Ajout d'une table de normalisation `_SYM_NORM` dans le producer.

### Verdict
La transition C→B+ est instantanée et fiable. Le pipeline complet fonctionne en <5 secondes.
Deux événements CDP ont maintenant été testés (vwap_reclaim + vwap_loss), les deux produisent B+.
