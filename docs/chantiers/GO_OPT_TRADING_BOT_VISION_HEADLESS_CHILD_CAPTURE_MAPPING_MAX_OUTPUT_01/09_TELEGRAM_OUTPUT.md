# 09 — Telegram Output

## Architecture Telegram existante

Deux implémentations coexistent :
1. **shared/telegram_notify.py** — production-grade (requests, métriques, utilisé par webhook/desk_pro/perf)
2. **bot_vision_step2 inline** — stdlib only (urllib, utilisé par bot_vision_step2)

## Filtre Telegram (nouveau)

`scripts/telegram_filter.py` est un module de filtrage qui décide si une analyse doit être envoyée à Telegram.

### Règles de filtrage

1. **Seuil de confiance** (défaut : 0.70)
   - Si au moins un signal a confidence ≥ seuil → envoyé
   - Sinon → ignoré (return code 2)
2. **Résumé condensé**
   - Extrait les lignes structurées (A), B), C), etc.)
   - Limite à 3500 caractères
3. **Mode dry-run**
   - `--dry-run` → affiche la décision sans envoyer

### Usage

```bash
# Décision + payload JSON sur stdout
python3 scripts/telegram_filter.py

# Preview seulement
python3 scripts/telegram_filter.py --dry-run

# Seuil personnalisé
python3 scripts/telegram_filter.py --confidence 0.80

# Run spécifique
python3 scripts/telegram_filter.py --run-dir /path/to/run
```

### Sortie

```json
{
  "send": true,
  "reason": "3 signal(s) above 0.70% confidence",
  "min_confidence": 0.70,
  "run_id": "2026-05-30_12-00-00",
  "symbols": ["BTCUSDT.P"],
  "filtered_signal_count": 3,
  "summary": "Résumé filtré...",
  "telegram_payload": {
    "message": "...",
    "disable_web_page_preview": true
  }
}
```

## Intégration pipeline

Dans `run_vision_pipeline.py`, après analyse :
1. Appeler `telegram_filter.py --dry-run`
2. Si return code 0 → décision d'envoi positive
3. Le payload JSON est prêt pour `shared/telegram_notify.send_telegram()`

## Gaps

- Le filtre ne fait que la décision ; l'envoi effectif est à intégrer (appel à shared/telegram_notify.py)
- Le filtrage OCR Coinglass (liquidations > $50M) n'est pas implémenté
- Pas de throttling Telegram (éviter les doublons sur des signaux redondants)
