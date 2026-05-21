---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01_BOT_VISION_VALIDATION_LAYER
doc_type: validation_protocol
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
status: open
updated_at: 2026-05-20
---

# 50_BOT_VISION_VALIDATION_LAYER

## Rôle

Bot vision / visual_context est une couche d'évidence visuelle, pas une source OHLCV.

```
backtest numérique → setups détectés mécaniquement
bot vision         → confirmation structure visuelle (CHOCH/BOS/FVG/OB) sur screenshot
```

L'opérateur peut utiliser bot vision pour valider que la condition CHOCH détectée par le runner correspond à ce qu'un trader SMC verrait sur le chart TradingView. C'est une validation humaine augmentée, pas une entrée de décision automatique.

## Contrat visual_context existant

Le repo définit le contrat `visual_context` avec les champs :

| Champ | Description |
|---|---|
| `source` | origine du screenshot (ex: tradingview, broker_chart) |
| `capture_id` | identifiant unique de la capture |
| `symbol` | ex: XAUUSD |
| `timeframe` | ex: M5, M15 |
| `captured_at` | timestamp UTC de la capture |
| `image_ref` | chemin ou URL du screenshot |
| `status` | ex: pending, validated, rejected |
| `chart_source` | ex: tradingview_web, mt5_chart |
| `signal_event_ref` | référence au setup / signal associé |

## Protocole de validation visuelle

### Étape 1 — Backtest numérique produit une liste de setups

```text
setup_id: XAUUSD_M5_20240315_08:45
variant: SMC_SWEEP_ONLY
direction: long
entry_bar: 1250
entry_price: 2185.40
sweep_low: 2182.10
choch_bar: 1253
```

### Étape 2 — Bot vision capture le chart correspondant

```text
symbol: XAUUSD
timeframe: M5
timestamp_range: [2024-03-15 08:30, 2024-03-15 09:15]
→ screenshot TradingView ou MT5 chart
→ annoté : swing low, sweep wick, CHOCH candle, VWAP line
→ image_ref: artifacts/visual_context/XAUUSD_M5_20240315_0845.png
```

### Étape 3 — Opérateur ou LLM vision confirme

Critères de validation :

| Critère | Attendu |
|---|---|
| Sweep identifiable | wick visible sous le swing low précédent |
| CHOCH visible | close au-dessus d'un récent swing high |
| FVG / Order Block | zone de retest identifiable |
| VWAP alignment | prix au-dessus de VWAP pour long |
| Contexte propre | pas de news candle, pas de gap |

```text
status: validated / rejected
notes: "CHOCH clair sur bar +3 après sweep, FVG visible sur M15"
```

### Étape 4 — Mise à jour du score setup

Un setup validé visuellement peut recevoir un bonus `visual_confirmed: true` dans le journal.

```python
# Dans results_to_journal_df — enrichissement optionnel
"visual_confirmed": setup.extra.get("visual_confirmed", False),
"visual_notes": setup.extra.get("visual_notes", ""),
```

## Ce que ce protocole n'est PAS

- Bot vision ne génère pas les OHLCV
- Bot vision ne remplace pas le calcul numérique des indicators
- TradingView ne doit pas être la source de truth — il confirme, il n'initie pas
- Le runner ne doit pas dépendre de bot vision pour fonctionner

## Scope de la validation visuelle dans ce GO

Dans ce rework, la couche bot vision est **documentée comme protocole** mais pas encore implémentée en code. L'objectif est de définir où elle s'insère dans le pipeline, pour que l'implémentation future soit cadrée.

## Implémentation future (hors scope immédiat)

```
tools/strategy/daily_scalping/visual_validator.py
  → génère des URL TradingView pré-paramétrées par setup
  → prépare le payload visual_context à remplir
  → lit le retour validé et injecte dans le journal
```
