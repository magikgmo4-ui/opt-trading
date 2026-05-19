# 00_INITIAL_PROJECT_DOC

GO: `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SOURCE_STABILITY_MATRIX_01`

## Objectif

Stabiliser les sources P0 du bot vision headless avant toute promotion runtime ou politique de rétention/archive.

## Base validée

- `d313a66f` : producer status-aware (`ready` / `blocked` / `invalid_visual`)
- `7476721b` : consumers status-aware (`vision_bot.py`, `bridge_vision_to_desk_inbox.sh`, `ingest_snapshots.py`)
- P0 initial encore partiellement bloqué :
  - `tv_btc_h1` : timeout / `networkidle` intermittent
  - `tv_xau_h1` : spinner / `invalid_visual`
  - `cg_btc_flow` : timeout ou faux positif visuel

## Invariants

1. `profiles.example.json` inchangé
2. Aucun profil runtime actif modifié
3. Aucun restart service/timer
4. Aucune suppression destructive
5. Aucun `.env`
6. Aucun trade

## Livrables

1. Matrice de stabilité documentée
2. Profil smoke non runtime principal
3. Profil alt non runtime
4. Fixes minimaux du producteur pour refléter le comportement réel des pages SPA
5. Décision de promotion documentée
