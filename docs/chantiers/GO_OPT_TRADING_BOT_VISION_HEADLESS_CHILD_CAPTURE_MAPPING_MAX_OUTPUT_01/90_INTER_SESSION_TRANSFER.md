# 90_INTER_SESSION_TRANSFER

## Objectif

Document de reprise rapide pour transferer l'etat du child GO entre sessions sans
re-auditer tout le repo.

## Branche de travail

- branche principale : `go/GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01`
- child GO cible : `GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01`
- parent confirme : `GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01`

## Etat etabli

- `PF_BOT_VISION_HEADLESS` reste `OPEN / ACTIVE_EXPANSION`
- le child GO `CAPTURE_MAPPING_MAX_OUTPUT` existe deja avec ses 8 docs de cadrage
- le parent reference maintenant explicitement ce child GO dans `00_INITIAL_PROJECT_DOC.md`
- `visual_context`, `vision_analysis.v1`, `vision_context.coinglass.v1`, `desk_snapshot.v1`
  et `market_metrics.v1` restent les contrats adjacents a respecter

## Ce qui est deja documente

- pages/sources a capturer
- univers d'actifs P0/P1
- families de `screen_type`
- triggers horaires / prix / liquidite / macro / screener
- analyseurs cibles par family d'ecran
- handoff Data Center et filtre Telegram

## Ce qui n'est pas stabilise

1. mapping URL runtime source par source
2. ecrans obligatoires P0/P1 a figer
3. normalisation runtime de `screen_type`
4. contrat canonique Data Center pour captures visuelles
5. projection finale DeskPro max-output
6. filtrage Telegram par importance/confiance

## Fichiers a relire d'abord

1. `docs/chantiers/GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01/00_CADRAGE_CHILD.md`
2. `docs/chantiers/GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01/01_CAPTURE_MAP.md`
3. `docs/chantiers/GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01/05_DATA_CENTER_INGESTION.md`
4. `docs/chantiers/GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01/50_DATA_CENTER_HANDOFF.md`
5. `docs/chantiers/GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01/60_DESKPRO_CONSUMPTION.md`

## Prochaine reprise utile

1. transformer `CAPTURE_MAP` en mapping runtime executable
2. definir le schema derive `visual_context` / `vision_analysis.v1` par `screen_type`
3. figer un payload principal `vision_pipeline_payload.v1` ou equivalent
4. choisir les sorties Telegram effectivement envoyables
5. prouver la jointure DeskPro sur un flux vision non-Coinglass
