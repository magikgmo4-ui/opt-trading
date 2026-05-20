---
doc_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01_RESEARCH_SOURCES
doc_type: research_sources
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: draft
lifecycle_stage: research
topic_keys: [opt-trading, strategy, daily_scalping, research_sources, ORB, VWAP, SMC_ICT]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/00_INITIAL_PROJECT_DOC.md
---

# 10_RESEARCH_SOURCES

## Objectif

Conserver les mots-clés, familles de sources et constats utilisables pour reprendre la recherche sans dépendre de la session ChatGPT.

## Mots-clés EN

```text
opening range breakout intraday strategy
5 minute ORB stocks in play
intraday momentum strategy SPY
VWAP intraday trend confirmation
VWAP pullback scalping strategy
liquidity sweep CHOCH BOS retest
SMC liquidity grab market structure
Donchian channel crypto trend following
scalping transaction costs slippage
day trading margin risk
CFD retail accounts lose money
```

## Mots-clés FR

```text
stratégie scalping intraday robuste
cassure range ouverture trading
VWAP scalping intraday
balayage liquidité CHOCH BOS
stratégie momentum intraday
frais slippage scalping
gestion risque day trading
CFD risque levier particuliers
```

## Sources / familles consultées

### ORB / Opening Range Breakout

- SSRN : recherche sur `Opening Range Breakout for Stocks in Play`, utile pour la famille ORB 5 minutes + volume relatif.
- QuantConnect Research : implémentation ORB stocks in play, utile pour transformer la logique en protocole backtest.

### Momentum intraday

- SSRN : stratégies intraday momentum SPY avec exits dynamiques, trailing / VWAP.
- À utiliser comme preuve qu'une routine intraday robuste doit filtrer le régime et la sortie, pas multiplier les micro-entrées.

### VWAP

- Investopedia : définition VWAP et usage intraday.
- National Bank Direct Brokerage : VWAP comme support/résistance et confirmation de tendance intraday.

### SMC / ICT

- Sources éducatives trading : structure de marché, liquidity grab, BOS, CHOCH, order block, FVG, retest.
- Niveau de preuve : utile comme langage de lecture et confirmation visuelle, moins robuste comme preuve statistique autonome.

### Risque / réglementation / coûts

- SEC : risques day trading, attention continue, coûts, marge.
- ESMA : pertes importantes des comptes CFD retail et restrictions liées au levier.
- FINRA : évolution des règles de marge intraday effective en 2026 côté US.

## 13_ESTABLISHED

- ORB est prioritaire pour la mesure et le backtest.
- VWAP doit rester un filtre de régime.
- SMC/ICT ne doit pas être traité comme preuve statistique autonome.
- Toute stratégie scalping sans modélisation de coûts, spread, slippage et risk cap est non robuste.

## 14_HYPOTHESIS

- Combiner ORB + VWAP + SMC peut réduire les faux signaux de chaque famille isolée.
- Cette combinaison doit être prouvée par backtest local avant d'être promue.

## 16_TODO

- Ajouter les liens exacts de sources dans un lot futur si une documentation bibliographique stricte est demandée.
- Convertir les constats en critères backtestables.
