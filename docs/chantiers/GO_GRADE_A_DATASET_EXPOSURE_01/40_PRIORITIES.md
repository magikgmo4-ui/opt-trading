# 40_PRIORITIES

## A1 — Valeur immediate Voice (sans nouveau code serveur)

| Action | Dataset | Effort | Impact |
|--------|---------|--------|--------|
| Exposer vision_analysis symboles dans Vue marche | vision_analysis | Moyen | 25 symboles visibles |
| Completer SPCX complet avec 14 champs manquants | spacex_super_desk | Faible | +70% champs |
| Ajouter signaux Telegram filtres (top 5 par score) | telegram_signals | Faible | +qualite signaux |
| Exposer analyse GPT dans spcx_full | deskpro_analysis | Faible | +analyse texte |

## A2 — Valeur DeskPro

| Action | Dataset | Effort |
|--------|---------|--------|
| Dashboard vision multi-symboles | vision_analysis | Eleve |
| Filtrer signaux Telegram par score > seuil | telegram_signals | Moyen |
| Exposer rapport GPT dans command-center | deskpro_analysis | Faible |

## A3 — Valeur Analytics

| Action | Dataset | Effort |
|--------|---------|--------|
| Dashboard usage vision (symboles les plus consultes) | vision_analysis | Moyen |
| Stats signaux Telegram (winrate par channel) | telegram_signals | Eleve |
| Tracking exposition datasets | voice_events | Faible |
