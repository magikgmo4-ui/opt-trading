---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_TELEGRAM_CLAIM_READONLY_01_READONLY_TARGET
doc_type: target_spec
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_TELEGRAM_CLAIM_READONLY_01
created_at: 2026-05-25
---

# 20_TELEGRAM_CLAIM_READONLY_TARGET

## Rôle de `telegram_claim.v1` côté Desk Pro

`telegram_claim.v1` est un input optionnel read-only dans la synthèse Desk Pro.

Il représente un claim de contexte Telegram produit en amont par un screener inbound
(non implémenté à ce stade), consommé par Desk Pro en lecture seule pour enrichir
la synthèse avec le contexte de canal (direction, levels, confidence).

## Contrat minimal `telegram_claim.v1`

```json
{
  "input_class": "telegram_claim.v1",
  "claim_id": "tg_claim_YYYYMMDD_HHMMSS_SYMBOL",
  "source": "telegram_screener",
  "channel_id": "<channel_alias>",
  "message_id": "<message_ref>",
  "symbol": "BTCUSDT",
  "timeframe": "H1",
  "claim_ts": "2026-05-25T00:00:00Z",
  "claim_type": "trade_context",
  "text": "<raw claim text>",
  "entities": {
    "direction": "long",
    "levels": [65000.0, 68500.0],
    "confidence": 0.72
  },
  "refs": {
    "telegram_message_ref": "fixture://telegram/<channel>/<message_id>"
  }
}
```

## Path par défaut

```
data/deskpro/inputs/telegram_claim/latest.json
```

## Comportement du reader

```python
read_telegram_claim(path=None) -> Optional[dict]
```

- `path=None` → lit depuis `TELEGRAM_CLAIM_LATEST`
- `path=explicit` → lit ce path (pour tests)
- Fichier absent → `None`
- JSON malformé → `None`
- `input_class != "telegram_claim.v1"` → `None`
- Pas un dict → `None`
- Jamais d'exception propagée
- Jamais d'appel API Telegram, lecture channel live, envoi message

## Intégration dry_run

```python
build_desk_pro_dry_run_synthesis(
    signal_event,
    visual_context=None,
    desk_snapshot=None,
    market_metrics=None,
    vision_analysis=None,
    telegram_claim=None,   # ← nouveau
)
```

- `telegram_claim=None` → warning `"telegram_claim missing: telegram-context-free synthesis"`, status WARN
- `telegram_claim=<dict>` → `summary.telegram_claim_present = True`, warning retiré

## Invariants

- Absent = WARN non bloquant, jamais FAIL.
- Reader ne fait jamais appel Telegram API / channel live / envoi.
- Le payload `telegram_claim` est passé tel quel dans la synthèse (no transform).
