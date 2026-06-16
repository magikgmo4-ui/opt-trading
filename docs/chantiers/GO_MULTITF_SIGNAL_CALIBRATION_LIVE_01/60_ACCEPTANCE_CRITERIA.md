# 60_ACCEPTANCE_CRITERIA — Critères d'acceptation

## Critères PASS

- [x] Baseline capturée (5 actifs, scores+grades+biais)
- [x] CDP events parsés (1 event : SPCX vwap_reclaim)
- [x] SPCX B+/62 expliqué par vwap_reclaim CDP
- [x] BTC/ETH/SOL/XAUUSD restent C/34 sans trigger fort
- [x] Voice reflète les grades réels (Rapport marché, Priorités, Attention)
- [x] Monitor-only strict (0 terme execution/broker/order)
- [x] Tests passent (147/147)
- [x] Pas de nouveau contrat, pas de nouvelle couche
- [ ] Downgrade stale vérifié en live (à observer sur 12-24h)
- [ ] Upgrade B→A vérifié avec nouveau trigger CDP (à observer)
- [ ] Tests de calibration spécifiques écrits

## Vérifications Voice live (admin-trading)

| Commande | Attendus | Statut |
|---|---|---|
| Rapport marché | "Top setups: SPCX B+(62)" | ✅ |
| Priorités | "SPCX B+ score 62 — vwap_reclaim" | ✅ |
| Attention | "BTC: completude 50%" | ✅ |
| Resume SPCX | "Setup CDP vwap_reclaim grade B+" | ✅ |
| Analyse BTC | "biais H4 bearish, grade C, score 34" | ✅ |
| Analyse Gold | "Prix 4430.0, grade C, score 34" | ✅ |

## Reste à observer

1. SPCX downgrade si signal stale > 4h (pas encore arrivé)
2. BTC/ETH/SOL/XAUUSD upgrade si nouveau CDP trigger (pas encore arrivé)
3. Contradiction HTF/LTF si biais divergent (pas de cas actuel)
