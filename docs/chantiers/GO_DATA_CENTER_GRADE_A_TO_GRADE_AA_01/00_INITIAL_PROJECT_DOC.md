# GO_DATA_CENTER_GRADE_A_TO_GRADE_AA_01

## 1_MASTER_TARGET

Transformer les datasets Grade A en datasets Premium (AA) pour le cockpit.
Objectif: moins de bruit, plus de signal. Chaque carte affichee doit etre utile a un trader.

## 7_CANONICAL STATE

5 datasets Grade A identifies. Exposition Voice ~50%.
Mais: SPCX complet 15 cartes, certaines redondantes ou peu utiles.

## Signal vs Bruit — par dataset

### spacex_super_desk

| Champ | Signal | Recommandation |
|-------|--------|----------------|
| price | ⭐⭐⭐ | Garder |
| gap_ipo_pct | ⭐⭐⭐ | Garder |
| volume | ⭐⭐ | Garder |
| vwap | ⭐⭐⭐ | Garder |
| edge_score | ⭐⭐⭐ | Garder |
| open_score | ⭐⭐ | Fusionner avec edge_score |
| action | ⭐⭐⭐ | Garder |
| confidence | ⭐⭐⭐ | Garder |
| top_setup | ⭐⭐⭐ | Garder |
| sector_regime | ⭐ | Retirer (peu fiable) |
| market_state | ⭐⭐⭐ | Garder |
| sources_ok | ⭐⭐ | Garder si < 100% |
| pipeline_healthy | ⭐⭐ | Garder si degraded |
| disagreement | ⭐ | Retirer (bruit) |
| rsi | ⭐⭐ | Garder si extreme |
| ipo_analogs | ⭐⭐ | Garder top 1 |
| orderflow_score | ⭐⭐⭐ | Garder |
| ownership_pressure | ⭐⭐⭐ | Garder |
| source_quality | ⭐⭐⭐ | Garder |
| vwap_state | ⭐⭐ | Garder |

**Resultat: 15 → 8 cartes utiles**

### vision_analysis

25 symboles. Afficher top 5 par score, pas tous.

### deskpro_analysis

10 actionable_signals. Afficher top 3 par confiance.

### telegram_signals

212 MB. Afficher 0 en l'etat — trop de bruit.
A n'exposer que si filtre par score > seuil.

### voice_events

OK — usage interne seulement.

## 6_FINAL_TARGET

Chaque commande Voice affiche:
- Max 8 cartes utiles
- Chaque carte a un label clair
- Pas de champs redondants
- Pas de champs sans valeur decisionnelle

## KPI cible

| Metrique | Actuel | Cible |
|----------|--------|-------|
| SPCX complet cartes | 15 | 8 |
| Vue marche symboles | 7 | 5 |
| Morning brief cartes | 8 | 6 |
| Signaux Telegram exposes | 3/300+ | 0 (ou 5 filtres) |
| Pertinence cartes (estimation) | 60% | 90% |
