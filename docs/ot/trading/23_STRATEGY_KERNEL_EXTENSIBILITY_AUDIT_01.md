# STRATEGY KERNEL EXTENSIBILITY — AUDIT 01

Date (America/Montreal) : 2026-04-14

## RÔLE DU DOCUMENT

Ce document fixe l'audit canonique d'extensibilité du noyau stratégie à partir de l'état réel des modules :
- `modules/trading_lab_v1`
- `modules/trading_realtime_v1`

Il ne redéfinit pas l'intention produit générale déjà fixée pour `Range Strategy V1`.
Il part de cette intention déjà figée et mesure si le noyau actuel peut la supporter proprement.

Il sert à figer :
- l'état réellement établi du noyau actuel ;
- les points d'extension réellement présents ;
- les blocages actuels ;
- les changements requis pour aller vers multi-actifs / multi-stratégies ;
- le next GO recommandé.

## INTENTION / OBJECTIF FINAL HÉRITÉS

L'intention et l'objectif final déjà figés dans la documentation précédente restent les suivants :
- construire un cadre stratégique exécutable humainement, documentable, testable et journalisable ;
- rester compatible avec la continuité dual stack LAB / REALTIME ;
- ouvrir ensuite des familles de stratégie comme `range`, `fvg`, `breakout` sans casser le canon commun.

Le présent audit n'ouvre pas encore une nouvelle stratégie.
Il mesure la capacité réelle du noyau existant à les absorber.

## CLASSIFICATION

- Type : audit d'extensibilité du noyau stratégie
- Classe de travail : module durable documentaire
- Portée : doc-only
- Repo canonique : `opt-trading`
- Branche canonique de continuité : `sot/mainline`

## RÔLES / POSTURES RETENUS

### Recommandation par défaut
- posture retenue : **architecte stratégie + audit repo-source**

### Séparation explicite
- **Rôle machine** : aucun runtime ni aucune machine d'exécution engagés à ce stade.
- **Rôle IA/IDE** : vérifier le code réel, qualifier les points d'extension et mesurer le coût de transformation.
- **Rôle repo / produit** : préparer un noyau stratégie compatible avec `Range Strategy V1` et, plus largement, avec un futur cadre multi-actifs / multi-stratégies.

## ETABLI

À ce stade, les points suivants sont retenus comme établis :
- l'architecture canonique dual stack du repo vise déjà un noyau partagé entre LAB et REALTIME ;
- `trading_lab_v1` et `trading_realtime_v1` constituent une vraie base utile pour observation, journalisation, reporting et continuité ;
- l'implémentation réelle reste encore fortement câblée autour de `XAUUSD`, du profil `xauusd_dual_stack_v1` et de la stratégie `xau_session_open_v1` ;
- le LAB contient déjà des briques de détection / classification utiles : lecture de profil, sessions, détection `sweep`, détection `fvg`, construction de features, projection en `event` et `trade` ;
- le REALTIME contient déjà une chaîne observation -> event -> reporting -> export -> runtime loop -> guardrails -> timer, mais elle reste bornée en `observation_only` et fortement câblée XAU ;
- le noyau est donc factorisable en principe, mais il n'est pas encore réellement générique en code.

## POINTS D'EXTENSION RÉELS IDENTIFIÉS

Les vrais points d'extension du noyau actuel sont :

1. `Trader Frame`
   - timezone
   - sessions
   - fenêtres actives
   - discipline et risk communs

2. `Feature Extractor`
   - détection `sweep`
   - détection `fvg`
   - direction
   - structure des premières bougies de session

3. `Variant Resolver`
   - mapping entre features détectées et `variant_id`
   - encore trop simple et trop câblé XAU aujourd'hui

4. `Event / Trade Projection`
   - transformation des features en `event`
   - dérivation vers `trade`
   - projection vers reporting, export, comparator et runtime

## LIMITES STRUCTURELLES ACTUELLES

Le noyau actuel reste limité par :
- des constantes XAU codées en dur dans LAB et REALTIME ;
- un `profile_path` unique ;
- des `variant_id` embarquant encore le contexte XAU ;
- une logique de stratégie encore trop fusionnée dans le LAB ;
- l'absence d'interface stratégie proprement séparée entre :
  - extraction de features
  - résolution de variante
  - signal
  - entry model
  - risk model

## CE QU'IL FAUT CHANGER POUR ALLER VERS MULTI-ACTIFS

Pour rendre la couche stratégie multi-actifs, il faut au minimum :
- rendre injectables `profile_path`, `profile_id`, `symbol`, `strategy_id` et les sources de données ;
- sortir les constantes XAU du cœur LAB / REALTIME ;
- cesser de coder les variantes comme si elles étaient intrinsèquement liées à un seul actif ;
- enrichir le profil pour porter les informations stratégiques communes nécessaires à plusieurs actifs.

## CE QU'IL FAUT CHANGER POUR ALLER VERS MULTI-STRATÉGIES

Pour rendre la couche stratégie multi-stratégies, il faut au minimum :
- introduire une vraie interface stratégie partagée ;
- séparer explicitement :
  - `market_features`
  - `strategy_rules`
  - `variant_resolution`
  - `entry_model`
  - `risk_model`
- créer une couche de registre de stratégies ;
- permettre au REALTIME de consommer un profil / une stratégie / un symbole configurables, et non des constantes codées en dur.

## QUALIFICATION DES FAMILLES DE STRATÉGIES

### Familles proches du noyau actuel
- `fvg`
- `sweep`
- `session_open`
- `breakout` simple
- `reclaim` simple

### Familles possibles mais nécessitant une vraie extension de noyau
- `range`
- `mean_reversion`
- `range + sweep`
- `range + false breakout`
- `range + reclaim`

### Familles hors portée immédiate du noyau actuel
- stratégies multi-timeframe avancées
- stratégies corrélées cross-asset
- stratégies fortement dépendantes d'un contexte desk ou news non déjà encodé

## MESURE DU CHANGEMENT

### Ce qui relève encore d'un patch local
- rendre injectables quelques constantes ;
- sortir les IDs XAU trop codés ;
- préparer un premier résolveur de variantes moins rigide.

### Ce qui relève d'un lot structurant
- créer un noyau stratégie partagé LAB / REALTIME ;
- introduire une interface stratégie ;
- introduire un registre de stratégies ;
- rendre le noyau proprement multi-actifs et multi-stratégies.

## CONCLUSION D'AUDIT

Le repo dispose déjà d'un squelette utile et cohérent pour construire ce noyau.
Mais le passage réel vers `range`, `fvg`, `breakout` comme familles de premier niveau partageant un noyau commun nécessite un lot structurant, pas seulement un patch cosmétique.

## NEXT GO

`GO_STRATEGY_KERNEL_SHARED_LAYER_01`

Objectif du prochain GO :
- cadrer une couche stratégie partagée LAB / REALTIME ;
- définir les contrats minimaux de stratégie ;
- définir le premier chemin de migration depuis le noyau XAU actuel vers une base multi-actifs / multi-stratégies.

## REPRISE

- repo : `opt-trading`
- branche de travail : `feat/range-strategy-v1-struct`
- document d'entrée : `docs/ot/trading/23_STRATEGY_KERNEL_EXTENSIBILITY_AUDIT_01.md`
- prochain GO : `GO_STRATEGY_KERNEL_SHARED_LAYER_01`

## MEM_CANDIDATE

NO_MEMORY
