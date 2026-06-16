# 90_REPRISE_POINT

## GO_MULTITF_SIGNAL_CALIBRATION_LIVE_01 — Reprise point

### État à la fermeture

```
Baseline capturée       ✅ 5 actifs, scores+grades+biais
CDP events parsés       ✅ 1 event SPCX vwap_reclaim
SPCX B+/62 validé       ✅ expliqué par CDP trigger
BTC/ETH/SOL/XAUUSD C/34 ✅ pas de trigger fort → correct
Voice reflète           ✅ Rapport marché, Priorités, Attention
Monitor-only            ✅ 0 terme execution/broker/order
Tests                   ✅ 16 calibration + 147 total = 163 PASS
Docs chantier           ✅ 00→60 + 90 + 99
Baseline JSON           ✅ outputs/multitf_signal_calibration/
CDP events JSON         ✅ outputs/multitf_signal_calibration/
```

### À observer dans le temps

| Observation | Condition | Action si échouée |
|---|---|---|
| SPCX downgrade si stale > 4h | signal_event timestamp vieillit | Vérifier freshness_source score dans scorer |
| BTC/ETH/SOL/XAUUSD B+ si nouveau trigger | apparition vwap_loss/reclaim/ORB | Vérifier que le scorer détecte le setup |
| Pas de faux A sans confluence | pas de A sans volume+alignement | Ajuster les seuils dans scorer |

### Prochain GO

Attendre accumulation de CDP events (≥ 5-10 events) avant de recalibrer.
Ou : provoquer des events CDP manuellement pour tester les transitions.
