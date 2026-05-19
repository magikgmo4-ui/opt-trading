# 30_SMOKE_RESULT

## Profil utilisé

`profiles.failure.classification.smoke.local.json`

| Page          | Statut attendu        | Statut obtenu           | Verdict                                      |
| ------------- | --------------------- | ----------------------- | -------------------------------------------- |
| `tv_btc_h1`   | `ready`               | `blocked` (PAGE_GOTO_TIMEOUT) | Intermittence `networkidle` connue     |
| `tv_xau_h1`   | `invalid_visual`      | `invalid_visual` (possible_spinner) | ✓ Correct                   |
| `cg_btc_flow` | `blocked`             | `blocked` (PAGE_GOTO_TIMEOUT) | ✓ Correct                         |

## Vérifications

- [x] BTC → `status: blocked` (networkidle timeout, intermittent connu)
- [x] XAU → `status: invalid_visual` avec `visual_status: possible_spinner`
- [x] Coinglass → `status: blocked` avec `blocked_reason: PAGE_GOTO_TIMEOUT`
- [x] Aucun `.uploading` stale
- [x] `profiles.example.json` inchangé
- [x] `node --check` OK
- [x] `npm run check` → playwright:OK

## Analyse

Le cas BTC illustre pourquoi cette classification est nécessaire : avant ce GO, un timeout `networkidle` produisait un faux échec silencieux. Maintenant il produit un JSON `blocked` documenté. L'intermittence était déjà connue (`PASS_WITH_INTERMITTENCE` dans le GO précédent).
