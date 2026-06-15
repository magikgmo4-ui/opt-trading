# 20_EXPOSURE_MATRIX

| Dataset | Collecte | DeskPro | LocalCMS | /read/* | Voice | Analytics | % Expose |
|---------|----------|---------|----------|---------|-------|-----------|----------|
| vision_analysis | ✅ 25 symboles | ✅ /desk/vision | ✅ /cms/vision | ❌ | ❌ | ❌ | **20%** |
| spacex_super_desk | ✅ 180 KB | ✅ /desk/spacex/* | ✅ /spacex | ✅ /read/spacex | ✅ 6 champs | ❌ | **60%** |
| telegram_signals | ✅ 212 MB | ✅ /cms/signals | ✅ /signals | ⚠️ 3 alertes | ⚠️ 3 alertes | ❌ | **30%** |
| deskpro analysis | ✅ 43 KB | ✅ interne | ❌ | ❌ | ❌ | ❌ | **10%** |
| voice_events | ✅ 295 B | ❌ | ❌ | ❌ | ✅ /voice/analytics | ✅ | **40%** |

## Detail par couche

### DeskPro
- ✅ vision_analysis: `/desk/vision`, `/desk/vision/news`, `/desk/vision/screener`
- ✅ spacex_super_desk: `/desk/spacex`, `/desk/spacex/snapshot`, `/desk/spacex/command-center`
- ✅ telegram_signals: `/cms/signals`, `/desk/vision/telegram-claim`
- ✅ deskpro_analysis: interne
- ❌ voice_events

### /read/*
- ❌ vision_analysis: non expose
- ✅ spacex_super_desk: `/read/spacex`
- ⚠️ telegram_signals: `/read/alerts` (3 signaux minimum)
- ❌ deskpro_analysis: non expose
- ❌ voice_events

### Voice Operator
- ❌ vision_analysis: 25 symboles absents des commandes
- ✅ spacex_super_desk: spcx_full (6/20 champs)
- ⚠️ telegram_signals: Alertes Telegram (3/300+ signaux)
- ❌ deskpro_analysis
- ✅ voice_events: /voice/analytics

### Analytics
- Seul voice_events est expose via `/voice/analytics`
- Aucun autre dataset Grade A n'a de dashboard analytics
