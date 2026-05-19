# SESSION_DOCUMENTATION_INTEGRALE_20260517

## CONTEXTE
Session visant à transformer l'écosystème existant (TradingView, Telegram, screeners, vision, perf engine, Google Sheets, watchlists, desk pro) en pipeline de signaux monitorés.

## DEMANDE ORIGINALE
Tester des stratégies SMC/ICT avec screener headless + TradingView + bot vision + Telegram + perf engine + desk pro + screenshots + webhooks + statistiques.

## DECISIONS VALIDÉES
- Ouvrir un chantier parent dédié.
- Créer une branche dédiée.
- Documenter intégralement le plan.
- Garder phase initiale doc-only.
- Aucun live trading.
- Monitoring statistique obligatoire.
- Journalisation avant notification.

## ARTEFACTS CRÉÉS DANS CETTE SESSION
- branche: go/GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01
- docs/chantiers/.../00_INITIAL_PROJECT_DOC.md
- docs/index/inbox/GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01.md
- présent document.

## ETABLI
Le prochain travail doit commencer par l'inventaire réel du repo et NON par de nouveaux modules.

## NEXT_GO
GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01
Objectif: cartographier TradingView / Telegram / perf engine / vision / Google Sheets / watchlists / runtime déjà présents.

## REPRISE_PC
1. git fetch
2. git pull --rebase
3. checkout go/GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01
4. lire 00_INITIAL_PROJECT_DOC.md
5. lancer inventaire repo
