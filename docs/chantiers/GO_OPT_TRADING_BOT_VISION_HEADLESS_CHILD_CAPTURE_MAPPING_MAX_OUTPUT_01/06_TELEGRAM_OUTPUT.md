---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01_TELEGRAM
doc_type: telegram_output
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01
---

# 06_TELEGRAM_OUTPUT.md

Filtrage et format des notifications Telegram.

## 1_PRINCIPES

- Telegram ne reçoit QUE les signaux utiles (pas de bruit)
- Seuil minimum : confiance >= 0.6 OU setup détecté
- Maximum 8 messages/heure (rate limiting)
- bot_vision_step2 gère déjà l'envoi Telegram — ne pas dupliquer

## 2_REGLE_DE_FILTRAGE

| Condition | Action |
|-----------|--------|
| confidence >= 0.8 | Envoyer (signal fort) |
| confidence >= 0.6 + setup détecté | Envoyer |
| confidence >= 0.6 | Envoyer (signal modéré) |
| confidence < 0.6 | Ne pas envoyer |
| risk_flags contient "noise" | Ne pas envoyer |
| Même actif < 5 min | Ne pas envoyer (dedup) |

## 3_FORMAT_MESSAGE

```
🔹 BTCUSDT (15m)
Breakout attempt — confiance 0.68

Tendance: haussier
Structure: HH/HL
Niveaux: S 104000 | R 106500

📊 Volume: hausse
⚡ Funding: neutre

⚠ Funding élevé au-dessus du prix
```

## 4_CANAUX_D_ENVOI

| Canal | Usage | Géré par |
|-------|-------|----------|
| Image + analyse | Capture chart + résumé | bot_vision_step2 (existant) |
| Texte seul | Signal rapide | bot_vision_step2 (existant) |
| Alerte setup | Setup détecté | bot_vision_step2 (existant) |

## 5_DEDUPLICATION

- bot_vision_step2 utilise `sender_state.json` pour tracker le dernier envoi par actif
- Ne pas renvoyer le même actif dans la même fenêtre de 5 minutes
- Même hash d'analyse = skip

## 6_RATE_LIMITING

| Limite | Période | Comportement |
|--------|---------|-------------|
| 8 messages | 1 heure | Skip, log warning |
| 1 message | 5 secondes | Queue, attendre |
| 10 MB | 1 heure | Images uniquement |

Note : bot_vision_step2 gère déjà le rate limiting côté Telegram API. Aucun changement nécessaire.
