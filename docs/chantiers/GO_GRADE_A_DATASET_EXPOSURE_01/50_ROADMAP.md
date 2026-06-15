# 50_ROADMAP

## Phase 1 — Exposition rapide (1 session)

Actions A1 — impact immediat Voice Operator, aucun nouveau service:

1. Enrichir `_handle_composite` spcx_full avec 14 champs spacex_super_desk
2. Enrichir `market_view` avec vraies donnees vision_analysis
3. Ajouter top 5 signaux Telegram filtres dans /read/alerts
4. Exposer deskpro analysis dans spcx_full

## Phase 2 — Enrichissement Voice (2-3 sessions)

1. Creer `/read/vision/{symbol}` pour requetes par symbole
2. Ajouter commandes: "Analyse BTC technique", "Analyse Gold technique"
3. Filtrer signaux Telegram par score minimum

## Phase 3 — Enrichissement DeskPro (3-5 sessions)

1. Dashboard multi-symboles
2. Stats signaux Telegram
3. Rapport GPT integre command-center

## KPI cible

| Metrique | Actuel | Cible Phase 1 | Cible Phase 3 |
|----------|--------|---------------|---------------|
| % champs SPCX exposes | 30% | 100% | 100% |
| % symboles vision exposes | 0% | 25% | 80% |
| % signaux Telegram filtres | 1% | 5% | 20% |
| % datasets Grade A en Voice | 20% | 50% | 80% |
