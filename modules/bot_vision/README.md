# bot_vision

Verticale vision historique de la famille Bot Vision, encore presente comme `step1` de generation visuelle placeholder.

## Role
- fournir un premier squelette de generation d'artefacts visuels pour `desk_pro_vision`
- produire des charts placeholder, une mosaique et un `summary.json`
- exposer les wrappers standard `cmd/menu/sanity` pour cette surface

## Contenu
- `bot_vision_step1/desk_pro_vision/vision/` : generateur visuel placeholder (`charts`, `mosaic`, `pack`, `vision_generate`)
- `bot_vision_step1/INSTALL_STEP1.md` : cadrage d'installation du step 1
- `scripts/cmd.sh`, `menu.sh`, `sanity_check.sh`, `install_shortcuts.sh`

## Integration
- fonctionne comme premiere etape de la lignee `Bot Vision`
- a lire avec :
  - `modules/bot_vision_step2`
  - `modules/vision_bot`
  - `docs/status/bot_vision_canonique.md`

## Statut
- actif mais ambigu au niveau famille
- surface de transition / heritage plus que survivant clairement fige

## Notes de consolidation
- ne pas considerer `bot_vision` comme survivant automatique de la famille
- la famille vision reste sous arbitrage :
  - `bot_vision` = step 1 skeleton / generation placeholder
  - `bot_vision_step2` = point d'appui operatoire documente
  - `vision_bot` = flux inbox/outbox et traitement capture
- releve du futur lot `VISION_FAMILY_SURVIVOR_DECISION`
