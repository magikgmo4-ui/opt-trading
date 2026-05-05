---
doc_id: SIGNAL_DIAG_01_TV_CHECKLIST
doc_type: external_checklist
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_EXTERNAL_TRADINGVIEW_CHECKLIST

## Verification manuelle TradingView (operateur humain)

### 1. Verifier l'alerte

- [ ] Ouvrir TradingView -> Alertes
- [ ] Verifier que l'alerte "SmartMoney" ou equivalente est **active** (verte)
- [ ] Si inactive/grise: la reactiver

### 2. Verifier l'URL webhook

- [ ] Dans les parametres de l'alerte, champ "Webhook URL":
  ```
  https://phytogeographical-subnodulous-joycelyn.ngrok-free.dev/tv
  ```
- [ ] Verifier que l'URL termine par `/tv`
- [ ] Verifier que la methode est POST (par defaut)
- [ ] Si l'URL est differente: la mettre a jour

### 3. Verifier le message

- [ ] Le message JSON doit correspondre au format attendu par webhook_server.py
- [ ] Verifier les champs: symbol, side, entry, stop, qty, etc.

### 4. Verifier la strategie

- [ ] Le Pine Script doit etre **ajoute au graphique** et **actif**
- [ ] Verifier timeframe (H1?) et symbole
- [ ] Verifier qu'il n'y a pas d'erreur Pine Script (icone rouge !)

### 5. Test safe (optionnel)

- [ ] Si possible, creer une alerte de test avec un symbole en PAPER mode
- [ ] Ne PAS tester avec un symbole qui pourrait declencher un trade reel

### 6. Limites free tier

- [ ] Verifier le nombre d'alertes activees (TradingView free = limite)
- [ ] Si quota atteint: desactiver d'autres alertes ou upgrader

## URL webhook canonique

```
https://phytogeographical-subnodulous-joycelyn.ngrok-free.dev/tv
```

Confirmee dans journal.md et correspondant a l'URL ngrok actuelle.
