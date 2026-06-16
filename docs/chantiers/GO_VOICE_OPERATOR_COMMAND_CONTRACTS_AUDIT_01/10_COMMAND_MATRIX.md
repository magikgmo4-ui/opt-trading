# 10_COMMAND_MATRIX — Toutes les commandes /voice

## Mapping Commande → Intent → Endpoint → Source → Sortie attendue

| Commande UI | Intent | Endpoint | Source primaire | Sortie attendue |
|---|---|---|---|---|
| Etat systeme | system_status | /read/system | /read/system + DC registry | Systeme OK. Data Center PASS. Pipeline hourly OK. LocalCMS OK. Voice API OK. 0 erreurs critiques. |
| Rapport marche | market_view | /read/composite | /read/spacex + vision_analysis.v1 | SPCX 171, BTC trend X, Gold trend Y, DXY/VIX risk-on/off, top mover, alerte majeure |
| Analyse BTC | btc_full | /read/composite | vision_analysis.v1 + market_metrics + signal_event | Prix, trend, VWAP, signal_event, funding/OI si dispo, invalidation |
| Analyse Gold | gold_full | /read/composite | vision_analysis.v1 + perf + fx_context | Prix, trend H4, DXY, setup CFD, danger, invalidation |
| Resume SPCX | spcx_full | /read/composite | /read/spacex + cc_path + true_value | Prix, VWAP, edge, true value grade, setup, alertes, freshness |
| Alertes Telegram | telegram_alerts | /read/composite | /read/alerts | Nombre alertes, top 3, canaux, symboles, urgence |
| Setups actifs | setups_all | /read/composite | /read/setups | Top setups classes par score, symbole, direction, invalidation |
| Setup BTC | setup_detail | /read/composite | /read/setup?symbol=BTC | Setup actif BTC ou "aucun setup actif", avec raison |
| Setup Gold | setup_detail | /read/composite | /read/setup?symbol=XAUUSD | Setup XAU actif ou attente |
| Setup SPCX | setup_detail | /read/composite | /read/setup?symbol=SPCX | Setup SPCX + grade + entry/invalidation |
| Score BTC | score_detail | /read/composite | true_value.v1 | score, freshness, source, missing fields |
| Score Gold | score_detail | /read/composite | true_value.v1 | score, source, missing fields |
| Score SPCX | score_detail | /read/composite | true_value.v1 | true_value, confidence, hype, risk, edge, setup |
| Rapport quotidien | daily_report | /read/composite | daily reports + true_value daily | resume jour + top risques + top signaux + perf |
| Priorites | priorities | /read/composite | priority_engine + all sources | Top 5 avec raison : score, fraicheur, impact |
| Attention | attention | /read/composite | alerts + stale + disagreement + high risk | Top 3 risques + pourquoi |
| Top movers | top_movers | /read/composite | vision_analysis + market_metrics | actifs qui bougent + prix/variation |
| Resume executif | exec_summary | /read/composite | all summaries | 3 faits, 1 risque, 1 prochaine action |
| Watchlist IA | watchlist_ia | /read/composite | true_value.v1 | classement IA par true value / momentum |
| Watchlist spatial | watchlist_spatial | /read/composite | true_value.v1 | classement spatial par true value |
