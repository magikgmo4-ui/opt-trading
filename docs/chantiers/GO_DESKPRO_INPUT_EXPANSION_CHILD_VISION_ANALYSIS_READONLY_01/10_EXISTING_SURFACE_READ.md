---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01_EXISTING_SURFACE_READ
doc_type: surface_read
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01
created_at: 2026-05-25
---

# 10_EXISTING_SURFACE_READ

## Inventaire vision côté repo (pré-GO)

### `visual_context.v1` — déjà fermé

- `modules/desk_pro/service/vision_context_reader.py` — reader existant
- `dry_run.py` — param `visual_context: dict | None` intégré
- Fixture `visual_context_v1_minimal.json` existante

### `vision_analysis.v1` — absent (gap ouvert)

Aucun fichier `vision_analysis_reader.py` dans le repo.

Références trouvées :
- `modules/desk_pro/ui/vision_panel.py` — affiche champ `vision_analysis` dans l'UI mais ne le lit pas
- `modules/desk_pro/ui/page.py` — référence `vision_analysis` en display

Aucune lecture effective ni contrat de lecture existant.

### bot_vision / headless

- `modules/bot_vision/` — squelette legacy step1, non runtime survivor
- `modules/bot_vision_step2/` — operational capture point ; produit des outputs de capture
- `modules/vision_bot/` — inbox/outbox processor (ShareX → SFTP → markdown)
- Headless Playwright : `modules/bot_vision/headless_capture/` — Node.js, install séparé

Aucun de ces modules ne produit un fichier `vision_analysis.v1` consommable par Desk Pro read-only.
Le format `vision_analysis.v1` est une convention interne à définir / prouver côté Desk Pro.

### Fixtures existantes liées

- `tests/fixtures/admin_trading_contract_smoke/visual_context_v1_minimal.json` ✓
- `tests/fixtures/admin_trading_contract_smoke/market_metrics_v1_minimal.json` ✓
- Aucune fixture `vision_analysis_v1_*` avant ce GO.

## Conclusion

Le reader `vision_analysis` est à créer de zéro.
Le contrat minimal (`input_class`, `capture_id`, `symbol`, `analysis_ts`, `signals`) est
à définir par fixture-first pour prouver la consommation Desk Pro read-only.
