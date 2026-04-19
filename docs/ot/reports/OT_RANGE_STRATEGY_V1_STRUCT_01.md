# OT_RANGE_STRATEGY_V1_STRUCT_01

Date: 2026-04-14

## 1. Objet

Ouvrir un chantier documentaire canonique pour formaliser une stratégie de trading en range centrée sur trois actifs validés en séance :
- AUD/NZD
- USD/CHF
- XAUUSD

Le document fige :
- le besoin initial ;
- la cible finale retenue ;
- le plan validé ;
- l'état établi actuel ;
- l'écart restant ;
- le prochain GO logique.

## 2. Classification

- Classe : module durable documentaire
- Nature : structuration stratégie / trading
- Portée : doc-only
- Repo canonique : `opt-trading`
- Branche canonique de continuité : `sot/mainline`

## 3. Rôles / postures retenus

### Recommandation par défaut
- **Posture recommandée : architecte stratégie + cadrage opératoire**

### Séparation des rôles
- **Rôle machine** : aucune machine runtime engagée à ce stade ; travail documentaire repo-side.
- **Rôle IA/IDE** : figer la stratégie, les règles, les hypothèses bornées et le point de reprise.
- **Rôle repo / produit** : porter une base canonique réutilisable pour une future stratégie range dans `opt-trading`.

## 4. Besoin initial

Identifier des actifs connus pour évoluer régulièrement dans des ranges de prix stables et relativement simples à trader, puis retenir un sous-ensemble exploitable pour une stratégie range structurée.

## 5. Cible finale retenue

Construire une stratégie `Range Strategy V1` :
- simple ;
- disciplinée ;
- centrée sur des ranges exploitables ;
- compatible avec une journalisation et une future formalisation de règles d'exécution ;
- bornée à trois actifs de référence :
  - `AUD/NZD`
  - `USD/CHF`
  - `XAUUSD`

## 6. ETABLI

Les points suivants sont retenus comme établis à ce stade :

- Le besoin utilisateur est explicitement centré sur des actifs faciles à trader en range.
- Trois actifs ont été retenus et validés en séance comme stack initiale :
  - `AUD/NZD` = profil range propre / serré ;
  - `USD/CHF` = profil lent / stable / technique ;
  - `XAUUSD` = profil range exploitable avec meilleur potentiel de RR mais timing plus exigeant.
- La suite logique validée est d'ouvrir un chantier documentaire propre dans le repo canonique.
- Aucun patch runtime, aucun backtest, aucun module d'exécution n'est encore engagé par ce document.

## 7. Plan validé

Le plan validé reconstitué pour `Range Strategy V1` est :

1. Figer les actifs de référence.
2. Définir le cadre de lecture du range par actif.
3. Formaliser les règles d'entrée.
4. Formaliser les règles de sortie, SL, TP et invalidation.
5. Définir la discipline de session et les cas à éviter.
6. Préparer une journalisation et une évaluation statistique futures.
7. Seulement ensuite décider s'il faut une déclinaison module, sheet, ou backtest.

## 8. Gap restant

Le chantier n'établit pas encore :

- les règles exactes d'entrée/sortie ;
- le protocole de confirmation (sweep, rejet, FVG, etc.) figé ;
- les sessions privilégiées par actif ;
- le modèle de risque unifié ;
- le format de journalisation ;
- la forme de livraison future (doc complémentaire, sheet, module, bundle).

## 9. Bornes explicites

Ce chantier n'autorise pas encore :

- de prétendre qu'une stratégie complète est validée ;
- d'annoncer un winrate ;
- d'ouvrir un module runtime ;
- de déployer un système automatique ;
- de confondre cadrage documentaire et validation statistique.

## 10. Next GO

`GO_RANGE_STRATEGY_V1_RULES_01`

Objectif du prochain GO :
- formaliser les règles opératoires minimales de la stratégie ;
- séparer clairement ce qui est ETABLI, HYPOTHÈSE et À TESTER ;
- préparer une base exploitable pour journalisation ou backtest ultérieur.

## 11. REPRISE

Point de reprise recommandé :
- relire `docs/ot/reports/OT_RANGE_STRATEGY_V1_STRUCT_01.md`
- ouvrir ensuite `GO_RANGE_STRATEGY_V1_RULES_01`

## 12. Tags utiles

- ETABLI
- TODO
- REPRISE
- GO_RANGE_STRATEGY_V1_RULES_01
- NO_MEMORY
