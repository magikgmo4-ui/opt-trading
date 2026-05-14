# 10_BRANCH_CROSSWALK

## Branches Recroisees

| Branche | Role canonique | Unite de travail | Sortie principale |
|---|---|---|---|
| `go/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01` | dataset bottom-up | ticker public + classification + scoring futur | parent doc + child dataset V1 |
| `go/GO_STOCK_SPACE_AI_MARKET_STRUCTURE_PARENT_01` | these top-down | lecture sectorielle `SpaceX -> beneficaires indirects` | session plan sectoriel |

## Fichiers Sources Utiles

| Branche | Fichiers observes | Signal principal |
|---|---|---|
| `watchlist` | `00_initial_project_doc.md`, `children/GO_CHILD_RESEARCH_DATASET_01/30_initial_dataset.md` | univers public de tickers, logique dataset, scoring futur |
| `market-structure` | `GO_SPACE_X_ECOSYSTEM_MAP_01_session_plan.md` | these `SpaceX`, `FLY`, effets second ordre, modele parabolic growth |

## Structure Canonique Extraite

### Parent `watchlist`

Doit rester le parent canonique pour :
- l'univers des titres cotes ;
- la classification par theme / role / risque ;
- le dataset qualitatif ;
- le futur scoring et la priorisation ;
- les ajouts / retraits de tickers publics.

### Parent `market-structure`

Doit rester le parent canonique pour :
- la these `SpaceX` et les effets de validation sectorielle ;
- la lecture `proxy public`, `second liners`, `supply chain`, `IPO scenario` ;
- les comparaisons top-down entre acteurs spatiaux ;
- `FLY` et les actifs narratifs qui ne sont pas encore des entrees dataset ticker-first ;
- le modele `x2 / x5 / x10` et le risque parabolic growth.

## Matrice De Recroisement

| Element | Watchlist | Market structure | Parent canonique | Decision student | Patch minimal suivant |
|---|---|---|---|---|---|
| `NVDA` | present, coeur IA | present, couche compute IA | `watchlist` | reste fiche dataset publique ; garde une mention sectorielle dans `market-structure` | aucun patch urgent |
| `AMD` | present, challenger IA | present, couche compute IA | `watchlist` | meme traitement que `NVDA` | aucun patch urgent |
| `RKLB` | present, dataset spatial | present, proxy public principal de `SpaceX` | partage avec ancrage `market-structure` pour la these | conserver la ligne dataset et garder la these proxy dans `market-structure` | aucun patch urgent |
| `ASTS` | present, dataset spatial telecom | present, pari telecom spatial | partage avec ancrage `watchlist` pour le suivi ticker | pas de conflit ; garder double presence avec roles distincts | aucun patch urgent |
| `PL` | present, dataset data spatiale | present, couche data satellite | partage avec ancrage `watchlist` pour le suivi ticker | pas de conflit ; garder double presence avec roles distincts | aucun patch urgent |
| `LUNR` | present, dataset lunaire / NASA | absent | partage avec ancrage `watchlist` pour le ticker, extension `market-structure` pour la these | ajouter `LUNR` au parent `market-structure` comme acteur lunaire / NASA et beneficaire indirect complementaire | patch prioritaire sur `market-structure` |
| `FLY` | absent du dataset et absent du schema ticker V1 | present, acteur lanceur / defense plus speculatif | `market-structure` | rester cote these sectorielle tant que l'integration ticker publique n'est pas formalisee dans `watchlist` | ajouter une note explicite d'exclusion / defer dans `watchlist` |
| `PLTR` | present, pont IA + defense | absent | `watchlist` | reste hors du perimetre `SpaceX` tant qu'aucun angle spatial direct n'est ajoute | aucun patch urgent |
| `SpaceX` | absent comme normal | centre de la these | `market-structure` | reste exclusivement dans la these sectorielle | aucun patch urgent |

## Decision Canonique `LUNR` / `FLY`

### `LUNR`

- `LUNR` est deja normalise dans le dataset `watchlist`.
- Le parent `market-structure` compare aujourd'hui `FLY / RKLB / ASTS / PL`, mais laisse un trou sur la brique lunaire / NASA deja retenue ailleurs.
- Decision : ajouter `LUNR` a `market-structure` sans deplacer sa fiche dataset hors de `watchlist`.

### `FLY`

- `FLY` est central dans la these `SpaceX` mais n'apparait nulle part dans le dataset `watchlist` V1.
- Le parent `watchlist` est structure comme une base ticker-first des actions publiques a suivre.
- Decision : `FLY` reste dans `market-structure` tant qu'une integration dataset publique explicite n'est pas definie et validee.

## Patch / PR Plan Canonique

### Patch 1

Branche cible : `go/GO_STOCK_SPACE_AI_MARKET_STRUCTURE_PARENT_01`

Objectif : integrer `LUNR` proprement.

Changements minimaux :
- ajouter `LUNR / Intuitive Machines` dans la liste d'actifs suivis ;
- etendre la comparaison `FLY / RKLB / ASTS / PL` vers `LUNR / RKLB / FLY / ASTS / PL` ;
- ajouter une ligne de these sur la couche lunaire / NASA ;
- mettre a jour resume point et todo du parent.

### Patch 2

Branche cible : `go/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01`

Objectif : figer la frontiere avec `market-structure`.

Changements minimaux :
- ajouter une note que `FLY` reste traite dans `market-structure` ;
- rappeler que `watchlist` est la couche canonique des tickers publics et du scoring ;
- conserver `LUNR` dans le dataset comme entree ticker publique deja validee.

### PR Student A Preparer

Le prochain paquet `student` doit proposer :
- une matrice crosswalk resumee ;
- le patch `LUNR` pour `market-structure` ;
- la note de frontiere `FLY` pour `watchlist` ;
- aucun changement global d'index sans validation explicite.
