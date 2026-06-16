# 40_GAPS_AND_MISSING_INFO

## Bugs identifies et corriges

### Bug #1: _get_vision_markets() undefined
- Emplacement: main.py:2603 dans btc_full
- Symptome: NameError au runtime
- Correction: definir _get_vision_markets() comme closure lisant vision_analysis DC views

### Bug #2: params non defini dans setup_detail / score_detail
- Emplacement: main.py:2642, main.py:2657
- Symptome: NameError — params n'est pas dans le scope de _handle_composite()
- Correction: ajouter `params=None` comme parametre de _handle_composite(), passer depuis /voice/query

### Bug #3: whats_new defini deux fois
- Emplacement: main.py:2414 et main.py:2734
- Symptome: code mort inoffensif
- Correction: supprimer la deuxieme definition

## Gaps de reponse

### gold_full: pas de prix/trend
- Actuel: Seulement trades perf, informations statiques
- Attendu: Prix XAUUSD, trend H4, DXY context, setup CFD
- Action: lire vision_analysis/by_symbol/OANDA:XAUUSD.json

### exec_summary: trop agrege
- Actuel: "5 setups actifs. 2 alertes critiques. SPCX setup X."
- Attendu: 3 faits, 1 risque, 1 prochaine action
- Action: restructurer pour donner faits + risque + next

### priorities: raisons insuffisantes
- Actuel: items classes par priorite mais sans raison explicite
- Attendu: chaque item avec pourquoi (score, fraicheur, impact)
- Action: ajouter raison dans spoken_text

### attention: manque causes explicites
- Actuel: "X points a surveiller" sans dire pourquoi
- Attendu: cause explicite (stale, stop proche, source degraded)
- Action: ajouter raison dans cards et spoken_text

### top_movers: pas de prix/variation
- Actuel: seulement trend depuis vision_analysis
- Attendu: prix + variation si disponible dans market_metrics
- Action: lire market_metrics pour prix

## Gaps API /read

### read_system: pas de Data Center registry
- Actuel: services_running, critical_alerts, pipeline_state
- Attendu: nombre de contrats DC, statut registry
- Action: ajouter data_center_contracts, data_center_status

### read_score: BTC/XAUUSD non geres
- Actuel: seulement SPCX via snapshot
- Attendu: BTC/XAUUSD via true_value DC views
- Action: lire spacex_true_value.v1 pour tous les symboles
