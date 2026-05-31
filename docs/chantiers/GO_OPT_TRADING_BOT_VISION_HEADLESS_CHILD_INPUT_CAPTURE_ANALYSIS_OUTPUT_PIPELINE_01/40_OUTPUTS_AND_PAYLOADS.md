---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01_OUTPUTS
doc_type: outputs_and_payloads
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01
---

# 40_OUTPUTS_AND_PAYLOADS.md

Catalogue des outputs générés par le pipeline.

## 1_MATRICE_DES_OUTPUTS

| Output | Format | Canal | Volume | Priorité |
|--------|--------|-------|--------|----------|
| Raw image | `.png` | Disque (data/screenshots/) | Toutes les captures | P0 |
| Annotated image | `.png` (avec overlays) | Disque + optionnel Telegram | Captures avec signal fort | P1 |
| Textual analysis | `.json` | Disque + Data Center | Toutes les analyses | P0 |
| Setup summary | `.json` | Data Center + DeskPro | Quand setup détecté | P0 |
| Telegram payload | texte court | Telegram | Filtré (importance haute) | P0 |
| Structured data payload | `.json` | Data Center POST | Toute analyse | P0 |
| DeskPro view | Vue agrégée | DeskPro / frontend | Synthèse périodique | P1 |

## 2_RAW_IMAGE

- Fichier : `data/screenshots/{capture_id}.png`
- Format : PNG, 1920x1080 (ou viewport natif)
- Rétention : 7 jours glissants (ou selon politique Data Center)
- Métadonnées : fichier JSON sidecar `{capture_id}.meta.json`

## 3_ANNOTATED_IMAGE

- Fichier : `data/annotated/{capture_id}_annotated.png`
- Overlays : niveaux S/R, tendance, labels, zones de signal
- Généré : uniquement si analyse détecte un signal significatif (confidence > 0.5)
- Usage : Telegram, DeskPro, relecture visuelle rapide

## 4_TEXTUAL_ANALYSIS

Format canonique (fichier sidecar JSON) :

```json
{
  "capture_id": "uuid",
  "screen_type": "CHART_TECHNICAL_SCREEN",
  "asset": "BTCUSDT",
  "timeframe": "15m",
  "summary": "BTC teste une résistance avec volume en hausse.",
  "signals": [
    {
      "type": "breakout_attempt",
      "direction": "bullish",
      "confidence": 0.68,
      "evidence": ["price above VWAP", "volume increasing", "RSI rising"]
    }
  ],
  "levels": {
    "support": [104000, 102800],
    "resistance": [106500, 108000]
  },
  "risk_flags": ["funding elevated", "liquidity above current price"],
  "next_watch": "confirmation above resistance or rejection back below VWAP"
}
```

## 5_SETUP_SUMMARY

Format setup (généré quand un setup trading est détecté) :

```json
{
  "setup_id": "uuid",
  "capture_id": "uuid",
  "asset": "BTCUSDT",
  "direction": "long|short",
  "entry_zone": [104500, 105000],
  "stop_loss": 103200,
  "targets": [106500, 108000, 110000],
  "conviction": "high|medium|low",
  "rationale": "Breakout résistance avec volume + funding reset + OI expansion",
  "risk_reward": 2.5,
  "timeframe": "4h",
  "generated_at_utc": "2026-05-29T00:00:00Z"
}
```

## 6_TELEGRAM_PAYLOAD

Format message Telegram (court, filtré, actionable) :

```text
🔵 BTCUSDT (15m)
Breakout attempt sur résistance 106500
Volume: hausse
RSI: 62 → momentum haussier
Funding: neutre

Signal: bullish (confiance 0.68)
Niveaux clés:
  S: 104000 / 102800
  R: 106500 / 108000

⚠ Funding elevated au-dessus du prix — risque de rejet
```

Règles d'envoi Telegram :
- Envoyer uniquement si confidence >= 0.6 OU setup détecté
- Ne pas envoyer si "risk_flags" contient "noise" ou "low_confidence_cluster"
- Maximum 8 messages / heure (rate limiting)
- Priorité : setup > breakout > divergence > routine

## 7_STRUCTURED_DATA_PAYLOAD

Payload complet pour Data Center POST :

```json
{
  "payload_type": "vision_analysis",
  "capture_id": "uuid",
  "source": "tradingview",
  "screen_type": "CHART_TECHNICAL_SCREEN",
  "asset": "BTCUSDT",
  "asset_class": "crypto",
  "timeframe": "15m",
  "timestamp_utc": "2026-05-29T00:00:00Z",
  "analysis": {
    "summary": "...",
    "signals": [...],
    "levels": {...},
    "risk_flags": [...]
  },
  "setup": null,
  "image_ref": "data/screenshots/{capture_id}.png",
  "image_annotated_ref": null,
  "telegram_sent": true,
  "deskpro_ready": true
}
```

## 8_FILTERING_ET_PRIORISATION

| Signal | Telegram | Data Center | DeskPro |
|--------|----------|-------------|---------|
| Routine (aucun signal fort) | NON | OUI | OUI |
| Breakout avec volume | OUI (si conf > 0.6) | OUI | OUI |
| Setup détecté | OUI (toujours) | OUI | OUI |
| Divergence macro | OUI (si impact BTC) | OUI | OUI |
| Funding extreme | OUI | OUI | OUI |
| Screener cluster | OUI (si thème fort) | OUI | OUI |
| News important | OUI | OUI | OUI |
