---
doc_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01_SOURCE_SCORING_AND_RESOLVER_PLAN
doc_type: plan
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 30_SOURCE_SCORING_AND_RESOLVER_PLAN

## Objet

Definir la trajectoire source scoring + best-value resolver sans l'implementer dans ce parent.

## Principe

Une meme donnee peut avoir plusieurs sources. Chaque source a un score. La valeur publiee dans la view Data Center est la meilleure valeur resolue selon une policy explicite.

```text
candidate sources
-> source_score.v1
-> source_evidence.v1
-> resolver_decision.v1
-> canonical_value.v1
-> data/data_center/views/<contract_class>/
```

## Scores cibles

```text
final_score =
  0.20 source_reliability
+ 0.20 freshness
+ 0.15 schema_validation
+ 0.15 completeness
+ 0.10 cross_source_consistency
+ 0.10 historical_accuracy
+ 0.05 latency
+ 0.05 permission
```

## Contracts a creer dans les child GO

- `source_score.v1.schema.json`
- `source_evidence.v1.schema.json`
- `canonical_value.v1.schema.json`
- `resolver_decision.v1.schema.json`

## Policy cible

Le resolver ne lit pas pour DeskPro un producer brut. Il repond a une requete logique :

```text
get_latest(symbol="BTCUSDT", data_key="open_interest")
```

Puis :

1. identifie `contract_class` ;
2. liste les sources candidates ;
3. controle fraicheur/schema/completude ;
4. calcule les scores ;
5. compare les valeurs concurrentes ;
6. selectionne la meilleure valeur ;
7. publie `resolver_decision` ;
8. met a jour la view canonique ;
9. laisse DeskPro consommer la view.

## Interdits

- Pas de resolver dans DeskPro.
- Pas de scoring source dans DeskPro.
- Pas de lecture directe de producer path par DeskPro.
- Pas de best value sans preuve de selection.
