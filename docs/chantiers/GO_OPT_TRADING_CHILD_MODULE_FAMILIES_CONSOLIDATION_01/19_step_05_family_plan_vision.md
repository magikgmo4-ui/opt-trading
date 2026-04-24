---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_05_VISION
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-05
  - vision
  - family-plan
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/status/bot_vision_canonique.md
  - docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md
  - docs/ot/project_cards/PROJECT_CARD_BOT_VISION_INGESTION_01.md
  - modules/bot_vision/README.md
  - modules/bot_vision_step2/README.md
  - modules/vision_bot/README.md
---

# Step 05 - family plan `Vision`

## Statut
Complete.

## Objet
Completer la structuration P2 de la famille `Vision` en separant heritage `step1`, transport capture et analyse / artefacts, sans forcer un survivant unique premature.

## Verifications utilisees
- lecture de `docs/status/bot_vision_canonique.md`
- lecture de `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`
- lecture de `docs/ot/project_cards/PROJECT_CARD_BOT_VISION_INGESTION_01.md`
- lecture des README de :
  - `modules/bot_vision`
  - `modules/bot_vision_step2`
  - `modules/vision_bot`

## Carte de suite
| Couche | Surface retenue | Role |
|---|---|---|
| heritage `step1` | `bot_vision` | squelette historique / placeholder visuel |
| capture / transport | `vision_bot` | inbox / outbox, transit ShareX / SFTP, traitement capture |
| analyse / artefacts | `bot_vision_step2` | Telegram, Vision analysis, artefacts Desk Pro |
| cible produit finale | spec a figer | chaine cross-platform headless non encore materialisee comme module unique |

## Frontieres retenues
- `bot_vision` reste la verticale historique `step1`. Il ne doit pas etre promu survivant par inertie.
- `vision_bot` reste le point d'entree capture / inbox-outbox de la chaine operatoire transitoire.
- `bot_vision_step2` reste la couche d'analyse Vision / Telegram / artefacts.
- le couple operatoire transitoire `vision_bot` + `bot_vision_step2` reste valide, mais ce n'est pas encore un survivant unique.
- si un consumer UI externe est introduit plus tard, il devra lire des artefacts ou contrats derives de cette chaine; il ne fait pas partie de la famille runtime actuelle.

## Ce qui doit etre harmonise
- contrats input/output entre `vision_bot` et `bot_vision_step2`
- vocabulaire d'artefacts :
  - inbox
  - processed
  - latest
  - artefacts desk
- documentation d'observabilite et d'erreurs
- formulation canonique de la cible cross-platform headless

## Ce qui peut etre mutualise plus tard
- conventions de wrappers et de logs
- petit contrat read-only pour exposer les sorties de vision a une UI consumer externe
- couche de specification unique pour la cible headless cross-platform

## Ce qui doit rester separe pour l'instant
- capture / transport et analyse Vision
- verticale historique `bot_vision` et chaine operatoire actuelle
- runtime present et cible produit finale non encore materialisee

## Risques a eviter
- declarer un survivant unique sans avoir fige la cible cross-platform
- fusionner `vision_bot` et `bot_vision_step2` alors que leurs responsabilites runtime restent distinctes
- garder `bot_vision` au meme niveau operatoire que la chaine transitoire
- relancer une refonte complete de la chaine avant d'avoir specifie le contrat cible

## Decision retenue
- oui a une structuration P2 explicite de la famille `Vision`
- non a une consolidation physique dans ce lot
- prochain travail utile :
  - `VISION_FAMILY_SURVIVOR_DECISION`
  - ou `GO_BOT_VISION_CROSS_PLATFORM_SPEC_01`

## Rollback
- revert doc-only de cette note
- revert doc-only du plan si besoin

## Point de reprise
Suite P2 `Vision` cadree. Basculer vers `Step 06` pour les familles a garder separees avec contrats renforces.
