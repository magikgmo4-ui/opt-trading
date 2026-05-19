# 00_INITIAL_PROJECT_DOC

GO: `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_SOAK_AND_RUNTIME_PROMOTION_DECISION_01`

## Objectif

Exécuter un soak contrôlé des 3 pages P0 maintenant stabilisées, puis produire une décision formelle de promotion runtime ou de report.

## Base validée

- source stability : `1841404a feat: stabilize bot vision p0 source loading`
- status-aware gate présent dans la base de branche via `06f59fbd` (équivalent local du gate accepté `7476721b`)
- profil utilisé : `modules/bot_vision/headless_capture/profiles.source.stability.smoke.local.json`
- surfaces P0 visées :
  - `tv_btc_h1`
  - `tv_xau_h1`
  - `cg_btc_flow`

## Invariants

1. `profiles.example.json` inchangé
2. aucun restart service/timer
3. aucune suppression/compression/archive
4. aucun `.env`
5. aucun trade
6. aucune promotion runtime appliquée dans ce GO
