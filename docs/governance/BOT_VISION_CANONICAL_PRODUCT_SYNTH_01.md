# BOT VISION — SYNTHÈSE CANONIQUE PRODUIT

## Lecture canonique

- lire cette synthese apres `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- recroiser `docs/governance/MATRICE_GOUVERNANTE_V2.md` seulement comme annexe stable secondaire si utile

## 1. Objet
Ce document synthétise le produit **Bot Vision** dans un format court et opposable, figeant son objectif final et la trajectoire de sortie de dépendance.

## 2. Besoin initial
Transformer des captures d'écran en analyse exploitable sans subir un workflow fragile ni une dépendance trop forte à une plateforme spécifique (Windows/ShareX).

## 3. Cible finale
Un pipeline vision cross-platform où un provider headless browser unifie `bot_vision` entre Windows et Linux sans dépendre de ShareX, afin de produire des artefacts Desk Pro exploitables.

## 4. Plan validé
- `vision_bot` : réception et traitement de captures.
- `bot_vision_step2` : interaction Telegram + analyse + génération d'artefacts Desk Pro.
- Direction de maturité : Sortir de la dépendance forte à ShareX / Windows-only et stabiliser une chaîne vision unifiée headless.

## 5. ETABLI
- Modules existants dans le repo (modules/vision_bot, modules/bot_vision_step2).
- Contrat input/output de base repo-sourcé.
- Chaîne partielle mais réelle (fortement couplée Windows/ShareX/SFTP).

## 6. Gap restant
- Le pipeline actuel repose encore sur Windows / ShareX / SFTP côté capture.
- La cible finale (headless browser cross-platform) n'est pas encore matérialisée comme spécification canonique explicite figée dans le repo.

## 7. Next GO
> GO_BOT_VISION_CROSS_PLATFORM_SPEC_01 (clarifier repo-source la cible produit finale et mesurer l'écart)
