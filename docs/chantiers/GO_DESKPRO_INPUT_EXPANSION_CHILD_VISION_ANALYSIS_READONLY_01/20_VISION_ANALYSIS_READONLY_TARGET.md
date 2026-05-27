---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01_READONLY_TARGET
doc_type: target_spec
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01
created_at: 2026-05-25
---

# 20_VISION_ANALYSIS_READONLY_TARGET

## Rôle de `vision_analysis.v1` côté Desk Pro

`vision_analysis.v1` est un input optionnel read-only dans la synthèse Desk Pro.

Il représente le résultat d'une analyse visuelle de chart produite en amont
(bot_vision_step2 ou équivalent), consommée par Desk Pro en lecture seule
pour enrichir la synthèse avec des signaux visuels (support/résistance, trend, etc.).

## Contrat minimal `vision_analysis.v1`

```json
{
  "input_class": "vision_analysis.v1",
  "capture_id": "cap_YYYYMMDD_HHMMSS_SYMBOL_TF",
  "symbol": "BTCUSDT",
  "timeframe": "H1",
  "analysis_ts": "2026-05-25T00:00:00Z",
  "source_module": "bot_vision_step2",
  "freshness_state": "fresh",
  "signals": [
    {"type": "support_level", "value": 65000.0, "confidence": 0.85, "note": "..."},
    {"type": "resistance_level", "value": 68500.0, "confidence": 0.80, "note": "..."},
    {"type": "trend_direction", "value": "bullish", "confidence": 0.75, "note": "..."}
  ]
}
```

## Path par défaut

```
data/deskpro/inputs/vision_analysis/latest.json
```

## Comportement du reader

```python
read_vision_analysis(path=None) -> Optional[dict]
```

- `path=None` → lit depuis `VISION_ANALYSIS_LATEST`
- `path=explicit` → lit ce path (pour tests)
- Fichier absent → `None`
- JSON malformé → `None`
- `input_class != "vision_analysis.v1"` → `None`
- Pas un dict → `None`
- Jamais d'exception propagée

## Intégration dry_run

```python
build_desk_pro_dry_run_synthesis(
    signal_event,
    visual_context=None,
    desk_snapshot=None,
    market_metrics=None,
    vision_analysis=None,   # ← nouveau
)
```

- `vision_analysis=None` → warning `"vision_analysis missing: vision-context-free synthesis"`, status WARN si aucune autre erreur
- `vision_analysis=<dict>` → `summary.vision_analysis_present = True`, warning retiré

## Invariants

- Absent = WARN non bloquant, jamais FAIL.
- Reader ne fait jamais appel API / OCR / headless / modèle vision.
- Le payload `vision_analysis` est passé tel quel dans la synthèse (no transform).
