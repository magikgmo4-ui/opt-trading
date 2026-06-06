---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01_SCOPE_RULES
doc_type: rules
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 10_CANONICAL_SCOPE_AND_RULES

## Objet

Fixer les regles de canonisation de l'inventaire complet des donnees de desks professionnels.

## Scope inclus

L'inventaire couvre :

```text
P0  instrument master
P1  market quote / trade / OHLCV / book
P2  position / PnL / capital / risk
P3  orders / fills / execution
P4  liquidity / microstructure
P5  options / volatility / derivatives
P6  rates / credit / funding
P7  macro calendar / releases
P8  fundamentals / earnings / filings
P9  news / events / sentiment
P10 flows / positioning
P11 technical context
P12 models / research / signals
P13 alternative data
P14 crypto-specific
P15 commodities-specific
P16 FX-specific
P17 equity-specific
P18 compliance / restrictions
P19 ops / settlement
P20 desk memory
P21 data quality / lineage
```

## Role de l'inventaire

L'inventaire sert a :

1. mesurer la couverture Data Center ;
2. guider les prochains contracts ;
3. detecter les gaps ;
4. preparer le scoring multi-sources ;
5. guider la consommation DeskPro ;
6. eviter les doublons et les readers fantomes.

## Non-objectifs

Ce child ne doit pas :

- modifier `modules/data_center/registry/producers.json` ;
- modifier `modules/data_center/registry/consumers.json` ;
- creer un schema runtime ;
- creer un reader ;
- migrer un path legacy ;
- implementer le resolver ;
- fermer le parent.

## Regle de granularite

Une categorie pro desk ne doit pas etre fusionnee avec une autre pour simplifier l'inventaire.

Exemples :

- `market_quote` n'est pas equivalent a `liquidity_microstructure` ;
- `flow_positioning` n'est pas equivalent a `technical_context` ;
- `news_event` n'est pas equivalent a `macro_event` ;
- `data_quality_state` n'est pas une metadonnee secondaire : c'est une categorie P21 complete.

## Regle Data Center

L'inventaire decrit ce que Data Center doit couvrir. DeskPro consomme ensuite les views Data Center, mais ne possede pas l'inventaire comme structure d'ingestion.
