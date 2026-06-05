---
doc_id: BRIDGE_GUARD_01_TESTS
doc_type: tests_smoke
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_TESTS_AND_SMOKE

## Test 0-byte + .uploading

Fichiers crees dans vision_inbox:
- `screen_test_0byte_*.png` (0 B)
- `screen_test_uploading_*.png.uploading.*` (0 B)

## Resultat

desk_bridge a SKIPPE les fichiers test et traite le fichier valide suivant.

```
Using source: .../vision_processed/screen_tradingview_BTCUSDT.P_H1_2026-05-04_19-52-16.png
Cropping with Python (PIL)...
Dropped 4 files into: .../inbox
processed: 4
OK: latest.json refreshed.
EXIT=0
```

## Cas nominal

Fichier valide traite normalement: crop 2x2 → 4 quadrants → ingest → exit 0.

## Verdict

| Cas | Resultat |
| --- | --- |
| PNG valide | TRAITE (4 quadrants, ingest OK) |
| PNG 0-byte | SKIP (silencieux) |
| .uploading | SKIP (silencieux) |
| PIL crash | 0 |

## RISKS

- À qualifier.
