---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_DESKPRO_UI_PANEL_C_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_DESKPRO_UI_PANEL_C_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: closed
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_DESKPRO_UI_PANEL_C_01

## Objectif

Implémenter option C — Desk Pro UI panel dédié `vision_context.coinglass.v1`.

Livrer :
- `modules/desk_pro/service/vision_panel.py` — `read_vision_panel_data()` helper
- `GET /desk/vision` endpoint — retourne données panel ou `{ok: false}`
- Section `<details>` "Coinglass Vision" dans `/desk/ui` avec table détections, confidence bar, warnings, freshness

## Périmètre

- **IN** : `vision_panel.py`, endpoint, section UI, 8 tests
- **OUT** : write vers data/, activation prod, Telegram

## Architecture

```
GET /desk/vision
  read_vision_panel_data()
    data/deskpro/inputs/vision_context/coinglass/latest.json
    → {ok, vision, age_hours}

/desk/ui JS
  fetch('/desk/vision')
  → table detections (metric/value/conf bar/notes)
  → freshness badge
  → warnings inline
```

## Fichiers modifiés

| Fichier | Action |
|---|---|
| `modules/desk_pro/service/vision_panel.py` | créé |
| `modules/desk_pro/api/routes.py` | +import +`GET /desk/vision` |
| `modules/desk_pro/ui/page.py` | +section "Coinglass Vision" + JS refreshVision() |
| `tests/test_desk_pro_vision_panel.py` | créé |
