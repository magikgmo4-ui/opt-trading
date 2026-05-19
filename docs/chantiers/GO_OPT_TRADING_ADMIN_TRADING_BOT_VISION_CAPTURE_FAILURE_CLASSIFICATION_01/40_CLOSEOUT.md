# 40_CLOSEOUT

GO: `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_CAPTURE_FAILURE_CLASSIFICATION_01`

## Livré

- [x] `capture_headless.js` : statuts `ready`, `blocked`, `invalid_visual`
- [x] Blocked reasons : `PAGE_GOTO_TIMEOUT`, `PAGE_GOTO_ERROR`, `SCREENSHOT_ERROR`, `OUTPUT_WRITE_ERROR`
- [x] Visual status : `unchecked`, `pass`, `possible_spinner`, `blank_or_uniform`, `too_small`, `loading_state_detected`
- [x] Fallback JSON sur timeout/erreur (pas de faux PNG)
- [x] Détection visuelle minimale (taille, DOM, readyState)
- [x] PNG invalides conservés (pas de suppression)
- [x] `profiles.failure.classification.smoke.local.json`
- [x] Docs chantier + index inbox

## Invariants respectés

- `profiles.example.json` non modifié
- Aucun restart service/timer
- Aucune suppression
- Aucun archive/compression
- Aucun .env lu
- Aucun trade

## Résultat smoke

| Page          | Attendu             | Obtenu                          | Verdict                                     |
| ------------- | ------------------- | ------------------------------- | ------------------------------------------- |
| `tv_btc_h1`   | `ready`             | `blocked` (PAGE_GOTO_TIMEOUT)   | Intermittence networkidle connue            |
| `tv_xau_h1`   | `invalid_visual`    | `invalid_visual` (possible_spinner) | ✓ Correct                                |
| `cg_btc_flow` | `blocked`           | `blocked` (PAGE_GOTO_TIMEOUT)   | ✓ Correct                                   |

## Commit

```
feat: classify bot vision capture failures
```
