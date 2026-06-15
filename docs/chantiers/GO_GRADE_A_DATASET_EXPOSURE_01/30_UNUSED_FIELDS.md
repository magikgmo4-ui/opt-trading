# 30_UNUSED_FIELDS

## vision_analysis — 25 symboles, champs disponibles

| Champ | Utilise par Voice? | Utilise par DeskPro? | Action |
|-------|-------------------|---------------------|--------|
| price | ❌ | ✅ | Exposer dans Vue marche |
| trend | ❌ | ✅ | Exposer dans Gold complet, BTC |
| support/resistance | ❌ | ✅ | Exposer dans setup/risque |
| rsi | ❌ | ❌ | Exposer score technique |
| macd | ❌ | ❌ | Exposer score technique |
| volume | ❌ | ❌ | Exposer volume relatif |
| pattern | ❌ | ✅ | Exposer setup SMC |
| confidence | ❌ | ❌ | Exposer confiance |
| freshness_state | ❌ | ❌ | Exposer fraicheur (deja gere) |

**25 symboles analyses par GPT, 0 exposes dans Voice.**

## spacex_super_desk — champs collectes vs exposes

| Champ | Voix? | Action |
|-------|-------|--------|
| price | ✅ | - |
| gap_ipo | ✅ | - |
| volume | ❌ | Ajouter a SPCX complet |
| VWAP | ✅ | - |
| edge_score | ❌ | Ajouter a SPCX complet |
| open_score | ❌ | Ajouter a SPCX complet |
| action | ❌ | Ajouter recommendation |
| confidence | ❌ | Ajouter |
| top_setup | ❌ | Ajouter |
| sector_regime | ❌ | Ajouter |
| ipo_analogs | ❌ | Ajouter contexte |
| risks | ❌ | Ajouter a SPCX risque |
| entry/stop/tp1/tp2 | ❌ | Ajouter niveaux |
| market_state | ❌ | Ajouter etat marche |
| sources_ok/sources_total | ❌ | Ajouter qualite source |
| pipeline_healthy | ❌ | Ajouter |
| orderflow_score | ✅ | - |
| ownership_pressure_score | ✅ | - |

**20 champs disponibles, 6 exposes dans Voice (30%).**

## telegram_signals — 300+ signaux, 3 exposes

212 MB de signaux scores. Voice n'expose que 3 alertes anonymes.
Champs disponibles par signal: channel, pair, direction, entry, tp, sl, confidence, score, timestamp, qualification.

## deskpro_analysis — 43 KB, 0 expose

Rapport GPT complet sur SPCX. Aucun endpoint /read/* ni commande Voice.

## voice_events — utilisation interne uniquement

Dashboard analytics existant. Pas de champs inutilises.
