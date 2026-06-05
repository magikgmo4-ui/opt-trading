---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01_DESK_BRIDGE_COMPAT
doc_type: desk_bridge_compatibility
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 40_DESK_BRIDGE_COMPATIBILITY - Desk Bridge Compatibility

## Input attendu par desk_bridge

`desk_bridge` (`bridge_vision_to_desk_inbox.sh`) attend :

- **Source primaire**: `vision_processed/screen_*.png` (triés par date, le plus récent)
- **Source fallback**: `vision_inbox/screen_*.png` (si rien dans processed)
- **Format**: PNG, nommé `screen_{...}_{timestamp}.png`
- **Timestamp parsing**: extraction via regex `^screen_([0-9]{4})-([0-9]{2})-([0-9]{2})_([0-9]{2})-([0-9]{2})-([0-9]{2})`

## Fichiers ignorés

| Pattern | Raison |
| --- | --- |
| `*.uploading` | Write atomique en cours |
| Fichier vide (0-byte) | Corrompu ou incomplet |
| Tout fichier non `screen_*.png` | Hors scope |

## Garde anti `.uploading`

```bash
[[ "$candidate" == *.uploading* ]] && continue
```

Double vérification :
1. Dans `pick_latest()` — skip au moment de la sélection
2. Dans `main()` — skip avant traitement (redondant, sécurité)

## Garde anti 0-byte

```bash
[ -s "$candidate" ] || continue
```

Double vérification :
1. Dans `pick_latest()` — `[ -s "$candidate" ]`
2. Dans `main()` — `[ ! -s "$src" ]`

## Output desk_snapshot attendu

| Champ | Valeur |
| --- | --- |
| Format | PNG (crop 2x2 quadrants) |
| Naming | `{SYMBOL}_{TF}_{ts}.png` |
| Symbols | BTCUSDT.P, XAUUSD, SOLUSDT.P, ETHUSDT.P |
| Timeframe | H1 (configurable via `$TF`) |
| Destionation | `inbox/` (SFTP shared) |
| Post-traitement | `cmd-desk_snapshot_ingest ingest_once` |

## Output desk_snapshot JSON (latest.json)

```json
{
  "BTCUSDT.P": {
    "symbol": "BTCUSDT.P",
    "tf": "H1",
    "snapshot_ts": "2026-05-06T02:25:35",
    "path": "/opt/trading/desk/snapshots/BTCUSDT.P/BTCUSDT.P_H1_20260506_022535.png",
    "ingested_at": "2026-05-06T02:25:35-04:00",
    "source": null,
    "host": null
  }
}
```

## Conditions PASS/FAIL

### PASS conditions

1. Le fichier source est un `screen_*.png` valide (> 0 byte, pas `.uploading`)
2. Le timestamp est extractible du nom de fichier
3. Le crop 2x2 produit 4 quadrants valides
4. Les 4 fichiers `{SYMBOL}_H1_{ts}.png` sont écrits dans `inbox/`
5. `desk_snapshot_ingest ingest_once` s'exécute avec succès
6. `latest.json` est mis à jour

### FAIL conditions

1. Source `.uploading` → skip silencieux
2. Source 0-byte → skip silencieux
3. Source introuvable → exit 2
4. Crop échoue (ni ImageMagick ni PIL) → exit 3 ou 4
5. `ingest_once` échoue → `latest.json` non mis à jour

## Matrice de compatibilité

| Producer | Artifact | Adapter | Output | Consumer | Required fields | Blocking gaps |
| --- | --- | --- | --- | --- | --- | --- |
| capture_headless.js | screen_{source}_{symbol}_{tf}_{ts}.png + .json | desk_bridge | {SYMBOL}_H1_{ts}.png | desk_snapshot_ingest | filename timestamp, valid PNG | playwright missing (STALE) |
| ShareX (cursor-ai) | screen_{...}_{ts}.png | desk_bridge | {SYMBOL}_H1_{ts}.png | desk_snapshot_ingest | filename timestamp, valid PNG | none (CONFIRMED) |
| desk_snapshot_ingest | {SYMBOL}_H1_{ts}.png + latest.json | — | desk/snapshots/ | Desk Pro | symbol, tf, snapshot_ts, path | Desk Pro not running |

## Compatibilité avec visual_context V1

Le `visual_context` V1 sidecar produit par `capture_headless.js` est compatible avec `desk_bridge` car :

1. Le sidecar n'est pas lu par `desk_bridge` (qui se base uniquement sur le nom de fichier PNG)
2. Le sidecar est déplacé/copié par `desk_snapshot_ingest` dans `desk/snapshots/{SYMBOL}/`
3. Le sidecar peut enrichir `latest.json` via les champs `source` et `host` de `ingest_snapshots.py`

Gap: `desk_bridge` ne lit pas le sidecar JSON → les métadonnées V1 ne sont pas propagées automatiquement vers `desk_snapshot`.

## RISKS

- À qualifier.
